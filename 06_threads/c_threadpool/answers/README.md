# 06c — Answer: a Cancel button for the pool

```bash
python 06_threads/c_threadpool/answers/main.py
```
Set *Max threads* to 2 (so most jobs are queued), press Run, then Cancel.

## Two kinds of jobs to cancel
| Job state | How it's stopped |
|---|---|
| **Running** on a pool thread | a shared `threading.Event`: `run()` checks `cancel_event.is_set()` between steps and returns early (emitting `cancelled`) |
| **Queued**, not started yet | `pool.clear()` removes it from the queue, so it never runs |

```python
def run_jobs(self):
    self.cancel_event = threading.Event()        # fresh per run
    for i in range(JOBS):
        self.pool.start(Job(i, self.cancel_event))

def cancel_jobs(self):
    self.cancel_event.set()
    self.pool.clear()
    self._cancel_poll.start()                    # QTimer: finish up once the pool is idle
```

## The subtle part: knowing when you're done
Jobs dropped by `pool.clear()` **emit nothing**. They never ran. So "count `finished` signals until
12" would wait forever. Instead, after cancelling, a 50 ms `QTimer` checks
`pool.activeThreadCount() == 0` and marks every bar that didn't reach 100% as cancelled.

(`pool.waitForDone()` would also work, but it **blocks the GUI thread**, which is the thing we're
trying to avoid. It's fine in `closeEvent`, where we're exiting anyway.)

## Why `threading.Event` and not `requestInterruption()`?
`requestInterruption()` belongs to a `QThread`. Pool threads are shared and reused, so there's no "my thread"
to interrupt. A plain `threading.Event` (or a `bool` flag) passed to each job is the standard approach.

## Review checklist
- [ ] Running jobs actually stop (the bars freeze, and the active thread count drops to 0 quickly)
- [ ] Queued jobs never start after Cancel
- [ ] Run works again after Cancel (a new event, bars reset)
- [ ] The GUI never blocks while cancelling
