"""Answer for 3b: a "Shout" checkbox added in Designer (answers/greeter.ui).

Regenerate:  pyside6-uic greeter.ui -o ui_greeter.py   (or ./build.sh 03_simple_app)
"""
import sys

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QWidget

from ui_greeter import Ui_Greeter


class Greeter(QWidget, Ui_Greeter):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.greetButton.clicked.connect(self.greet)
        self.clearButton.clicked.connect(self.clear)
        self.nameEdit.textChanged.connect(self.update_greet_button)
        self.shoutCheck.toggled.connect(self.greet)  # NEW: re-render when toggled

        self.update_greet_button("")

    @Slot()
    def greet(self) -> None:
        name = self.nameEdit.text().strip()
        if not name:
            return
        message = f"Hello, {name}! 👋"
        if self.shoutCheck.isChecked():  # NEW
            message = message.upper()
        self.resultLabel.setText(message)

    @Slot()
    def clear(self) -> None:
        self.nameEdit.clear()
        self.resultLabel.setText("Type a name and press Greet")
        self.nameEdit.setFocus()

    @Slot(str)
    def update_greet_button(self, text: str) -> None:
        self.greetButton.setEnabled(bool(text.strip()))


def main() -> None:
    app = QApplication(sys.argv)
    window = Greeter()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
