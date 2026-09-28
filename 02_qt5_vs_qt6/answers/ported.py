"""Answer for topic 2: the Qt5 snippet ported to PySide6."""
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction  # Qt6: QAction lives in QtGui
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)

label = QLabel("hi")
label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Qt6: fully-qualified enum

width = app.primaryScreen().geometry().width()  # Qt6: QScreen replaces QDesktopWidget
label.setText(f"hi, your screen is {width}px wide")

quit_action = QAction("Quit", label, shortcut="Ctrl+Q", triggered=app.quit)
label.addAction(quit_action)  # Ctrl+Q works while the label has focus

label.resize(300, 100)
label.show()
sys.exit(app.exec())  # Qt6: exec()
