# 05 — Answer: Clear completed, overdue dates, inline editing

```bash
./build.sh 05_todo_app
python 05_todo_app/answers/main.py
```
This is a full copy of the app. The sample data includes an overdue task ("File the report").
Look for `# EXERCISE` / `# BONUS` comments in `models.py` and `main.py`.

## 1. Clear completed
**Designer:** add `actionClearCompleted` to the Task menu (`main_window.ui`).

**Model** (`models.py`):
```python
def remove_done(self) -> int:
    for row in reversed(range(len(self._tasks))):   # backwards!
        if self._tasks[row].done:
            self.remove_task(row)                   # uses beginRemoveRows/endRemoveRows
```
Why backwards? Removing row 1 shifts rows 2, 3, 4… up by one. Going forward you'd skip rows.
Going from the end, rows you haven't visited yet never move.

An equally valid alternative is `self.set_tasks([t for t in self._tasks if not t.done])`: one model *reset*
instead of several row removals. It's simpler, but the view loses its selection and scroll position.

**Window:** a confirmation `QMessageBox.question`, and `update_actions()` disables the action when
nothing is done (it's called from `refresh_after_change`, so it stays correct after every change).

## 2. Overdue dates in red
A new **role** answer in `data()`, with nothing changed in the view:
```python
if role == Qt.ItemDataRole.ForegroundRole:
    if col == self.DUE and self.is_overdue(task):
        return QBrush(QColor("#e53e3e"))
```
`is_overdue()` compares `QDate.fromString(task.due, ISODate) < QDate.currentDate()` and ignores done tasks.

## 3. Bonus: inline title editing
Three pieces, all in the model, plus one Designer property:
| Where | What |
|---|---|
| `flags()` | add `Qt.ItemFlag.ItemIsEditable` for the Title column |
| `data()` | answer `EditRole` with the current title (the editor's initial text) |
| `setData()` | handle `EditRole`: validate, store, emit `dataChanged`, return `True` |
| Designer → tableView → `editTriggers` | `EditKeyPressed` (F2 / Enter on macOS) + `SelectedClicked` |

Double-click still opens the full dialog, and click-on-selected / F2 edits the title in place. The view
creates a `QLineEdit` editor for you. That's the default **delegate** (`QStyledItemDelegate`).
A custom delegate is how you'd get a combo box for Priority, which makes a good follow-up exercise.

Returning `False` from `setData()` (empty title) rejects the edit, and the old value stays.

## Review checklist
- [ ] Removal goes through `begin/endRemoveRows` (or a reset), never `del list[i]` alone
- [ ] Overdue color lives in the **model** (`data()`), not in the view
- [ ] `setData()` emits `dataChanged` → the JSON auto-save still happens (through `tasks_changed`)
