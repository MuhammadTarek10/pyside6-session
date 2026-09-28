# 05 — A more complex app: Todo Manager

A real-world-shaped app that combines what we've seen so far and adds the patterns every
non-trivial Qt app needs.

```bash
./build.sh 05_todo_app
python 05_todo_app/main.py
```

| Feature | Qt concept |
|---|---|
| Main window with menu, toolbar, status bar, **dock** | `QMainWindow`, `QDockWidget` (Designer) |
| Add/edit form | a second Designer form: `QDialog` + `QDialogButtonBox`, `exec()` |
| Task table with checkboxes, colors, strike-out | **Model/View**: custom `QAbstractTableModel` + `QTableView` |
| Search box + status filter + column sorting | `QSortFilterProxyModel` |
| "Something changed → save + update status bar" | **custom `Signal`** |
| Saved tasks | JSON (`storage.py`, plain Python) |
| Remembers window size, dock position, filter | `QSettings` |

## Files
```
main.py            TodoWindow + TaskDialog (behavior)
models.py          Task dataclass, TaskModel, TaskFilterProxy
storage.py         load/save JSON
main_window.ui     → ui_main_window.py
task_dialog.ui     → ui_task_dialog.py
resources.qrc      → resources_rc.py   (toolbar icons)
tasks.json         created at runtime (git-ignored)
```

## 1. Model/View (the big idea)
```
 list[Task]  ◄──  TaskModel  ──►  TaskFilterProxy  ──►  QTableView
 (your data)     (adapter)        (filter + sort)       (just draws)
```
- The **view never owns data**. It asks the model: `rowCount()`, `columnCount()`, `data(index, role)`.
- **Roles** let one cell answer many questions: `DisplayRole` (text), `CheckStateRole` (checkbox),
  `ForegroundRole` (color), `FontRole` (strike-out), `ToolTipRole` (notes), `UserRole` (our sort key).
- When the data changes, the model **must notify** the views:
  - `beginInsertRows/endInsertRows`, `beginRemoveRows/endRemoveRows`, `beginResetModel/endResetModel`
  - `dataChanged.emit(topLeft, bottomRight)` for edits
- The same model could feed a `QListView`, a second table, or a combo box, all in sync, for free.

## 2. Proxy models and index mapping
`TaskFilterProxy` wraps the model to filter (text + status) and sort **without changing the data**.
The view shows *proxy* indexes, so convert them before touching the model:
```python
source_row = self.proxy.mapToSource(proxy_index).row()
```
Custom filter logic lives in `filterAcceptsRow()`. When the filter criteria change, wrap the change in
`beginFilterChange()` / `endFilterChange()` so the proxy re-filters.

## 3. Dialogs
```python
dialog = TaskDialog(self, task)          # parent = self → centered over the window, modal
if dialog.exec() == QDialog.DialogCode.Accepted:
    self.model.update_task(row, dialog.get_task())
```
- `exec()` blocks (it runs a local event loop) until OK/Cancel.
- In Designer, `buttonBox.accepted → accept()` and `rejected → reject()` are wired in the Signal/Slot editor.
  `dueCheck.toggled(bool) → dueEdit.setEnabled(bool)` is wired there too, with zero code.
- Label **buddies** (`&Title` + buddy `titleEdit`) give you Alt+T keyboard navigation.

## 4. Custom signals
```python
class TaskModel(QAbstractTableModel):
    tasks_changed = Signal()
```
The model forwards all its built-in change signals into this one, and the window connects it to
`refresh_after_change` (save JSON + update the status bar). **The model doesn't know the window exists.**
That's the decoupling signals give you.

## 5. QSettings
```python
app.setOrganizationName("pyside-session"); app.setApplicationName("Todo Manager")
settings = QSettings()
settings.setValue("window/geometry", self.saveGeometry())
self.restoreState(settings.value("window/state"))   # toolbar + dock positions
```
It's stored in the platform-native place (a macOS plist, the Windows registry, a Linux .conf).
Drag the dock to the right, restart, and it stays there.

## Common mistakes
- Changing the underlying list without `begin…/end…` → the view shows stale rows or crashes.
- Using a proxy row number as a model row → editing/deleting the **wrong task** once sorted or filtered.
- `saveState()` needs every toolbar and dock to have an `objectName` (Designer sets them, but in code you must do it yourself).
- Naming a method `on_<something>_<signal>`: `setupUi` calls `QMetaObject.connectSlotsByName`, which
  tries to auto-connect methods named `on_<objectName>_<signalName>` and warns if nothing matches.
  (We hit this with `on_tasks_changed`, which is why the method is called `refresh_after_change`.)
- Forgetting `setOrganizationName`/`setApplicationName` → QSettings stores data in an unexpected place.

## Exercise
1. Add a **Clear completed** action (Task menu) that removes all done tasks.
   Hint: remove rows from the end backwards, or use `set_tasks()` with a filtered list.
2. Show overdue due dates in red (`ForegroundRole` on the Due column).
3. Bonus: make the title editable inline (`ItemIsEditable` in `flags()`, handle `EditRole` in `setData()`,
   change `editTriggers` in Designer).

🧩 Starter code: [`starter/`](starter/README.md) · ➡️ Answer: [`answers/`](answers/README.md)
