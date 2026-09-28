# 06a — The frozen UI (the problem)

```bash
python 06_threads/a_frozen_ui/main.py
```
Watch the **"UI alive" spinner**, then click the button and try to move or resize the window.

## What happens
- The spinner stops, the button stays pressed, and the progress bar jumps from 0 to 100 at the end.
- macOS shows the beach ball. Windows adds "(Not Responding)" to the title.

## Why
There is **one GUI thread**, and it runs the event loop (topic 3). A slot is just a function
call *inside* that loop:

```
event loop:  [timer tick][paint][click → run_task() ─── 5 s of time.sleep ───][paint][timer]…
                                               ▲ nothing else can run here
```
`setValue()` and `setText()` only *schedule* a repaint, and the repaint is an event that waits
for `run_task()` to return.

## Rules of thumb
- Anything taking **more than ~50 ms** (network, disk, big computations, `time.sleep`) must not run on the GUI thread.
- ❌ `QApplication.processEvents()` inside the loop "fixes" it, but it's a hack: it allows re-entrancy
  (the user can click Run again *inside* the running task) and it doesn't help when the code blocks inside a single call.
- ✅ Move the work to another thread → **06b**, **06c**.
- For "do something later / periodically" you don't need threads at all: use `QTimer`.

## Exercise
Replace the `for` loop with a `QTimer` that advances the progress bar by 20% every second (no threads, no sleep).
Why does this stay responsive?

➡️ Answer: [`answers/`](answers/README.md)
