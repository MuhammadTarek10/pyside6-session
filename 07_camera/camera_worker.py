"""OpenCV capture loop running in a worker thread (the pattern from topic 6b)."""
import time

import cv2
import numpy as np
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtGui import QImage


def to_qimage(frame: np.ndarray, grayscale: bool = False, mirror: bool = False) -> QImage:
    """Convert an OpenCV BGR frame (numpy array) into a QImage that owns its own memory."""
    if mirror:
        frame = cv2.flip(frame, 1)  # 1 = horizontal flip
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
                self.frame_ready.emit(to_qimage(frame, self.grayscale, self.mirror))

                frames += 1
                now = time.perf_counter()
                if now - last >= 1.0:
                    self.fps_changed.emit(frames / (now - last))
                    frames, last = 0, now
        finally:
            capture.release()  # always free the device, or the next open fails
            self.finished.emit()
