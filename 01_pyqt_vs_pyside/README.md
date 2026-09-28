# 01 — PyQt vs PySide

Both are **Python bindings for the same C++ framework: Qt**. The widgets, the signals,
the layouts and the event loop are the same Qt underneath. What differs is *who* makes the
binding, the *license*, and a handful of naming details.

## At a glance

| | **PyQt** (PyQt5 / PyQt6) | **PySide** (PySide2 / PySide6) |
|---|---|---|
| Maintainer | Riverbank Computing (third party) | **The Qt Company** (official, "Qt for Python") |
| License | **GPL v3** or paid commercial license | **LGPL v3** (+ commercial) |
| Closed-source app allowed for free? | ❌ No (GPL: you must open your code, or buy a license) | ✅ Yes (LGPL: dynamic linking to unmodified Qt is fine) |
| Binding generator | SIP | Shiboken |
| First release | 1998 | 2009 (Nokia) → revived in 2018 as Qt for Python |
| Signal class | `pyqtSignal` | `Signal` |
| Slot decorator | `pyqtSlot` | `Slot` |
| Property | `pyqtProperty` | `Property` |
| UI compiler | `pyuic6` | `pyside6-uic` |
| Resource compiler | *(dropped in PyQt6, use files or Python)* | `pyside6-rcc` ✅ |
| Designer shipped in pip? | No (`pip install pyqt6-tools`, unofficial) | ✅ `pyside6-designer` |
| Extra tools | `pylupdate6` | `pyside6-deploy`, `pyside6-project`, `pyside6-lupdate`, `pyside6-qml` … |
| Docs | Riverbank docs (thin) + C++ docs | doc.qt.io/qtforpython-6 (official, Python examples) |

> **Key takeaway:** 95% of your code is identical. Most porting is a find-and-replace of the
> import lines plus `pyqtSignal` → `Signal`.

## Code differences (see the two files in this folder)

```python
# PyQt6                                   # PySide6
from PyQt6.QtCore import pyqtSignal, pyqtSlot   from PySide6.QtCore import Signal, Slot
from PyQt6.QtWidgets import QApplication        from PySide6.QtWidgets import QApplication

class Counter(QObject):                   class Counter(QObject):
    changed = pyqtSignal(int)                 changed = Signal(int)

    @pyqtSlot()                               @Slot()
    def inc(self): ...                        def inc(self): ...
```

Compare them in your editor:

```bash
diff 01_pyqt_vs_pyside/same_app_pyqt6.py 01_pyqt_vs_pyside/same_app_pyside6.py
```

Only PySide6 is installed in this session, so run the PySide6 one:

```bash
python 01_pyqt_vs_pyside/same_app_pyside6.py
```

## Smaller behavioral differences

- **Loading `.ui` at runtime:** PyQt has `uic.loadUi("file.ui", self)`. PySide uses
  `QUiLoader` (it returns a *new* widget and does not fill `self`) or `loadUiType`.
  → In this session we avoid both and **compile** `.ui` to Python with `pyside6-uic`.
- **Resources:** PyQt6 removed `pyrcc`. PySide6 still ships `pyside6-rcc`, so `:/icons/x.svg`
  paths work out of the box.
- **Type hints / stubs:** both ship `.pyi` stubs. PySide6's are generated with `pyside6-genpyi`.
- **Snake case / true properties:** PySide6 can optionally use
  `from __feature__ import snake_case, true_property` → `widget.set_text("x")`,
  `widget.text = "x"`. It's PySide-only, fun to show, but **don't mix it into team code**.

## Which one should I pick?

- **New project in 2026 → PySide6.** It's official, LGPL, has better tooling, and its docs
  have Python examples.
- PyQt6 is fine if your company already has a Riverbank license or an existing PyQt codebase.
- Libraries that must support both use **`qtpy`** (`from qtpy.QtWidgets import ...`).

## Common mistakes
- Mixing imports (`from PyQt6...` and `from PySide6...` in one process) → crashes or
  "type mismatch" errors. **Pick one.**
- Copying a PyQt Stack Overflow answer and forgetting to rename `pyqtSignal`.

## Exercise
Take `same_app_pyside6.py` and, *without looking at the PyQt file*, list every line you would
change to port it to PyQt6. Then check with `diff`.

➡️ Answer: [`answers/`](answers/README.md)
