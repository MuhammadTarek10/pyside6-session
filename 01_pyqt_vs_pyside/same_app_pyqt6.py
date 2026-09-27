"""The same tiny counter app, written for PyQt6 (compare with same_app_pyside6.py).

NOTE: PyQt6 is NOT installed in this session. This file is for reading and diffing only.
"""
import sys

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


class Counter(QObject):
    changed = pyqtSignal(int)  # PySide6: Signal(int)

    def __init__(self) -> None:
        super().__init__()
        self._value = 0

    @pyqtSlot()  # PySide6: @Slot()
    def increment(self) -> None:
        self._value += 1
        self.changed.emit(self._value)


def main() -> None:
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("PyQt6 counter")
    label = QLabel("0")
    button = QPushButton("+1")

    layout = QVBoxLayout(window)
    layout.addWidget(label)
    layout.addWidget(button)

    counter = Counter()
    button.clicked.connect(counter.increment)
    counter.changed.connect(lambda v: label.setText(str(v)))

    window.resize(240, 100)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
