"""Answer for 6c (Cancel button): many short, independent jobs: QThreadPool + QRunnable.

QRunnable is NOT a QObject, so it can't have signals. The usual trick is a small
QObject that carries the signals (WorkerSignals).
"""
import random
import sys
import threading
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
    cancelled = Signal(int)  # NEW: job_id


class Job(QRunnable):
    def __init__(self, job_id: int, cancel_event: threading.Event) -> None:
        super().__init__()
        self.job_id = job_id
        self.cancel_event = cancel_event  # shared by all jobs of one run
        self.signals = WorkerSignals()

    def run(self) -> None:  # runs on a pool thread
        start = time.perf_counter()
        step = random.uniform(0.01, 0.05)
        for pct in range(0, 101, 5):
            if self.cancel_event.is_set():  # cooperative cancel, checked between steps
                self.signals.cancelled.emit(self.job_id)
                return
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
        self.cancel_button = QPushButton("Cancel")  # NEW
        self.cancel_button.setEnabled(False)
        self.cancel_event = threading.Event()
        self._cancelling = False
        self._cancel_poll = QTimer(self, interval=50)
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
        layout.addWidget(self.cancel_button)
        layout.addLayout(grid)
        layout.addWidget(self.summary)

        self._tick = 0
        self._remaining = 0
        self._started = 0.0
        timer = QTimer(self, interval=100)
        timer.timeout.connect(self.animate)
        timer.start()

        self.run_button.clicked.connect(self.run_jobs)
        self.cancel_button.clicked.connect(self.cancel_jobs)
        self._cancel_poll.timeout.connect(self.check_cancel_done)

    @Slot()
    def animate(self) -> None:
        self._tick += 1
        active = self.pool.activeThreadCount()
        self.alive_label.setText(f"UI alive {SPINNER[self._tick % 4]}   active pool threads: {active}")

    @Slot()
    def run_jobs(self) -> None:
        self.pool.setMaxThreadCount(self.threads_spin.value())
        self.run_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.cancel_event = threading.Event()  # fresh event per run
        self._cancelling = False
        self._remaining = JOBS
        self._started = time.perf_counter()
        for i, bar in enumerate(self.bars):
            bar.setValue(0)
            bar.setFormat(f"Job {i + 1}: %p%")
            job = Job(i, self.cancel_event)
            job.signals.progress.connect(self.on_progress)
            job.signals.finished.connect(self.on_finished)
            job.signals.cancelled.connect(self.on_cancelled)
            self.pool.start(job)  # queued; runs when a pool thread is free
        self.summary.setText(f"Running on up to {self.pool.maxThreadCount()} threads…")

    @Slot(int, int)
    def on_progress(self, job_id: int, pct: int) -> None:
        self.bars[job_id].setValue(pct)

    @Slot()
    def cancel_jobs(self) -> None:
        self.cancel_event.set()  # running jobs stop at their next check
        self.pool.clear()  # queued jobs are dropped and never start
        self._cancelling = True
        self.cancel_button.setEnabled(False)
        self.summary.setText("Cancelling…")
        # dropped jobs emit nothing, so instead of counting signals, wait until the pool is idle
        self._cancel_poll.start()

    @Slot()
    def check_cancel_done(self) -> None:
        if self.pool.activeThreadCount() > 0:
            return
        self._cancel_poll.stop()
        cancelled = 0
        for i, bar in enumerate(self.bars):
            if bar.value() < 100:
                bar.setFormat(f"Job {i + 1}: cancelled")
                cancelled += 1
        self.summary.setText(f"Cancelled {cancelled} of {JOBS} jobs")
        self._reset_buttons()

    @Slot(int, float)
    def on_finished(self, job_id: int, seconds: float) -> None:
        self._remaining -= 1
        if self._remaining == 0 and not self._cancelling:
            total = time.perf_counter() - self._started
            self.summary.setText(
                f"All {JOBS} jobs done in {total:.2f}s with {self.pool.maxThreadCount()} threads"
            )
            self._reset_buttons()

    @Slot(int)
    def on_cancelled(self, job_id: int) -> None:
        self.bars[job_id].setFormat(f"Job {job_id + 1}: cancelled")

    def _reset_buttons(self) -> None:
        self.run_button.setEnabled(True)
        self.cancel_button.setEnabled(False)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.cancel_event.set()  # stop running jobs quickly too
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
