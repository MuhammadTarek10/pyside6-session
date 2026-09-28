"""Starter for exercise 7: Edges, Record, Faces (see README.md in this folder).

Regenerate after editing main_window.ui:  pyside6-uic main_window.ui -o ui_main_window.py
"""
import sys
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QThread, Qt, Slot
from PySide6.QtGui import QCloseEvent, QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

from camera_worker import CameraWorker
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
        # TODO(exercise 2): after adding a CHECKABLE recordButton in Designer, connect its toggled(bool)
        #                   to a slot that sets worker.record_path to CAPTURES_DIR / "video_<timestamp>.mp4"
        #                   (or to None to stop)
        self.statusbar.showMessage("Press Start")

    # ---- camera lifecycle (same pattern as 06b) --------------------------------
    @Slot()
    def start_camera(self) -> None:
        self.thread = QThread()
        self.worker = CameraWorker(self.cameraSpin.value())
        self.worker.grayscale = self.grayCheck.isChecked()
        self.worker.mirror = self.mirrorCheck.isChecked()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.frame_ready.connect(self.show_frame)
        self.worker.fps_changed.connect(lambda fps: self.statusbar.showMessage(f"{fps:.1f} FPS"))
        self.worker.error.connect(self.show_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.handle_camera_stopped)

        # The worker's thread is stuck inside run()'s while-loop, so it never gets back to its
        # event loop. A normal (queued) connection to a worker slot would NEVER be delivered.
        # DirectConnection calls the slot right away in the GUI thread; it only sets a bool.
        self.grayCheck.toggled.connect(self.worker.set_grayscale, Qt.ConnectionType.DirectConnection)
        self.mirrorCheck.toggled.connect(self.worker.set_mirror, Qt.ConnectionType.DirectConnection)
        # TODO(exercise 1): after adding edgesCheck in Designer, connect it to worker.set_edges the same way
        # TODO(bonus):      facesCheck → worker.set_faces

        self.startButton.setEnabled(False)
        self.cameraSpin.setEnabled(False)
        self.stopButton.setEnabled(True)
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
        self.videoLabel.setText("Camera stopped")  # setText clears the pixmap
        self.statusbar.showMessage("Stopped")

    # ---- frames arrive here, on the GUI thread ----------------------------------
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
            self.thread.wait()  # release the camera before the app exits
        super().closeEvent(event)


def main() -> None:
    app = QApplication(sys.argv)
    window = CameraWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
