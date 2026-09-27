# 06c — QThreadPool + QRunnable (many small jobs)

```bash
python 06_threads/c_threadpool/main.py
```
Run 12 jobs with *Max threads* = 1, then 4, then 12, and compare the total time.

## When to use which

| | `QThread` + worker (06b) | `QThreadPool` + `QRunnable` (06c) |
|---|---|---|
| Best for | one long-lived task (camera loop, a server connection) | many short, independent jobs (thumbnails, downloads) |
| Thread creation | you create and destroy it | reused from a pool (cheap) |
| Signals | the worker *is* a QObject | `QRunnable` is **not** a QObject → use a `WorkerSignals` helper |
| Cancel | `requestInterruption()` | your own flag, or `pool.clear()` for jobs not started yet |
| Queueing | — | automatic: extra jobs wait for a free thread |

## The pattern
```python
class WorkerSignals(QObject):          # QRunnable can't have signals…
    progress = Signal(int, int)
    finished = Signal(int, float)

class Job(QRunnable):
    def __init__(self, job_id):
        super().__init__()
        self.signals = WorkerSignals()  # …so it carries a QObject that does
    def run(self):                      # executes on a pool thread
        self.signals.progress.emit(self.job_id, 50)

pool = QThreadPool.globalInstance()
pool.setMaxThreadCount(4)
pool.start(Job(1))                      # the pool takes ownership and deletes the job when done
```

## Notes
- `QThread.idealThreadCount()` = number of CPU cores. It's the pool's default max.
- **The GIL:** Python threads don't run Python bytecode in parallel. Threads are great for
  **I/O-bound** work (network, disk, `sleep`, and C libraries that release the GIL, such as OpenCV and NumPy).
  For heavy pure-Python CPU work, use `multiprocessing`/`concurrent.futures.ProcessPoolExecutor`
  (or the free-threaded Python 3.14t build).
- On close: `pool.clear()` removes queued jobs, and `pool.waitForDone()` waits for the running ones.

## Common mistakes
- Defining signals on the `QRunnable` itself → `TypeError`/silent failure (it's not a QObject).
- Updating widgets from `run()` → same golden rule as 06b.
- Expecting CPU-bound pure-Python jobs to get faster with more threads (GIL).

## Exercise
Add a **Cancel** button: give each `Job` a shared `threading.Event` and have `run()` return early
when it's set. Also call `pool.clear()` so queued jobs never start.
