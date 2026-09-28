# 06b — QThread + worker object (the fix)

```bash
python 06_threads/b_qthread_worker/main.py
```
The spinner keeps turning, the window stays draggable, and **Cancel** works.

## The pattern ("worker object", recommended by the Qt docs)
```python
self.thread = QThread()
self.worker = Worker()                     # a plain QObject with signals + a run() slot
self.worker.moveToThread(self.thread)      # its slots will now execute in that thread

self.thread.started.connect(self.worker.run)          # 1. start → work
self.worker.progress.connect(self.progress.setValue)  # 2. worker → GUI (via signals)
self.worker.finished.connect(self.thread.quit)        # 3. cleanup chain
self.worker.finished.connect(self.worker.deleteLater)
self.thread.finished.connect(self.thread.deleteLater)

self.thread.start()
```

```
 GUI thread                                   worker thread
 ──────────                                   ─────────────
 start() ── thread.start() ─────────────────► worker.run()
 progress.setValue(i)  ◄── queued signal ───  progress.emit(i)
 status.setText(msg)   ◄── queued signal ───  message.emit(msg)
 requestInterruption() ──── flag ──────────►  isInterruptionRequested()?
                       ◄── finished ───────── finished.emit() → thread.quit()
```

## Why signals make this safe
Every `QObject` has a **thread affinity** (the thread it "lives" in). When a signal is emitted in
one thread and the receiver lives in another, Qt uses a **queued connection**: it copies the
arguments and posts an event to the receiver's event loop. So `progress.setValue` runs **on the GUI
thread**, even though `emit` happened in the worker.

## 🟥 The golden rule
> **Never touch a widget from a worker thread.** No `label.setText`, no `QMessageBox`, no `QPixmap`.
> Emit a signal, and let the GUI thread do it.

Breaking this rule doesn't always crash right away. It crashes *sometimes*, randomly, on other machines.

## Cancelling
Threads can't be killed safely (`QThread.terminate()` exists, but **don't use it**). Cancelling is
**cooperative**: the GUI calls `thread.requestInterruption()`, and the worker checks
`QThread.currentThread().isInterruptionRequested()` between steps.

## Shutting down
`closeEvent` asks the thread to stop and `wait()`s for it. Without this you get
`QThread: Destroyed while thread is still running` and a crash on exit.

## QThread subclass vs worker object
You may see `class MyThread(QThread): def run(self): ...`. It works, but only `run()` executes in
the new thread (the subclass's other slots live in the *GUI* thread). That confuses people, so
the worker-object pattern is clearer and reusable.

## Common mistakes
- Calling `self.worker.run()` directly → it runs on the GUI thread, and the UI freezes again.
- Keeping no reference to `thread`/`worker` (local variables) → garbage-collected → crash.
- Using the Python references after `deleteLater` → `RuntimeError: Internal C++ object already deleted`
  (that's why `on_thread_finished` sets them to `None`).
- `time.sleep()` in the GUI thread to "wait for the worker" → frozen again. Use signals.

## Exercise
Add an `error = Signal(str)` to the worker. Make it raise on step 50 when a "Simulate error"
checkbox is ticked, catch the exception inside `run()`, emit `error`, and show a `QMessageBox`
**from the GUI thread**.

🧩 Starter code: [`starter/`](starter/README.md) · ➡️ Answer: [`answers/`](answers/README.md)
