# 03b — Starter

A copy of the Designer greeter. It runs as-is:
```bash
./build.sh 03_simple_app          # generates starter/ui_greeter.py
python 03_simple_app/b_designer/starter/main.py
```

## Tasks
1. **Designer:** `pyside6-designer 03_simple_app/b_designer/starter/greeter.ui`
   - Drag a **Check Box** above the buttons.
   - `objectName` = **`shoutCheck`** (the code expects this exact name), `text` = `&Shout`.
   - Save.
2. Regenerate: `./build.sh 03_simple_app` (or `pyside6-uic greeter.ui -o ui_greeter.py`).
3. **Code** (`main.py`, see the TODOs): upper-case the greeting when the box is checked, and re-greet on toggle.

🚫 Don't edit `ui_greeter.py`.

Check your work: `diff greeter.ui ../answers/greeter.ui` and `diff main.py ../answers/main.py`
