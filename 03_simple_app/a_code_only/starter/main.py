"""Starter for exercise 3a: add a greeting combo box (see README.md in this folder)."""
import sys

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Greeter(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Greeter (starter)")

        # TODO(exercise 1): create self.greeting_combo = QComboBox() with the items
        #                  "Hello", "Hi", "Welcome"  (don't forget the import)

        # 1. Create widgets
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Your name")
        self.greet_button = QPushButton("Greet")
        self.clear_button = QPushButton("Clear")
        self.result_label = QLabel("Type a name and press Greet")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 2. Arrange them with layouts (never hard-code x/y positions)
        buttons = QHBoxLayout()
        buttons.addWidget(self.greet_button)
        buttons.addWidget(self.clear_button)

        # TODO(exercise 1): put the combo and the name field side by side (a QHBoxLayout)
        layout = QVBoxLayout(self)  # passing `self` installs the layout on this widget
        layout.addWidget(self.name_edit)
        layout.addLayout(buttons)
        layout.addWidget(self.result_label)

        # 3. Connect signals (events) to slots (handlers)
        self.greet_button.clicked.connect(self.greet)
        self.name_edit.returnPressed.connect(self.greet)  # Enter key does the same
        self.clear_button.clicked.connect(self.clear)
        self.name_edit.textChanged.connect(self.update_greet_button)
        # TODO(exercise 1, optional): re-greet when the combo selection changes

        self.update_greet_button("")  # set the initial button state

    @Slot()
    def greet(self) -> None:
        name = self.name_edit.text().strip()
        if name:
            # TODO(exercise 1): use the greeting selected in the combo instead of "Hello"
            self.result_label.setText(f"Hello, {name}! 👋")

    @Slot()
    def clear(self) -> None:
        self.name_edit.clear()
        self.result_label.setText("Type a name and press Greet")
        self.name_edit.setFocus()

    @Slot(str)
    def update_greet_button(self, text: str) -> None:
        # signals can carry data: textChanged(str) passes the new text
        self.greet_button.setEnabled(bool(text.strip()))
        # TODO(bonus): disable the Clear button when the field is empty


def main() -> None:
    app = QApplication(sys.argv)  # exactly one per process, created first
    window = Greeter()
    window.resize(320, 140)
    window.show()  # widgets are hidden until shown
    sys.exit(app.exec())  # start the event loop, which blocks until the last window closes


if __name__ == "__main__":
    main()
