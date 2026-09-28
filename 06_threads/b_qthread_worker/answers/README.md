# 06b — Answer: an `error` signal

```bash
python 06_threads/b_qthread_worker/answers/main.py
```
Tick **Simulate error at step 50** and press Start.

## Worker side
```python
class Worker(QObject):
    error = Signal(str)

    def __init__(self, fail_at=None):
        super().__init__()
        self.fail_at = fail_at            # configured BEFORE moveToThread/start

    @Slot()
    def run(self):
        try:
            ...
            if i == self.fail_at:
                raise ConnectionError(f"Simulated failure at step {i}")
        except Exception as exc:
            self.error.emit(f"{type(exc).__name__}: {exc}")
        finally:
            self.finished.emit()          # ALWAYS
```
- **Catch inside `run()`.** An exception that escapes a slot running in a worker thread is only printed to
  stderr. Your GUI never hears about it.
- **`finished` goes in `finally`.** If it's skipped, `thread.quit()` never runs, the thread lives forever, the
  Start button never re-enables, and closing the window hangs on `wait()`.
- Pass config through `__init__` (before the thread starts) rather than reading GUI widgets from `run()`.
  Reading `self.fail_check.isChecked()` inside `run()` would touch a widget from the worker thread.

## GUI side
```python
self.worker.error.connect(self.show_error)

@Slot(str)
def show_error(self, message):
    QMessageBox.critical(self, "Worker failed", message)
```
The connection is queued, so `show_error` runs on the **GUI thread**. That's the only place a
`QMessageBox` is allowed.

## Review checklist
- [ ] No widget access (including `QMessageBox`) inside `Worker`
- [ ] `finished` emitted on every path: success, cancel and error
- [ ] The error message carries useful information (the exception type + text)
