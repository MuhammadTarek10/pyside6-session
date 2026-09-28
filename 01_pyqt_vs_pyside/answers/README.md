# 01 — Answer: porting PySide6 → PyQt6

Lines in `same_app_pyside6.py` that change (check with `diff ../same_app_pyside6.py ../same_app_pyqt6.py`):

| Line | PySide6 | PyQt6 |
|---|---|---|
| import QtCore | `from PySide6.QtCore import QObject, Signal, Slot` | `from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot` |
| import QtWidgets | `from PySide6.QtWidgets import ...` | `from PyQt6.QtWidgets import ...` |
| signal | `changed = Signal(int)` | `changed = pyqtSignal(int)` |
| slot decorator | `@Slot()` | `@pyqtSlot()` |
| *(cosmetic)* window title | `"PySide6 counter"` | `"PyQt6 counter"` |

**That's all: 4 real changes.** Everything else (widgets, layouts, `connect`, `emit`, `app.exec()`) is identical,
because it's the same Qt underneath.

Talking points:
- If the code had used short enums (`Qt.AlignCenter`), PyQt6 would **fail** while PySide6 still works. That's the most common extra porting cost.
- `qtpy` hides these differences if you really need to support both.
