"""Starter for exercise 3b: a "Shout" checkbox (see README.md in this folder).

Step 1 is in Designer: pyside6-designer greeter.ui

Regenerate the Python UI module after editing greeter.ui:
    pyside6-uic greeter.ui -o ui_greeter.py
"""
import sys

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QWidget

from ui_greeter import Ui_Greeter  # generated, never edit by hand


class Greeter(QWidget, Ui_Greeter):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)  # creates nameEdit, greetButton, ... as attributes of self

        # Only *behavior* lives here. Layout and look live in the .ui file.
        self.greetButton.clicked.connect(self.greet)
        self.clearButton.clicked.connect(self.clear)
        self.nameEdit.textChanged.connect(self.update_greet_button)
        # nameEdit.returnPressed -> greetButton.click() is wired in Designer (Signal/Slot editor)

        # TODO(exercise): after adding the checkbox in Designer (objectName: shoutCheck) and
        #                 rerunning pyside6-uic, connect shoutCheck.toggled to self.greet

        self.update_greet_button("")

    @Slot()
    def greet(self) -> None:
        name = self.nameEdit.text().strip()
        if name:
            message = f"Hello, {name}! 👋"
            # TODO(exercise): if self.shoutCheck is checked, make the message upper-case
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
