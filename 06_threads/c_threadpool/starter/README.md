# 06c — Starter

A copy of the thread pool app. It runs as-is:
```bash
python 06_threads/c_threadpool/starter/main.py
```

## Task
Add a **Cancel** button that stops everything:
1. `Job` takes a shared `threading.Event` and returns early (emitting `cancelled`) when it's set.
2. `run_jobs()` creates one new `threading.Event` per run and passes it to every job.
3. `cancel_jobs()` sets the event and calls `self.pool.clear()`.
4. Figure out when *everything* has stopped (the TODO has a hint), then re-enable Run.

Test it with *Max threads* = 2, so most jobs are still queued when you press Cancel.

Check your work: `diff main.py ../answers/main.py`
