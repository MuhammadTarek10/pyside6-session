# 04 — Answer: Rotate + Dark mode

```bash
./build.sh 04_resources
python 04_resources/answers/main.py
```
This folder is a full copy of the app with the exercise done. The new files are
`icons/rotate.svg`, `icons/dark.svg` and `styles/dark.qss`.

## 1. Rotate action: the full resource round-trip
1. Add `icons/rotate.svg`.
2. Register it in `resources.qrc`:
   ```xml
   <file alias="rotate.svg">icons/rotate.svg</file>
   ```
3. In Designer, reload the Resource Browser (🔄), create `actionRotate` in the Action Editor, set its icon
   → *Choose Resource…* → `rotate.svg`, and drag it to the View menu and the toolbar.
4. `./build.sh` (rcc **and** uic).
5. Code:
   ```python
   self.actionRotate.triggered.connect(self.rotate)

   def rotate(self):
       self._pixmap = self._pixmap.transformed(QTransform().rotate(90), Qt.TransformationMode.SmoothTransformation)
       self._render()
   ```
   We rotate the **original** pixmap, not the scaled one, so quality doesn't degrade.

## 2. Dark mode: a checkable action + swapping stylesheets
- In Designer, set `actionDarkMode` → `checkable = true`. A checkable action emits `toggled(bool)`, and the
  toolbar button stays pressed while it's on (styled with `QToolButton:checked` in `dark.qss`).
- ```python
  self.actionDarkMode.toggled.connect(self.set_dark_mode)

  def set_dark_mode(self, on: bool):
      qss = ":/styles/dark.qss" if on else ":/styles/style.qss"
      QApplication.instance().setStyleSheet(load_stylesheet(qss))
  ```
- `setStyleSheet` on the **app** restyles every widget immediately, including dialogs opened later.

## Checklist to review attendees' answers
- [ ] New files are in `resources.qrc`, and the code uses `:/…` paths (no `icons/rotate.svg` relative paths)
- [ ] `resources_rc.py` was regenerated (otherwise the icon is blank)
- [ ] Nobody edited `ui_main_window.py` or `resources_rc.py` by hand
- [ ] Dark mode uses `toggled(bool)`, not `triggered` + a manual flag
