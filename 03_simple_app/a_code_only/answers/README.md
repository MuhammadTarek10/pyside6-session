# 03a — Answer

```bash
python 03_simple_app/a_code_only/answers/main.py
```

What changed compared to `../main.py`:
1. **`QComboBox`** with `addItems([...])`, read with `currentText()`.
2. The combo and the line edit sit in a `QHBoxLayout`. `stretch=1` lets the line edit take the extra width.
3. `greeting_combo.currentTextChanged.connect(self.greet)` → switching the greeting updates the message live.
   `greet()` ignores the call if the name is empty, so this is safe.
4. **Bonus:** `update_buttons()` enables Clear only when there's text. One slot can manage several widgets' state.

Discussion: `currentTextChanged` emits a `str`, but `greet()` takes no argument. PySide drops extra
signal arguments when the slot accepts fewer, so this just works.
