# PySide6 Session

A hands-on tour of building desktop apps with **PySide6** (Qt for Python), from "what even is
this?" to threads and a live camera feed.

Each folder is a **standalone step** with its own `README.md` (concepts, walkthrough, common
mistakes, exercise). Read them in order.

## Agenda

| # | Topic | Folder | ~Time |
|---|---|---|---|
| 1 | PyQt vs PySide | [`01_pyqt_vs_pyside`](01_pyqt_vs_pyside/README.md) | 10 min |
| 2 | Qt5 (PyQt5/PySide2) vs Qt6 (PyQt6/PySide6) | [`02_qt5_vs_qt6`](02_qt5_vs_qt6/README.md) | 10 min |
| 3 | Simple app: a) code only, b) Qt Designer | [`03_simple_app`](03_simple_app/a_code_only/README.md) | 25 min |
| 4 | App with resources (icons, images, QSS) | [`04_resources`](04_resources/README.md) | 20 min |
| 5 | More complex app: Todo manager (Model/View, dialogs, QSettings) | [`05_todo_app`](05_todo_app/README.md) | 35 min |
| 6 | Threads: a) frozen UI, b) QThread worker, c) QThreadPool | [`06_threads`](06_threads/a_frozen_ui/README.md) | 30 min |
| 7 | Camera with OpenCV + QThread | [`07_camera`](07_camera/README.md) | 20 min |

Quick reference: [`CHEATSHEET.md`](CHEATSHEET.md)

**Exercises:** every step's README ends with an *Exercise*, and its solution lives in that step's
`answers/` folder (runnable code + a README explaining the solution and a review checklist).

## Setup

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt   # PySide6 6.11, opencv-python
```

Check it:
```bash
python -c "import PySide6; print(PySide6.__version__)"
pyside6-designer                  # Qt Designer ships with PySide6
```

**macOS camera permission (topic 7):** System Settings → Privacy & Security → Camera → allow your
terminal/IDE, then restart it.

## Running a step
Run each app from the repo root. Imports are relative to each file's folder, which Python adds automatically:
```bash
python 03_simple_app/a_code_only/main.py
python 05_todo_app/main.py
```

## `.ui` and `.qrc` files → Python

Forms are made in **Qt Designer** (`*.ui`) and assets are listed in **resource files** (`*.qrc`).
They're compiled to Python, and the generated files are **committed**, so every step runs right away.

```bash
./build.sh                  # regenerate everything
./build.sh 04_resources     # only one folder
```
which runs, for each file:
```bash
pyside6-uic  main_window.ui -o ui_main_window.py
pyside6-rcc  resources.qrc  -o resources_rc.py     # name MUST be <qrc>_rc.py (see topic 4)
```
**Never edit `ui_*.py` or `*_rc.py` by hand.** Edit the `.ui`/`.qrc` and rebuild.

## Repo layout
```
01_pyqt_vs_pyside/   notes + same app in PyQt6 (read-only) and PySide6
02_qt5_vs_qt6/       notes + same app in Qt5 style (read-only) and Qt6 style
03_simple_app/       a_code_only/  b_designer/
04_resources/        image viewer: icons/, images/, styles/, resources.qrc
05_todo_app/         models.py, storage.py, 2 Designer forms
06_threads/          a_frozen_ui/  b_qthread_worker/  c_threadpool/
07_camera/           camera_worker.py + Designer form
build.sh             uic/rcc for all folders
CHEATSHEET.md
```
