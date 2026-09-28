"""Starter for exercise 6b: add an error signal (see README.md in this folder).

Original notes:

Pattern:
    worker = Worker(); thread = QThread()
    worker.moveToThread(thread)
    thread.started -> worker.run        (run executes in the new thread)
    worker.progress -> GUI slots        (queued back to the GUI thread automatically)
    worker.finished -> thread.quit; worker.deleteLater; thread.finished -> thread.deleteLater
"""
import sys
import threading
import time

from PySide6.QtCore import QObject, QThread, QTimer, Signal, Slot
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

SPINNER = "◐◓◑◒"


class Worker(QObject):
    """Lives in a worker thread. Talks to the GUI ONLY through signals."""

    progress = Signal(int)  # 0..100
    message = Signal(str)
    # TODO(exercise): declare  error = Signal(str)
    finished = Signal()

    # TODO(exercise): add __init__(self, fail_at: int | None = None) that stores self.fail_at
    #                 (remember super().__init__())

    @Slot()
    def run(self) -> None:
        self.message.emit(f"Worker running in thread id {threading.get_native_id()}")
        thread = QThread.currentThread()
        # TODO(exercise): wrap the loop in try/except/finally:
        #   - inside the loop: if i == self.fail_at, raise an exception (e.g. ConnectionError)
        #   - except: emit self.error with a helpful message
        #   - finally: emit self.finished (move the line below into it). Why must it ALWAYS run?
        for i in range(1, 101):
            if thread.isInterruptionRequested():  # cooperative cancel
                self.message.emit("Cancelled")
                break
            time.sleep(0.05)  # the "work"
            self.progress.emit(i)
        else:
            self.message.emit("Done!")
        self.finished.emit()


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("6b: QThread + worker")

        self.alive_label = QLabel()
        self.progress = QProgressBar()
        self.start_button = QPushButton("Start")
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setEnabled(False)
        # TODO(exercise): add self.fail_check = QCheckBox("Simulate error at step 50") to the layout
        self.status = QLabel(f"GUI thread id {threading.get_native_id()}")

        buttons = QHBoxLayout()
        buttons.addWidget(self.start_button)
        buttons.addWidget(self.cancel_button)
        layout = QVBoxLayout(self)
        layout.addWidget(self.alive_label)
        layout.addWidget(self.progress)
        layout.addLayout(buttons)
        layout.addWidget(self.status)

        self._tick = 0
        timer = QTimer(self, interval=100)
        timer.timeout.connect(self.animate)
        timer.start()

        self.thread: QThread | None = None
        self.worker: Worker | None = None
        self.start_button.clicked.connect(self.start)
        self.cancel_button.clicked.connect(self.cancel)

    @Slot()
    def animate(self) -> None:
        self._tick += 1
        self.alive_label.setText(f"UI alive {SPINNER[self._tick % 4]}   ticks: {self._tick}")

    @Slot()
    def start(self) -> None:
        self.thread = QThread()
        self.worker = Worker()  # TODO(exercise): pass fail_at=50 when self.fail_check is checked
        self.worker.moveToThread(self.thread)  # the worker's slots now run in self.thread

        # start → work
        self.thread.started.connect(self.worker.run)
        # worker → GUI (Qt queues these across threads for us)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.message.connect(self.status.setText)
        # TODO(exercise): connect self.worker.error to self.show_error
        # cleanup chain
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.on_thread_finished)

        self.progress.setValue(0)
        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.thread.start()

    @Slot()
    def cancel(self) -> None:
        if self.thread:
            self.thread.requestInterruption()

    @Slot(str)
    def show_error(self, message: str) -> None:
        # TODO(exercise): show a QMessageBox.critical. Which thread does this run on, and why is that OK?
        pass

    @Slot()
    def on_thread_finished(self) -> None:
        self.thread = None  # C++ objects are about to be deleted, so drop our references
        self.worker = None
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)

    def closeEvent(self, event: QCloseEvent) -> None:
        # never let the window die while its thread is still running
        if self.thread:
            self.thread.requestInterruption()
            self.thread.quit()
            self.thread.wait()
        super().closeEvent(event)


def main() -> None:
    app = QApplication(sys.argv)
    window = Window()
    window.resize(380, 170)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
