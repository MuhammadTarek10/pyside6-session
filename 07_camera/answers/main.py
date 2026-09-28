"""Answer for topic 7: camera preview + Edges, Faces and Record.

Regenerate after editing main_window.ui:  pyside6-uic main_window.ui -o ui_main_window.py
"""
import sys
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QThread, Qt, Slot
from PySide6.QtGui import QCloseEvent, QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

from camera_worker import FACE_MODEL, CameraWorker
from ui_main_window import Ui_CameraWindow

CAPTURES_DIR = Path(__file__).with_name("captures")


class CameraWindow(QMainWindow, Ui_CameraWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.thread: QThread | None = None
        self.worker: CameraWorker | None = None
        self.last_frame: QImage | None = None

        self.startButton.clicked.connect(self.start_camera)
        self.stopButton.clicked.connect(self.stop_camera)
        self.snapshotButton.clicked.connect(self.take_snapshot)
        self.recordButton.toggled.connect(self.toggle_recording)
        # Edges replaces Grayscale, so the two are mutually exclusive in the UI
        self.edgesCheck.toggled.connect(lambda on: self.grayCheck.setEnabled(not on))
        if not FACE_MODEL.exists():
            self.facesCheck.setEnabled(False)
            self.facesCheck.setToolTip(f"Model not found: {FACE_MODEL}")
        self.statusbar.showMessage("Press Start")

    # ---- camera lifecycle --------------------------------------------------------
    @Slot()
    def start_camera(self) -> None:
        self.thread = QThread()
        self.worker = CameraWorker(self.cameraSpin.value())
        self.worker.grayscale = self.grayCheck.isChecked()
        self.worker.mirror = self.mirrorCheck.isChecked()
        self.worker.edges = self.edgesCheck.isChecked()
        self.worker.faces = self.facesCheck.isChecked()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.frame_ready.connect(self.show_frame)
        self.worker.fps_changed.connect(self.show_fps)
        self.worker.recording_changed.connect(self.show_recording_state)
        self.worker.error.connect(self.show_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.handle_camera_stopped)

        direct = Qt.ConnectionType.DirectConnection  # see ../README.md: the worker loop never idles
        self.grayCheck.toggled.connect(self.worker.set_grayscale, direct)
        self.mirrorCheck.toggled.connect(self.worker.set_mirror, direct)
        self.edgesCheck.toggled.connect(self.worker.set_edges, direct)
        self.facesCheck.toggled.connect(self.worker.set_faces, direct)

        self.startButton.setEnabled(False)
        self.cameraSpin.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.recordButton.setEnabled(True)
        self.statusbar.showMessage("Opening camera…")
        self.thread.start()

    @Slot()
    def stop_camera(self) -> None:
        if self.thread:
            self.thread.requestInterruption()
            self.stopButton.setEnabled(False)

    @Slot()
    def handle_camera_stopped(self) -> None:
        self.thread = None
        self.worker = None
        self.startButton.setEnabled(True)
        self.cameraSpin.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.snapshotButton.setEnabled(False)
        self.recordButton.setChecked(False)
        self.recordButton.setEnabled(False)
        self.videoLabel.setText("Camera stopped")
        self.statusbar.showMessage("Stopped")

    # ---- recording (EXERCISE 2) --------------------------------------------------
    @Slot(bool)
    def toggle_recording(self, on: bool) -> None:
        if not self.worker:
            return
        if on:
            CAPTURES_DIR.mkdir(exist_ok=True)
            path = CAPTURES_DIR / f"video_{datetime.now():%Y%m%d_%H%M%S}.mp4"
            self.worker.record_path = str(path)  # the worker opens the VideoWriter in its thread
        else:
            self.worker.record_path = None  # the worker releases it on the next frame

    @Slot(bool, str)
    def show_recording_state(self, recording: bool, path: str) -> None:
        self.recordButton.setText("⏹ Stop recording" if recording else "⏺ Record")
        if recording:
            self.statusbar.showMessage(f"Recording to {Path(path).name}")
        else:
            self.recordButton.setChecked(False)  # e.g. the writer failed to open
            self.statusbar.showMessage("Recording saved", 3000)

    # ---- frames ------------------------------------------------------------------
    @Slot(QImage)
    def show_frame(self, image: QImage) -> None:
        self.last_frame = image
        self.snapshotButton.setEnabled(True)
        pixmap = QPixmap.fromImage(image).scaled(
            self.videoLabel.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.videoLabel.setPixmap(pixmap)

    @Slot(float)
    def show_fps(self, fps: float) -> None:
        if not self.recordButton.isChecked():
            self.statusbar.showMessage(f"{fps:.1f} FPS")

    @Slot(str)
    def show_error(self, message: str) -> None:
        QMessageBox.warning(self, "Camera", message)

    @Slot()
    def take_snapshot(self) -> None:
        if self.last_frame is None:
            return
        CAPTURES_DIR.mkdir(exist_ok=True)
        path = CAPTURES_DIR / f"snapshot_{datetime.now():%Y%m%d_%H%M%S}.png"
        if self.last_frame.save(str(path)):
            self.statusbar.showMessage(f"Saved {path.name}", 3000)
        else:
            self.show_error(f"Could not save {path}")

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.thread:
            self.thread.requestInterruption()
            self.thread.quit()
            self.thread.wait()  # the worker's finally: closes the video file + releases the camera
        super().closeEvent(event)


def main() -> None:
    app = QApplication(sys.argv)
    window = CameraWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
