# 03a — Starter

This is a copy of `../main.py` with `TODO(exercise)` markers. It runs as-is:
```bash
python 03_simple_app/a_code_only/starter/main.py
```

## Tasks
1. Add a `QComboBox` named `self.greeting_combo` with **Hello / Hi / Welcome**, placed next to the name field.
2. `greet()` uses the selected greeting.
3. *Optional:* changing the combo re-greets immediately.
4. **Bonus:** the Clear button is disabled while the field is empty.

Hints: `addItems([...])`, `currentText()`, `currentTextChanged`, `QHBoxLayout`, `layout.addLayout(...)`.

Check your work: `diff main.py ../answers/main.py`
