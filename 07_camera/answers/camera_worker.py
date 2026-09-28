"""Answer for topic 7: capture loop with Edges, face detection and recording."""
import time
from pathlib import Path

import cv2
import numpy as np
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtGui import QImage

FACE_MODEL = Path(__file__).with_name("models") / "face_detection_yunet_2023mar.onnx"


def to_qimage(frame: np.ndarray) -> QImage:
    """BGR (3 channels) or grayscale (2D) numpy array → QImage that owns its memory."""
    if frame.ndim == 2:
        h, w = frame.shape
        return QImage(frame.data, w, h, frame.strides[0], QImage.Format.Format_Grayscale8).copy()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, _ = rgb.shape
    return QImage(rgb.data, w, h, rgb.strides[0], QImage.Format.Format_RGB888).copy()


class CameraWorker(QObject):
    frame_ready = Signal(QImage)
    fps_changed = Signal(float)
    recording_changed = Signal(bool, str)  # is_recording, file path
    error = Signal(str)
    finished = Signal()

    def __init__(self, camera_index: int = 0) -> None:
        super().__init__()
        self.camera_index = camera_index
        # flags written from the GUI thread (DirectConnection), read by the loop
        self.grayscale = False
        self.mirror = True
        self.edges = False  # EXERCISE 1
        self.faces = False  # EXERCISE 3
        self.record_path: str | None = None  # EXERCISE 2: set → start, None → stop

        self._face_detector = None
        self._writer: cv2.VideoWriter | None = None

    # ---- setters (called directly from the GUI thread) --------------------------
    @Slot(bool)
    def set_grayscale(self, on: bool) -> None:
        self.grayscale = on

    @Slot(bool)
    def set_mirror(self, on: bool) -> None:
        self.mirror = on

    @Slot(bool)
    def set_edges(self, on: bool) -> None:
        self.edges = on

    @Slot(bool)
    def set_faces(self, on: bool) -> None:
        self.faces = on

    # ---- processing (runs in the worker thread) ---------------------------------
    def process(self, frame: np.ndarray) -> np.ndarray:
        if self.mirror:
            frame = cv2.flip(frame, 1)
        if self.faces:
            self.draw_faces(frame)
        if self.edges:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return cv2.Canny(gray, 100, 200)  # 2D array: white edges on black
        if self.grayscale:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame

    def draw_faces(self, frame: np.ndarray) -> None:
        h, w = frame.shape[:2]
        if self._face_detector is None:  # created lazily, in THIS thread
            self._face_detector = cv2.FaceDetectorYN.create(str(FACE_MODEL), "", (w, h), 0.8)
        self._face_detector.setInputSize((w, h))
        _, faces = self._face_detector.detect(frame)
        for face in faces if faces is not None else []:
            x, y, fw, fh = face[:4].astype(int)
            cv2.rectangle(frame, (x, y), (x + fw, y + fh), (0, 200, 0), 2)
            cv2.putText(frame, f"{face[-1]:.2f}", (x, y - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 0), 1)

    def update_recording(self, frame: np.ndarray, fps: float) -> None:
        """Open/close/write the VideoWriter. Everything happens in the worker thread."""
        if self.record_path and self._writer is None:
            h, w = frame.shape[:2]
            self._writer = cv2.VideoWriter(self.record_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
            if not self._writer.isOpened():
                self._writer = None
                self.error.emit(f"Cannot write video to {self.record_path}")
                self.record_path = None
                return
            self.recording_changed.emit(True, self.record_path)
        elif not self.record_path and self._writer is not None:
            self.stop_writer()

        if self._writer is not None:
            # VideoWriter expects 3-channel BGR at the size it was opened with
            self._writer.write(cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR) if frame.ndim == 2 else frame)

    def stop_writer(self) -> None:
        if self._writer is not None:
            self._writer.release()  # finalizes the file; without this the .mp4 is unplayable
            self._writer = None
            self.recording_changed.emit(False, "")

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

        camera_fps = capture.get(cv2.CAP_PROP_FPS) or 30.0
        thread = QThread.currentThread()
        frames, last = 0, time.perf_counter()
        try:
            while not thread.isInterruptionRequested():
                ok, frame = capture.read()
                if not ok:
                    self.error.emit("Camera stopped sending frames.")
                    break
                processed = self.process(frame)
                self.update_recording(processed, camera_fps)
                self.frame_ready.emit(to_qimage(processed))

                frames += 1
                now = time.perf_counter()
                if now - last >= 1.0:
                    self.fps_changed.emit(frames / (now - last))
                    frames, last = 0, now
        finally:
            self.stop_writer()
            capture.release()
            self.finished.emit()
