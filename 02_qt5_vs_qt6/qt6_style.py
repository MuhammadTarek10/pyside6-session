"""The same app in modern Qt6 style (PySide6). Compare with qt5_style.py."""
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction  # Qt6: QAction moved to QtGui
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

# Qt6: High-DPI is always on, so there's nothing to set here


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Qt6 style")

        label = QLabel("Hello from Qt6")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Qt6: fully-qualified enum
        self.setCentralWidget(label)

        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        self.menuBar().addMenu("File").addAction(quit_action)

        # Qt6: QDesktopWidget is gone, so use QScreen
        screen = QApplication.primaryScreen().availableGeometry()
        self.resize(screen.width() // 3, screen.height() // 3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())  # Qt6: exec()
