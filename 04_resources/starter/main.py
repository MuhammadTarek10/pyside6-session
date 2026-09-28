"""Starter for exercise 4: Rotate + Dark mode (see README.md in this folder).

Regenerate after editing main_window.ui or resources.qrc:
    pyside6-rcc resources.qrc -o resources_rc.py
    pyside6-uic main_window.ui -o ui_main_window.py
"""
import sys

from PySide6.QtCore import QFile, QTextStream, Qt, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox

import resources_rc  # noqa: F401  (registers the ":/..." files with Qt; ui_main_window imports it too)
from ui_main_window import Ui_ImageViewer

ZOOM_STEP = 1.25


def load_stylesheet(path: str) -> str:
    """Read a text file. `path` can be a real path or a resource path like ':/styles/style.qss'."""
    file = QFile(path)
    if not file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        return ""
    return QTextStream(file).readAll()


class ImageViewer(QMainWindow, Ui_ImageViewer):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self._pixmap = QPixmap(":/images/logo.svg")  # the resource logo is the default image
        self._scale = 1.0

        self.actionOpen.triggered.connect(self.open_image)
        self.actionZoomIn.triggered.connect(self.zoom_in)
        self.actionZoomOut.triggered.connect(self.zoom_out)
        self.actionFit.triggered.connect(self.fit_to_window)
        self.actionAbout.triggered.connect(self.about)
        # actionQuit -> close() is connected in Designer

        # TODO(exercise 1): after adding actionRotate in Designer + rebuilding, connect it to self.rotate
        # TODO(exercise 2): after adding a CHECKABLE actionDarkMode, connect its toggled(bool) to self.set_dark_mode

        self._render()

    @Slot()
    def open_image(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Open image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif *.svg)"
        )
        if not path:
            return
        pixmap = QPixmap(path)
        if pixmap.isNull():
            QMessageBox.warning(self, "Open image", f"Could not load:\n{path}")
            return
        self._pixmap = pixmap
        self._scale = 1.0
        self._render()
        self.statusbar.showMessage(f"Opened {path}", 3000)

    @Slot()
    def zoom_in(self) -> None:
        self._scale *= ZOOM_STEP
        self._render()

    @Slot()
    def zoom_out(self) -> None:
        self._scale /= ZOOM_STEP
        self._render()

    @Slot()
    def fit_to_window(self) -> None:
        viewport = self.scrollArea.viewport().size()
        self._scale = min(
            viewport.width() / self._pixmap.width(),
            viewport.height() / self._pixmap.height(),
        )
        self._render()

    @Slot()
    def rotate(self) -> None:
        # TODO(exercise 1): rotate self._pixmap by 90° and re-render.
        # Hint: QPixmap.transformed(QTransform().rotate(90), ...), then self._render()
        raise NotImplementedError

    @Slot(bool)
    def set_dark_mode(self, on: bool) -> None:
        # TODO(exercise 2): apply ":/styles/dark.qss" when on, ":/styles/style.qss" when off.
        # Hint: QApplication.instance().setStyleSheet(load_stylesheet(...))
        raise NotImplementedError

    @Slot()
    def about(self) -> None:
        QMessageBox.about(
            self,
            "About",
            "Image Viewer\n\nIcons, logo and stylesheet are embedded via resources.qrc.",
        )

    def _render(self) -> None:
        scaled = self._pixmap.scaled(
            self._pixmap.size() * self._scale,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.imageLabel.setPixmap(scaled)
        self.imageLabel.resize(scaled.size())
        self.statusbar.showMessage(
            f"{self._pixmap.width()}×{self._pixmap.height()}  |  zoom {self._scale:.0%}"
        )


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet(":/styles/style.qss"))  # applies to the whole app
    window = ImageViewer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
