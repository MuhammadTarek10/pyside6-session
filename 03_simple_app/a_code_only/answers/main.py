"""Answer for 3a: a greeting combo box + Clear disabled when the field is empty."""
import sys

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
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
        self.setWindowTitle("Greeter (answer)")

        self.greeting_combo = QComboBox()  # NEW
        self.greeting_combo.addItems(["Hello", "Hi", "Welcome"])
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Your name")
        self.greet_button = QPushButton("Greet")
        self.clear_button = QPushButton("Clear")
        self.result_label = QLabel("Type a name and press Greet")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        row = QHBoxLayout()  # combo + name side by side
        row.addWidget(self.greeting_combo)
        row.addWidget(self.name_edit, stretch=1)

        buttons = QHBoxLayout()
        buttons.addWidget(self.greet_button)
        buttons.addWidget(self.clear_button)

        layout = QVBoxLayout(self)
        layout.addLayout(row)
        layout.addLayout(buttons)
        layout.addWidget(self.result_label)

        self.greet_button.clicked.connect(self.greet)
        self.name_edit.returnPressed.connect(self.greet)
        self.clear_button.clicked.connect(self.clear)
        self.name_edit.textChanged.connect(self.update_buttons)
        # re-greet live when the greeting changes (only if we already greeted someone)
        self.greeting_combo.currentTextChanged.connect(self.greet)

        self.update_buttons("")

    @Slot()
    def greet(self) -> None:
        name = self.name_edit.text().strip()
        if name:
            greeting = self.greeting_combo.currentText()
            self.result_label.setText(f"{greeting}, {name}! 👋")

    @Slot()
    def clear(self) -> None:
        self.name_edit.clear()
        self.result_label.setText("Type a name and press Greet")
        self.name_edit.setFocus()

    @Slot(str)
    def update_buttons(self, text: str) -> None:
        has_text = bool(text.strip())
        self.greet_button.setEnabled(has_text)
        self.clear_button.setEnabled(bool(text))  # BONUS: nothing to clear → disabled


def main() -> None:
    app = QApplication(sys.argv)
    window = Greeter()
    window.resize(360, 140)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
