"""Topic 6a: the WRONG way. Long work on the GUI thread freezes the whole window."""
import sys
import time

from PySide6.QtCore import QTimer, Slot
from PySide6.QtWidgets import QApplication, QLabel, QProgressBar, QPushButton, QVBoxLayout, QWidget

SPINNER = "◐◓◑◒"


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("6a: frozen UI")

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

    @Slot()
    def animate(self) -> None:
        self._tick += 1
        self.alive_label.setText(f"UI alive {SPINNER[self._tick % 4]}   ticks: {self._tick}")

    @Slot()
    def run_task(self) -> None:
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
