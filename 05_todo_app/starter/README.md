# 05 — Starter

A copy of the Todo app with `TODO(exercise)` markers in `models.py` and `main.py`. It runs as-is,
and the sample data includes an overdue task ("File the report").
```bash
./build.sh 05_todo_app
python 05_todo_app/starter/main.py
```

## Exercise 1: Clear completed
1. **Designer** (`starter/main_window.ui`): in the Action Editor, create **`actionClearCompleted`**, text `&Clear Completed`.
   Drag it into the **Task** menu (below a separator). Save and run `./build.sh 05_todo_app`.
2. `models.py`: implement `TaskModel.remove_done()`.
3. `main.py`: implement `clear_completed()` and connect the action to it.

## Exercise 2: Overdue dates in red
`models.py`: implement `is_overdue()` and return a red `QBrush` for the Due column in `data()`
(`ForegroundRole`).

## Bonus: inline title editing
- `models.py`: `flags()` → `ItemIsEditable` for Title; `data()` → `EditRole`; `setData()` → handle `EditRole`.
- **Designer:** tableView → `editTriggers` → tick `EditKeyPressed` and `SelectedClicked` (keep double-click
  for the dialog). Rebuild.

Check your work: `diff models.py ../answers/models.py` and `diff main.py ../answers/main.py`
