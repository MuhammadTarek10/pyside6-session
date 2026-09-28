"""Starter for exercise 7: Edges, Record, Faces (see README.md in this folder)."""
import time
from pathlib import Path

import cv2
import numpy as np
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtGui import QImage


# Bonus: the YuNet face model ships with the answer
FACE_MODEL = Path(__file__).parent.parent / "answers" / "models" / "face_detection_yunet_2023mar.onnx"


def to_qimage(frame: np.ndarray, grayscale: bool = False, mirror: bool = False) -> QImage:
    """Convert an OpenCV BGR frame (numpy array) into a QImage that owns its own memory."""
    if mirror:
        frame = cv2.flip(frame, 1)  # 1 = horizontal flip
    # TODO(exercise 1): an `edges` mode. cv2.Canny(gray, 100, 200) returns a 2D grayscale image
    #                  → display it with Format_Grayscale8, just like the grayscale branch
    if grayscale:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        image = QImage(gray.data, w, h, gray.strides[0], QImage.Format.Format_Grayscale8)
    else:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV is BGR, Qt expects RGB
        h, w, _ = rgb.shape
        image = QImage(rgb.data, w, h, rgb.strides[0], QImage.Format.Format_RGB888)
    # QImage(data, ...) only *borrows* the numpy buffer, which is freed when this function
    # returns. .copy() gives the QImage its own memory, so it's safe to send to another thread.
    return image.copy()


class CameraWorker(QObject):
    frame_ready = Signal(QImage)
    fps_changed = Signal(float)
    error = Signal(str)
    finished = Signal()

    def __init__(self, camera_index: int = 0) -> None:
        super().__init__()
        self.camera_index = camera_index
        # Written from the GUI thread, read in the loop. Plain bools are fine here.
        self.grayscale = False
        self.mirror = True
        # TODO(exercise 1): self.edges = False  (+ a set_edges slot like set_grayscale)
        # TODO(exercise 2): self.record_path: str | None = None and self._writer = None
        # TODO(bonus):      self.faces = False, and the detector created lazily in this thread:
        #                   cv2.FaceDetectorYN.create(str(FACE_MODEL), "", (w, h), 0.8)
        #                   NOTE: cv2.CascadeClassifier no longer exists in OpenCV 5!

    @Slot(bool)
    def set_grayscale(self, on: bool) -> None:
        self.grayscale = on

    @Slot(bool)
    def set_mirror(self, on: bool) -> None:
        self.mirror = on

    @Slot()
    def run(self) -> None:
        capture = cv2.VideoCapture(self.camera_index)
        if not capture.isOpened():
            self.error.emit(
                f"Cannot open camera {self.camera_index}. "
                "Is it in use, or is camera permission missing?"
            )
            self.finished.emit()
            return

        thread = QThread.currentThread()
        frames, last = 0, time.perf_counter()
        try:
            while not thread.isInterruptionRequested():
                ok, frame = capture.read()  # blocks until the next frame (~33 ms at 30 fps)
                if not ok:
                    self.error.emit("Camera stopped sending frames.")
                    break
                # TODO(exercise 2): if recording, write the frame with a cv2.VideoWriter created HERE
                #                   (worker thread), e.g. cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
                #                   It needs 3-channel BGR frames. Release it when record_path becomes None.
                # TODO(bonus): detect faces and draw rectangles on `frame` before converting
                self.frame_ready.emit(to_qimage(frame, self.grayscale, self.mirror))

                frames += 1
                now = time.perf_counter()
                if now - last >= 1.0:
                    self.fps_changed.emit(frames / (now - last))
                    frames, last = 0, now
        finally:
            # TODO(exercise 2): release the VideoWriter too, or the .mp4 file is unplayable
            capture.release()  # always free the device, or the next open fails
            self.finished.emit()
