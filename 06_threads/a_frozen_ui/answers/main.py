"""Answer for 6a: the same 5-step task driven by a QTimer, with no threads and no sleep."""
import sys

from PySide6.QtCore import QTimer, Slot
from PySide6.QtWidgets import QApplication, QLabel, QProgressBar, QPushButton, QVBoxLayout, QWidget

SPINNER = "◐◓◑◒"


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("6a answer: QTimer steps")

        self.alive_label = QLabel()
        self.progress = QProgressBar()
        self.run_button = QPushButton("Run 5-second task (QTimer steps)")
        self.status = QLabel("Idle")

        layout = QVBoxLayout(self)
        for w in (self.alive_label, self.progress, self.run_button, self.status):
            layout.addWidget(w)

        self._tick = 0
        spinner = QTimer(self, interval=100)
        spinner.timeout.connect(self.animate)
        spinner.start()

        # One step per second. Between steps, control returns to the event loop.
        self.step_timer = QTimer(self, interval=1000)
        self.step_timer.timeout.connect(self.step)
        self._step = 0

        self.run_button.clicked.connect(self.run_task)

    @Slot()
    def animate(self) -> None:
        self._tick += 1
        self.alive_label.setText(f"UI alive {SPINNER[self._tick % 4]}   ticks: {self._tick}")

    @Slot()
    def run_task(self) -> None:
        self._step = 0
        self.progress.setValue(0)
        self.status.setText("Working…")  # visible now: we return right away, so it gets painted
        self.run_button.setEnabled(False)  # prevent starting twice
        self.step_timer.start()

    @Slot()
    def step(self) -> None:
        # each call is short (a few microseconds), so the loop is never blocked
        self._step += 1
        self.progress.setValue(self._step * 20)
        if self._step == 5:
            self.step_timer.stop()
            self.status.setText("Done!")
            self.run_button.setEnabled(True)


def main() -> None:
    app = QApplication(sys.argv)
    window = Window()
    window.resize(380, 150)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
