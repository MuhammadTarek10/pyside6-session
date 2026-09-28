# 06b — Starter

A copy of the QThread worker app. It runs as-is:
```bash
python 06_threads/b_qthread_worker/starter/main.py
```

## Task
Report worker errors to the user **safely**:
1. `Worker`: an `error = Signal(str)` and an `__init__(fail_at=None)`.
2. `Worker.run()`: `try` / `except` / `finally`. Raise at step `fail_at`, emit `error` in `except`,
   and emit `finished` in `finally`.
3. `Window`: a "Simulate error at step 50" `QCheckBox` (`self.fail_check`). Pass `fail_at=50` when it's checked.
4. Connect `worker.error` to `show_error()` and show a `QMessageBox.critical` there.

Rules: no widget access inside `Worker`, and `finished` must be emitted on **every** path.

Check your work: `diff main.py ../answers/main.py`
