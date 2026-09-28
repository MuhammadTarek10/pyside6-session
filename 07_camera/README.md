# 07 — Using the camera (OpenCV + QThread)

A live camera preview with mirror/grayscale toggles and snapshots. It puts topic 6 into practice:
the capture loop runs in a worker thread and hands frames to the GUI through a signal.

```bash
./build.sh 07_camera
python 07_camera/main.py
```

> **macOS:** the first run needs camera permission for your terminal/IDE:
> *System Settings → Privacy & Security → Camera → enable Terminal / iTerm / VS Code*,
> then **restart the terminal**. Without it, you'll see "Cannot open camera 0".
> Do this **before** the session!

## Architecture
```
 ┌─────────────── worker thread ───────────────┐        ┌──────────── GUI thread ────────────┐
 │ CameraWorker.run()                          │        │ CameraWindow                       │
 │   cap = cv2.VideoCapture(0)                 │        │                                    │
 │   while not interrupted:                    │ Signal │                                    │
 │       ok, frame = cap.read()   (numpy BGR)  │───────►│ show_frame(QImage)                 │
 │       img = to_qimage(frame)   (QImage)     │ queued │   label.setPixmap(scaled pixmap)   │
 │       frame_ready.emit(img)                 │        │                                    │
 │   cap.release(); finished.emit()            │───────►│ thread.quit → cleanup              │
 └─────────────────────────────────────────────┘        └────────────────────────────────────┘
```

## Key steps

### 1. numpy (OpenCV) → QImage
```python
rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)          # OpenCV is BGR, Qt is RGB
h, w, _ = rgb.shape
img = QImage(rgb.data, w, h, rgb.strides[0], QImage.Format.Format_RGB888).copy()
```
- Pass `bytesPerLine` (`strides[0]`), or images come out **skewed** at some resolutions.
- `.copy()` matters: without it the QImage points into a numpy buffer that is freed after the
  function returns, and you get garbage frames or crashes.
- **QImage** is safe to create in a worker thread. **QPixmap** is not (it's a GPU/screen resource), so
  it's only created in `show_frame`, on the GUI thread.

### 2. Settings while the loop runs: why `DirectConnection`?
The worker thread sits inside `while ...: cap.read()`, so its **event loop never runs**. A normal
signal → worker-slot connection is *queued* and would never be delivered. So we use
```python
self.grayCheck.toggled.connect(self.worker.set_grayscale, Qt.ConnectionType.DirectConnection)
```
The slot then runs immediately in the GUI thread, and it only sets a `bool` that the loop reads on the next frame.
That's fine for simple flags. For anything more complex, protect it with a lock (`QMutex`/`threading.Lock`).

### 3. Stop and cleanup
Stop → `thread.requestInterruption()` → the loop exits → `capture.release()` in `finally` →
`finished` → thread quits. `closeEvent` waits for this so the camera is released and the LED goes off.

## Why not QtMultimedia?
Qt6 has its own camera API (rewritten from Qt5, see topic 2):
```python
from PySide6.QtMultimedia import QCamera, QMediaCaptureSession, QMediaDevices, QImageCapture
from PySide6.QtMultimediaWidgets import QVideoWidget
session = QMediaCaptureSession()
session.setCamera(QCamera(QMediaDevices.defaultVideoInput()))
session.setVideoOutput(video_widget); session.camera().start()
```
| | OpenCV (this demo) | QtMultimedia |
|---|---|---|
| Extra dependency | `opencv-python` (+ numpy) | none |
| Access to each frame as a numpy array | ✅ trivial | via `QVideoSink` → `QVideoFrame.toImage()` |
| Computer vision (faces, filters, ML) | ✅ the whole cv2 ecosystem | ❌ you convert anyway |
| Threading | you manage it (good practice for topic 6) | Qt manages it internally |
| Recording video / device names | manual | ✅ `QMediaRecorder`, `QMediaDevices` |

Rule of thumb: **processing frames → OpenCV; just preview/record → QtMultimedia.**

## Common mistakes
- Forgetting BGR→RGB → people look blue 🔵.
- Building a `QPixmap` in the worker thread → warnings or random crashes.
- Not calling `capture.release()` → "camera busy" on the next start (and the LED stays on).
- Emitting frames faster than the GUI can paint → growing lag. Here `cap.read()` naturally paces at the camera FPS.
  If you add heavy processing, drop frames instead of queueing them.
- Wrong camera index. On Macs with an iPhone nearby, **Continuity Camera** may be index 0 or 1.

## Exercise
1. Add an **Edges** checkbox that applies `cv2.Canny(gray, 100, 200)` (show it as Grayscale8).
2. Add a **Record** button that writes frames with `cv2.VideoWriter` *inside the worker thread*.
3. Bonus: detect faces and draw rectangles before converting to QImage. Note that OpenCV 5 removed
   `cv2.CascadeClassifier`, so use `cv2.FaceDetectorYN` with the YuNet model in `answers/models/`.

🧩 Starter code: [`starter/`](starter/README.md) · ➡️ Answer: [`answers/`](answers/README.md)
