# 03b — Simple app with Qt Designer

The same greeter as 03a, but the **UI is drawn in Qt Designer** and compiled to Python.

```bash
pyside6-designer 03_simple_app/b_designer/greeter.ui   # open or edit it
./build.sh 03_simple_app                                # regenerate ui_greeter.py
python 03_simple_app/b_designer/main.py
```

## The workflow

```
 greeter.ui  ──pyside6-uic──►  ui_greeter.py  ──import──►  main.py
 (XML, edited   (generated Python,          (your code:
  in Designer)   DO NOT EDIT)                behavior only)
```

1. **Designer**: create a *Widget* form, drop a Line Edit, two Push Buttons and a Label.
   Select the form and use **Lay Out Vertically** (Ctrl+L). Put the buttons in a horizontal layout.
2. **Name every widget** you'll touch from code (`objectName`: `nameEdit`, `greetButton` …).
   These names become Python attributes.
3. Save → `greeter.ui` (plain XML: open it and look!)
4. `pyside6-uic greeter.ui -o ui_greeter.py`
5. In code, inherit from the generated class and call `setupUi(self)`.

## What does uic generate?
Open `ui_greeter.py`. It's a plain class with **no Qt base class**:

```python
class Ui_Greeter(object):
    def setupUi(self, Greeter):
        self.mainLayout = QVBoxLayout(Greeter)
        self.nameEdit = QLineEdit(Greeter)
        ...
    def retranslateUi(self, Greeter):   # all user-visible strings, for i18n
        ...
```
It's exactly the code we wrote by hand in 03a. Designer just writes it for you.

## Multiple-inheritance pattern (used in this session)
```python
class Greeter(QWidget, Ui_Greeter):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.greetButton.clicked.connect(self.greet)
```
The alternative is *composition*: `self.ui = Ui_Greeter(); self.ui.setupUi(self)` → `self.ui.greetButton`.
Both are fine. Pick one per project.

## Connections in Designer
The Signal/Slot editor (F4) can wire widget-to-widget connections with no code.
This file does `nameEdit.returnPressed() → greetButton.click()`. Look for
`QObject.connect` / `.connect(` in the generated file.

## Common mistakes
- **Editing `ui_greeter.py`**: your changes are erased the next time you run uic. Put logic in `main.py`.
- Forgetting to rerun uic after changing the `.ui` → "my change doesn't show up".
- Leaving default names (`pushButton_2`) → unreadable code. Rename in Designer.
- No top-level layout on the form → widgets don't resize (Designer shows a red "broken layout" icon).

> **Heads-up about method names:** `setupUi()` calls `QMetaObject.connectSlotsByName()`, which
> auto-connects methods named `on_<objectName>_<signal>` (e.g. `on_greetButton_clicked`). It's handy,
> but it's implicit and it warns about any `on_…` method that doesn't match. In this repo we connect
> explicitly and avoid the `on_` prefix.

## Exercise
In Designer, add a `QCheckBox` "Shout" (`shoutCheck`). Regenerate, then make `greet()` use
`.upper()` when it's checked. **Do not touch `ui_greeter.py`.**
