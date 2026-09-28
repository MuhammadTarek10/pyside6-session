# 03b — Answer

```bash
./build.sh 03_simple_app
python 03_simple_app/b_designer/answers/main.py
```

Steps:
1. `pyside6-designer answers/greeter.ui` → drag a **Check Box** above the buttons.
2. Set `objectName` = `shoutCheck`, `text` = `&Shout` (Alt+S toggles it).
3. Save → `pyside6-uic greeter.ui -o ui_greeter.py`.
4. In `main.py`: `.upper()` when `self.shoutCheck.isChecked()`, and `shoutCheck.toggled.connect(self.greet)`
   so the label updates immediately.

The point of the exercise: **`ui_greeter.py` was regenerated, never edited.** Open the diff of the
generated file and you'll see uic added `self.shoutCheck = QCheckBox(Greeter)` for you.
