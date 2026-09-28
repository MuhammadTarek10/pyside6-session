# 06a — Starter

A copy of the frozen app. It runs as-is (and still freezes, until you fix it):
```bash
python 06_threads/a_frozen_ui/starter/main.py
```

## Task
Make the 5-second task run **without freezing and without threads**:
1. In `__init__`: create `self.step_timer` (a `QTimer` with a 1000 ms interval) and connect `timeout` to `self.step`.
2. `run_task()`: remove the `time.sleep` loop. Reset the state, disable the button, start the timer, and **return**.
3. `step()`: one step of work per call, and stop the timer after step 5.

Then answer: *why* does the spinner keep turning now?

Check your work: `diff main.py ../answers/main.py`
