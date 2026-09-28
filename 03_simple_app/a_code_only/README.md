# 03a — Simple app, code only

A greeter: type a name, press **Greet**, see a message. Everything is built in Python so you can
see every moving part.

```bash
python 03_simple_app/a_code_only/main.py
```

## Concepts

### 1. `QApplication` and the event loop
```python
app = QApplication(sys.argv)
...
sys.exit(app.exec())
```
- There is **exactly one** `QApplication` per process, and it must be created before any widget.
- `app.exec()` starts the **event loop**: an endless loop of *wait for event (click, key,
  repaint, timer) → dispatch it → repeat*. Your code only runs when an event calls it.
- It returns when the last window closes. `sys.exit(...)` passes the exit code on.

### 2. Widgets
Everything visible is a `QWidget`. A widget with **no parent** becomes a window.
Here `Greeter(QWidget)` is our window, and `QLineEdit`, `QPushButton` and `QLabel` are children.

### 3. Layouts
`QVBoxLayout` (vertical), `QHBoxLayout` (horizontal), `QGridLayout`, `QFormLayout`.
Layouts position and resize children automatically, and they **take ownership** (set the parent) of the
widgets you add. Layouts can nest: `layout.addLayout(buttons)`.

### 4. Signals and slots
Qt's observer pattern:
```python
self.greet_button.clicked.connect(self.greet)       # signal → slot
self.name_edit.textChanged.connect(self.on_text_changed)  # signal carries a str
```
- A **signal** is emitted when something happens (`clicked`, `textChanged`, `returnPressed`).
- A **slot** is any callable: a method, a function or a lambda. `@Slot()` is optional but
  documents intent and is slightly faster.
- One signal → many slots, and many signals → one slot (both Enter and the button call `greet`).

## Object tree / memory
Parents own their children. When the window is destroyed, all its children go with it.
That's why we keep `self.name_edit` as an attribute: we need it later, not to keep it alive.

## Common mistakes
- Creating widgets before `QApplication` → `QWidget: Must construct a QApplication before a QWidget`.
- `button.clicked.connect(self.greet())` ← **calls** greet immediately and connects its `None` result.
  Pass the function itself: `connect(self.greet)`.
- Forgetting `window.show()` → the app runs but nothing appears.
- Creating a window as a local variable in a function that returns: Python garbage-collects it
  and the window flashes and disappears.
- Long work inside a slot freezes the UI (→ topic 6).

## Exercise
Add a `QComboBox` with "Hello / Hi / Welcome" and use the selected greeting.
Bonus: disable **Clear** when the field is empty.

➡️ Answer: [`answers/`](answers/README.md)
