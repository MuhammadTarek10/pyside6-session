# 07 — Answer: Edges, Record, Faces

```bash
./build.sh 07_camera
python 07_camera/answers/main.py
```
New in the UI (`main_window.ui`): **Edges** and **Faces** checkboxes, and a checkable **⏺ Record** button.
Recordings and snapshots go to `answers/captures/` (git-ignored).

## Pipeline (all in the worker thread)
```
cap.read() → mirror → [draw faces] → [Canny edges | grayscale | color] → [VideoWriter.write] → QImage → emit
```
`CameraWorker.process()` returns either a 3-channel BGR frame or a 2D grayscale one, and `to_qimage()`
picks `Format_RGB888` or `Format_Grayscale8` from `frame.ndim`.

## 1. Edges
```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
return cv2.Canny(gray, 100, 200)       # 2D uint8: 255 on edges, 0 elsewhere
```
It's a flag set by `edgesCheck.toggled` via `DirectConnection`, like Grayscale. Edges replaces
Grayscale, so the UI disables the Grayscale box while Edges is on.

## 2. Recording, inside the worker thread
- The GUI only sets `worker.record_path = "…mp4"` (start) or `None` (stop).
- The **worker** opens `cv2.VideoWriter` on the next frame, since only there does it know the frame size, and
  it writes every processed frame.
- `VideoWriter` needs 3-channel frames of a fixed size → grayscale/edges frames are converted with
  `COLOR_GRAY2BGR` before writing.
- `writer.release()` **finalizes the file**. It's called on stop, and also in `run()`'s `finally`, so closing
  the window mid-recording still gives a playable `.mp4`.
- `recording_changed(bool, str)` tells the GUI when the file is actually open (or when it failed).

Why not write the video from the GUI thread in `show_frame()`? Encoding costs a few ms per frame, which
would stutter the UI, and frames could be dropped or reordered on their way through the event queue.

## 3. Bonus: face detection with YuNet
> ⚠️ **OpenCV 5 removed `cv2.CascadeClassifier`** (and the bundled Haar XML files), so the classic
> tutorial code no longer works. The replacement is the DNN face detector `cv2.FaceDetectorYN`.

```python
detector = cv2.FaceDetectorYN.create("models/face_detection_yunet_2023mar.onnx", "", (w, h), 0.8)
detector.setInputSize((w, h))
_, faces = detector.detect(frame)       # N×15 array: x, y, w, h, 5 landmarks, score
for f in faces if faces is not None else []:
    x, y, fw, fh = f[:4].astype(int)
    cv2.rectangle(frame, (x, y), (x + fw, y + fh), (0, 200, 0), 2)
```
- The model (`models/face_detection_yunet_2023mar.onnx`, 227 KB) is from
  [opencv_zoo](https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet) (MIT license).
- The detector is created **lazily inside the worker thread**, the first time Faces is enabled.
- Faces are drawn *before* edges/grayscale, so the boxes show up in every mode and in recordings.
- You'll see a `[ WARN ] … Targets are not supported by the new graph engine` log line from OpenCV 5. It's harmless.

## Review checklist
- [ ] All OpenCV work (Canny, detection, VideoWriter) happens in the worker, and only QImages cross threads
- [ ] The video file is released on stop **and** on window close
- [ ] Grayscale/edges frames are converted to BGR before `VideoWriter.write`
- [ ] No `QPixmap` created in the worker
