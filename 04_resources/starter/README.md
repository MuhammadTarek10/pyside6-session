# 04 — Starter

A copy of the image viewer. It runs as-is:
```bash
./build.sh 04_resources
python 04_resources/starter/main.py
```
Already provided: `icons/rotate.svg`, `icons/dark.svg` (in the folder but **not** registered yet), and
a stub `styles/dark.qss`.

## Exercise 1: Rotate
1. Register `icons/rotate.svg` in `resources.qrc` under the `/icons` prefix (`alias="rotate.svg"`).
2. `pyside6-designer 04_resources/starter/main_window.ui`
   → Resource Browser → 🔄 reload → Action Editor → new action **`actionRotate`**, text `&Rotate`,
   shortcut `Ctrl+R`, icon → *Choose Resource…* → `rotate.svg`. Drag it to the View menu and the toolbar. Save.
3. `./build.sh 04_resources` (rcc **and** uic)
4. `main.py`: implement `rotate()` and connect `actionRotate.triggered` to it.

## Exercise 2: Dark mode
1. Finish `styles/dark.qss`, and register it (and `icons/dark.svg`) in `resources.qrc`.
2. Designer: a new action **`actionDarkMode`**, **checkable = true**, icon `dark.svg`, shortcut `Ctrl+D`.
3. Rebuild, implement `set_dark_mode(on)`, and connect `actionDarkMode.toggled` to it.

Use the exact `objectName`s above, since the TODOs refer to them.

Check your work: `diff -r . ../answers -x '*_rc.py' -x 'ui_*.py' -x README.md -x __pycache__`
