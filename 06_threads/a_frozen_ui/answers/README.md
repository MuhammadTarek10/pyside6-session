# 06a — Answer: QTimer instead of sleep

```bash
python 06_threads/a_frozen_ui/answers/main.py
```

```python
self.step_timer = QTimer(self, interval=1000)
self.step_timer.timeout.connect(self.step)   # step() does ONE unit of work and returns

def run_task(self):  self.step_timer.start()
def step(self):
    self._step += 1; self.progress.setValue(self._step * 20)
    if self._step == 5: self.step_timer.stop()
```

## Why it stays responsive
The original held the event loop hostage for 5 seconds inside one slot. Here each slot call
lasts microseconds, and **control goes back to the event loop between steps**, so paints, clicks and the
spinner timer all get processed:

```
event loop: [step][paint][spinner]…[spinner][click][spinner]…[step][paint]…
```

## When this is enough, and when it isn't
- ✅ The work is naturally *waiting* (polling, animations, "do X every N ms") or can be split into small chunks.
- ❌ One indivisible slow call (`requests.get`, a big `numpy` op, `cv2.VideoCapture.read`) still blocks
  for its full duration → you need a thread (06b/06c).

Bonus point: the button is disabled while running. The frozen version couldn't even show that,
and with `processEvents()` hacks users could start the task twice.
