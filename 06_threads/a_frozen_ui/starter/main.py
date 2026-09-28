"""Starter for exercise 6a: replace the sleep loop with a QTimer (see README.md in this folder)."""
import sys
import time

from PySide6.QtCore import QTimer, Slot
from PySide6.QtWidgets import QApplication, QLabel, QProgressBar, QPushButton, QVBoxLayout, QWidget

SPINNER = "◐◓◑◒"


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("6a starter")

        self.alive_label = QLabel()  # animated by a timer, so it stops when the UI freezes
        self.progress = QProgressBar()
        self.run_button = QPushButton("Run 5-second task (on the GUI thread)")
        self.status = QLabel("Idle")

        layout = QVBoxLayout(self)
        for w in (self.alive_label, self.progress, self.run_button, self.status):
            layout.addWidget(w)

        self._tick = 0
        timer = QTimer(self, interval=100)
        timer.timeout.connect(self.animate)
        timer.start()

        self.run_button.clicked.connect(self.run_task)

        # TODO(exercise): create self.step_timer = QTimer(self, interval=1000)
        #                 connect its timeout to self.step, and keep a step counter (self._step = 0)

    @Slot()
    def animate(self) -> None:
        self._tick += 1
        self.alive_label.setText(f"UI alive {SPINNER[self._tick % 4]}   ticks: {self._tick}")

    @Slot()
    def step(self) -> None:
        # TODO(exercise): do ONE step: advance the counter, set the progress (20% per step),
        #                 and after step 5 stop the timer, show "Done!" and re-enable the button
        pass

    @Slot()
    def run_task(self) -> None:
        # TODO(exercise): delete the for-loop below. Instead reset the counter and progress,
        #                 disable the button and start self.step_timer. Then return right away!
        self.status.setText("Working…")  # you won't even see this text: no repaint happens
        for i in range(1, 6):
            time.sleep(1)  # pretend: network call, file processing, heavy math…
            self.progress.setValue(i * 20)  # updates are queued but never painted
        self.status.setText("Done!")
        # While this method runs, the event loop is blocked: no repaint, no clicks, no timer.
        # macOS shows the beach ball; Windows says "(Not Responding)".


def main() -> None:
    app = QApplication(sys.argv)
    window = Window()
    window.resize(380, 150)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
