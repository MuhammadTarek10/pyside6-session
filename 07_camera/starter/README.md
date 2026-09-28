# 07 — Starter

A copy of the camera app with `TODO(exercise)` markers in `camera_worker.py` and `main.py`. It runs as-is:
```bash
./build.sh 07_camera
python 07_camera/starter/main.py
```

## Exercise 1: Edges
1. **Designer** (`starter/main_window.ui`): add a `QCheckBox` **`edgesCheck`** ("Edges") next to Grayscale. Rebuild.
2. Worker: an `edges` flag + `set_edges` slot, and the Canny branch in the processing.
3. Window: connect `edgesCheck.toggled` → `worker.set_edges` with `DirectConnection` (why? see `../README.md`).

## Exercise 2: Record
1. **Designer:** a `QPushButton` **`recordButton`** ("⏺ Record"), **checkable = true**, disabled by default. Rebuild.
2. Window: on toggle, set `worker.record_path` (a path under `captures/`) or `None`. Enable the button while the camera runs.
3. Worker: create, write to and release the `cv2.VideoWriter` **inside the worker thread**.

## Bonus: Faces
1. **Designer:** a `QCheckBox` **`facesCheck`** ("Faces"). Rebuild.
2. Worker: `cv2.FaceDetectorYN` with the model at `FACE_MODEL` (already defined in `camera_worker.py`),
   drawing a rectangle per face with `cv2.rectangle`.
   `detect(frame)` returns `(ok, faces)`, where each row is `x, y, w, h, …, score`, and `faces` may be `None`.

No camera handy? Test the processing on a still image: `frame = cv2.imread("photo.jpg")`.

Check your work: compare with `../answers/` (`camera_worker.py`, `main.py`, `main_window.ui`).
