# PySide6 Cheatsheet

## Skeleton
```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App")

app = QApplication(sys.argv)     # one per process, before any widget
window = MainWindow()
window.show()
sys.exit(app.exec())             # event loop
```

## With a Designer form
```python
from ui_main_window import Ui_MainWindow        # pyside6-uic main_window.ui -o ui_main_window.py

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)                      # widgets become self.<objectName>
        self.okButton.clicked.connect(self.save)
```

## Tools
| Command | Does |
|---|---|
| `pyside6-designer [file.ui]` | open Qt Designer |
| `pyside6-uic form.ui -o ui_form.py` | .ui → Python |
| `pyside6-rcc resources.qrc -o resources_rc.py` | .qrc → Python (keep the `_rc` name!) |
| `pyside6-deploy main.py` | package as a standalone app (Nuitka) |
| `pyside6-lupdate` / `pyside6-lrelease` / `pyside6-linguist` | translations |

## Common widgets (`PySide6.QtWidgets`)
| Widget | Key API | Key signals |
|---|---|---|
| `QLabel` | `setText`, `setPixmap`, `setAlignment` | `linkActivated` |
| `QPushButton` | `setText`, `setIcon`, `setEnabled` | `clicked` |
| `QLineEdit` | `text()`, `setPlaceholderText`, `setEchoMode` | `textChanged(str)`, `returnPressed`, `editingFinished` |
| `QPlainTextEdit` / `QTextEdit` | `toPlainText()`, `setPlainText` | `textChanged` |
| `QCheckBox` | `isChecked()`, `setChecked` | `toggled(bool)`, `checkStateChanged` |
| `QComboBox` | `addItems`, `currentText()`, `currentIndex()` | `currentIndexChanged(int)`, `currentTextChanged(str)` |
| `QSpinBox` / `QDoubleSpinBox` | `value()`, `setRange` | `valueChanged` |
| `QSlider` | `value()`, `setRange` | `valueChanged(int)` |
| `QProgressBar` | `setValue`, `setRange`, `setFormat("%p%")` | — |
| `QDateEdit` | `date()`, `setCalendarPopup(True)` | `dateChanged` |
| `QListWidget` / `QTableWidget` | item-based (simple) | `itemClicked`, `currentRowChanged` |
| `QListView` / `QTableView` | + a model (Model/View) | `clicked`, `doubleClicked` |
| `QTabWidget`, `QStackedWidget`, `QScrollArea`, `QSplitter`, `QGroupBox` | containers | |

Dialogs: `QMessageBox.information/warning/question(...)`, `QFileDialog.getOpenFileName(...)`,
`QInputDialog.getText(...)`, `QColorDialog.getColor()`.

## Layouts
```python
layout = QVBoxLayout(parent)        # or QHBoxLayout / QGridLayout / QFormLayout
layout.addWidget(w)                 # grid: addWidget(w, row, col, rowSpan, colSpan)
layout.addLayout(other)             # nesting
layout.addStretch()                 # spring
form.addRow("Name:", QLineEdit())   # QFormLayout
```

## Signals and slots
```python
from PySide6.QtCore import QObject, Signal, Slot

class Model(QObject):
    changed = Signal(int)            # declare at class level
    renamed = Signal(str, int)

    @Slot(int)
    def on_value(self, v): ...

model.changed.connect(handler)       # connect (pass the function, don't call it!)
model.changed.connect(lambda v: label.setText(str(v)))
model.changed.emit(42)               # emit
model.changed.disconnect(handler)
```
Connection types: `AutoConnection` (default), `QueuedConnection` (cross-thread), `DirectConnection`.

## QMainWindow parts
```python
self.setCentralWidget(w)
self.menuBar().addMenu("&File").addAction(action)
self.addToolBar("Main").addAction(action)
self.statusBar().showMessage("Ready", 3000)
self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)

from PySide6.QtGui import QAction, QIcon, QKeySequence   # QAction is in QtGui in Qt6
action = QAction(QIcon(":/icons/open.svg"), "&Open", self)
action.setShortcut(QKeySequence.StandardKey.Open)
action.triggered.connect(self.open)
```

## Resources and styles
```python
import resources_rc                       # registers ":/..." paths
QIcon(":/icons/open.svg"); QPixmap(":/images/logo.png")
f = QFile(":/styles/style.qss"); f.open(QFile.OpenModeFlag.ReadOnly); QTextStream(f).readAll()
app.setStyleSheet("QPushButton { border-radius: 6px; } QLabel#title { font-size: 18px; }")
```

## Timers
```python
QTimer.singleShot(1000, self.do_later)
timer = QTimer(self, interval=100); timer.timeout.connect(self.tick); timer.start()
```

## Threads
```python
# One long task: worker object
thread = QThread(); worker = Worker(); worker.moveToThread(thread)
thread.started.connect(worker.run)
worker.progress.connect(bar.setValue)
worker.finished.connect(thread.quit); worker.finished.connect(worker.deleteLater)
thread.finished.connect(thread.deleteLater)
thread.start()
# cancel: thread.requestInterruption()  /  in worker: QThread.currentThread().isInterruptionRequested()

# Many short jobs: pool
class Signals(QObject): done = Signal(object)
class Job(QRunnable):
    def __init__(self): super().__init__(); self.signals = Signals()
    def run(self): self.signals.done.emit(result)
QThreadPool.globalInstance().start(Job())
```
🟥 **Never touch widgets from a worker thread.** Emit a signal instead. `QImage` is OK in threads, `QPixmap` is not.

## Model/View essentials
```python
class M(QAbstractTableModel):
    def rowCount(self, parent=QModelIndex()): ...
    def columnCount(self, parent=QModelIndex()): ...
    def data(self, index, role=Qt.ItemDataRole.DisplayRole): ...
    def headerData(self, section, orientation, role): ...
# change data:  beginInsertRows(...)/endInsertRows(), beginRemoveRows/endRemoveRows,
#               beginResetModel/endResetModel, dataChanged.emit(tl, br)
proxy = QSortFilterProxyModel(); proxy.setSourceModel(model); view.setModel(proxy)
source_index = proxy.mapToSource(view_index)
```

## Settings
```python
app.setOrganizationName("Me"); app.setApplicationName("App")
s = QSettings(); s.setValue("key", value); s.value("key", default, type=int)
```

## Qt6 enum style
`Qt.AlignmentFlag.AlignCenter`, `Qt.ItemDataRole.DisplayRole`, `QMessageBox.StandardButton.Yes`,
`QSizePolicy.Policy.Expanding`: always `Class.EnumName.Value`.
