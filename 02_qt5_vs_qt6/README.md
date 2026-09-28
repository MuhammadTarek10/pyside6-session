# 02 — Qt5 (PyQt5 / PySide2) vs Qt6 (PyQt6 / PySide6)

The binding name tracks the Qt major version:

| Qt version | PyQt | PySide | Status |
|---|---|---|---|
| Qt 5 | PyQt5 | **PySide2** | Qt 5.15 was the last release. Open-source support ended in 2025. PySide2 supports Python ≤ 3.10 |
| Qt 6 | PyQt6 | **PySide6** | Current. Supports modern Python (this session uses Python 3.14 + PySide6 6.11) |

> There was never a "PySide5": PySide (Qt4) → PySide2 (Qt5) → PySide6 (Qt6), so the name
> jumped to match the Qt number.

## What changed (the things you will actually hit)

| Topic | Qt5 (PySide2/PyQt5) | Qt6 (PySide6/PyQt6) |
|---|---|---|
| Run the event loop | `app.exec_()` (`exec` was a Python 2 keyword) | `app.exec()` (`exec_` is deprecated) |
| Enums | `Qt.AlignCenter` | `Qt.AlignmentFlag.AlignCenter` (fully qualified, **required in PyQt6**, recommended in PySide6) |
| `QAction`, `QShortcut`, `QActionGroup` | `QtWidgets` | **`QtGui`** |
| High-DPI scaling | opt-in: `AA_EnableHighDpiScaling` | **always on**. Delete those attributes |
| Screen geometry | `QDesktopWidget` | removed → `QScreen` (`app.primaryScreen()`) |
| Regex | `QRegExp` | removed → `QRegularExpression` (or Python `re`) |
| Multimedia / camera | `QCamera` + `QCameraViewfinder` | **Rewritten**: `QMediaCaptureSession` + `QVideoWidget`, `QMediaDevices`, `QImageCapture` |
| `QMouseEvent.pos()` | `event.pos()` | `event.position()` (QPointF). `pos()` is deprecated |
| Resources tool (PyQt only) | `pyrcc5` | removed in PyQt6 (PySide6 keeps `pyside6-rcc`) |
| Qt modules | QtWebKit, QtXmlPatterns … | removed. Qt 6.2+ brought back Multimedia, WebEngine, Bluetooth … |
| OpenGL widgets | `QtWidgets.QOpenGLWidget` | `QtOpenGLWidgets.QOpenGLWidget` |
| Python support | old | 3.9+ (PySide6 6.11 supports 3.14) |

## See it in code

- `qt5_style.py`: a PySide2-style app (**read-only**: PySide2 can't be installed on Python 3.14)
- `qt6_style.py`: the same app in modern PySide6 (**runnable**)

```bash
diff 02_qt5_vs_qt6/qt5_style.py 02_qt5_vs_qt6/qt6_style.py
python 02_qt5_vs_qt6/qt6_style.py
```

## Porting checklist (Qt5 → Qt6)

1. `PySide2` → `PySide6` in the imports
2. `exec_()` → `exec()`
3. Move `QAction`/`QShortcut` imports from `QtWidgets` to `QtGui`
4. Fully qualify enums (`Qt.AlignCenter` → `Qt.AlignmentFlag.AlignCenter`)
5. Delete the High-DPI attributes
6. `QDesktopWidget` → `QScreen`, `QRegExp` → `QRegularExpression`
7. Camera/multimedia code → rewrite (we'll use OpenCV in topic 7)
8. Regenerate `.ui` / `.qrc` with `pyside6-uic` / `pyside6-rcc`

## Common mistakes
- Following a 2018 tutorial: `exec_()` and short enums still *work* in PySide6, which hides the
  problem until you switch to PyQt6 or a newer PySide6 removes them.
- Looking for `QCameraViewfinder` in Qt6: it's gone.

## Exercise
Port this Qt5 snippet to PySide6:

```python
from PySide2.QtWidgets import QApplication, QAction, QDesktopWidget, QLabel
from PySide2.QtCore import Qt
app = QApplication([])
label = QLabel("hi"); label.setAlignment(Qt.AlignCenter)
w = QDesktopWidget().screenGeometry().width()
app.exec_()
```

🧩 Starter code: [`starter/`](starter/README.md) · ➡️ Answer: [`answers/`](answers/README.md)
