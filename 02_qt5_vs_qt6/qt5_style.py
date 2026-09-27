"""Qt5-era style (PySide2). READ-ONLY: PySide2 does not install on Python 3.14.

Every line marked `# Qt5:` is something that changes in Qt6. Compare with qt6_style.py.
"""
import sys

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (  # Qt5: QAction lives in QtWidgets
    QAction,
    QApplication,
    QDesktopWidget,
    QLabel,
    QMainWindow,
)

# Qt5: High-DPI must be opted into, before QApplication is created
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt5 style")

        label = QLabel("Hello from Qt5")
        label.setAlignment(Qt.AlignCenter)  # Qt5: short enum name
        self.setCentralWidget(label)

        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        self.menuBar().addMenu("File").addAction(quit_action)

        # Qt5: QDesktopWidget for screen size
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() // 3, screen.height() // 3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())  # Qt5: exec_()
