"""The same tiny counter app, written for PySide6 (compare with same_app_pyqt6.py)."""
import sys

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


class Counter(QObject):
    changed = Signal(int)  # PyQt6: pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self._value = 0

    @Slot()  # PyQt6: @pyqtSlot()
    def increment(self) -> None:
        self._value += 1
        self.changed.emit(self._value)


def main() -> None:
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("PySide6 counter")
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
