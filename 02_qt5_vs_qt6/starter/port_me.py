"""Exercise 02: port this Qt5 (PySide2) snippet to PySide6.

It does NOT run as-is (PySide2 isn't installed). Your job is to make it run with PySide6:
    python 02_qt5_vs_qt6/starter/port_me.py

There are 5 things to fix. Look for the TODO markers.
"""
import sys

from PySide2.QtCore import Qt  # TODO(exercise): which package?
from PySide2.QtWidgets import QAction, QApplication, QDesktopWidget, QLabel  # TODO(exercise): two of these moved or were removed

app = QApplication(sys.argv)

label = QLabel("hi")
label.setAlignment(Qt.AlignCenter)  # TODO(exercise): Qt6 enum style

width = QDesktopWidget().screenGeometry().width()  # TODO(exercise): QDesktopWidget is gone in Qt6
label.setText(f"hi, your screen is {width}px wide")

quit_action = QAction("Quit", label)
quit_action.setShortcut("Ctrl+Q")
quit_action.triggered.connect(app.quit)
label.addAction(quit_action)

label.resize(300, 100)
label.show()
sys.exit(app.exec_())  # TODO(exercise): Qt6 name
