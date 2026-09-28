"""Starter for exercise 6c: a Cancel button (see README.md in this folder).

Original notes:

QRunnable is NOT a QObject, so it can't have signals. The usual trick is a small
QObject that carries the signals (WorkerSignals).
"""
import random
import sys
import time

from PySide6.QtCore import QObject, QRunnable, QThread, QThreadPool, QTimer, Signal, Slot
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

SPINNER = "◐◓◑◒"
JOBS = 12


class WorkerSignals(QObject):
    progress = Signal(int, int)  # job_id, percent
    finished = Signal(int, float)  # job_id, seconds taken
    # TODO(exercise): add  cancelled = Signal(int)  # job_id


class Job(QRunnable):
    # TODO(exercise): accept a shared threading.Event (cancel_event) and store it
    def __init__(self, job_id: int) -> None:
        super().__init__()
        self.job_id = job_id
        self.signals = WorkerSignals()

    def run(self) -> None:  # runs on a pool thread
        start = time.perf_counter()
        step = random.uniform(0.01, 0.05)
        for pct in range(0, 101, 5):
            # TODO(exercise): if the cancel event is set, emit cancelled and return
            time.sleep(step)
            self.signals.progress.emit(self.job_id, pct)
        self.signals.finished.emit(self.job_id, time.perf_counter() - start)


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("6c: QThreadPool")
        self.pool = QThreadPool.globalInstance()

        self.alive_label = QLabel()
        self.threads_spin = QSpinBox(minimum=1, maximum=32, value=4, prefix="Max threads: ")
        self.run_button = QPushButton(f"Run {JOBS} jobs")
        # TODO(exercise): add a Cancel button (disabled until jobs run) and connect it to self.cancel_jobs
        self.summary = QLabel(f"Ideal thread count on this machine: {QThread.idealThreadCount()}")

        grid = QGridLayout()
        self.bars: list[QProgressBar] = []
        for i in range(JOBS):
            bar = QProgressBar(format=f"Job {i + 1}: %p%")
            grid.addWidget(bar, i // 2, i % 2)
            self.bars.append(bar)

        layout = QVBoxLayout(self)
        layout.addWidget(self.alive_label)
        layout.addWidget(self.threads_spin)
        layout.addWidget(self.run_button)
        layout.addLayout(grid)
        layout.addWidget(self.summary)

        self._tick = 0
        self._remaining = 0
        self._started = 0.0
        timer = QTimer(self, interval=100)
        timer.timeout.connect(self.animate)
        timer.start()

        self.run_button.clicked.connect(self.run_jobs)

    @Slot()
    def animate(self) -> None:
        self._tick += 1
        active = self.pool.activeThreadCount()
        self.alive_label.setText(f"UI alive {SPINNER[self._tick % 4]}   active pool threads: {active}")

    @Slot()
    def run_jobs(self) -> None:
        self.pool.setMaxThreadCount(self.threads_spin.value())
        self.run_button.setEnabled(False)
        self._remaining = JOBS
        self._started = time.perf_counter()
        for i, bar in enumerate(self.bars):
            bar.setValue(0)
            job = Job(i)  # TODO(exercise): create ONE threading.Event per run and pass it to every job
            job.signals.progress.connect(self.on_progress)
            job.signals.finished.connect(self.on_finished)
            self.pool.start(job)  # queued; runs when a pool thread is free
        self.summary.setText(f"Running on up to {self.pool.maxThreadCount()} threads…")

    @Slot()
    def cancel_jobs(self) -> None:
        # TODO(exercise):
        #   1. set the cancel event   → running jobs stop at their next check
        #   2. self.pool.clear()      → queued jobs never start
        #   3. jobs removed by clear() emit NOTHING, so how will you know when everything has stopped?
        #      Hint: a QTimer that checks self.pool.activeThreadCount() == 0
        pass

    @Slot(int, int)
    def on_progress(self, job_id: int, pct: int) -> None:
        self.bars[job_id].setValue(pct)

    @Slot(int, float)
    def on_finished(self, job_id: int, seconds: float) -> None:
        self._remaining -= 1
        if self._remaining == 0:
            total = time.perf_counter() - self._started
            self.summary.setText(
                f"All {JOBS} jobs done in {total:.2f}s with {self.pool.maxThreadCount()} threads"
            )
            self.run_button.setEnabled(True)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.pool.clear()  # drop jobs that haven't started
        self.pool.waitForDone()  # wait for running ones
        super().closeEvent(event)



def main() -> None:
    app = QApplication(sys.argv)
    window = Window()
    window.resize(520, 360)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
