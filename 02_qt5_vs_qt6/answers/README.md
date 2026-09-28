# 02 — Answer: porting the Qt5 snippet

```python
# Qt5 (PySide2)                                   # Qt6 (PySide6)
from PySide2.QtWidgets import QApplication, \     from PySide6.QtWidgets import QApplication, QLabel
    QAction, QDesktopWidget, QLabel               from PySide6.QtGui import QAction          # moved to QtGui
from PySide2.QtCore import Qt                     from PySide6.QtCore import Qt
app = QApplication([])                            app = QApplication([])
label.setAlignment(Qt.AlignCenter)                label.setAlignment(Qt.AlignmentFlag.AlignCenter)   # full enum
w = QDesktopWidget().screenGeometry().width()     w = app.primaryScreen().geometry().width()        # QScreen
app.exec_()                                       app.exec()
```

Five changes: **import package**, **QAction → QtGui**, **fully-qualified enum**, **QDesktopWidget → QScreen**, **exec_ → exec**.

Run the ported version:
```bash
python 02_qt5_vs_qt6/answers/ported.py
```
