"""Starter for exercise 5: Clear completed, overdue dates, inline editing (see README.md here).

Regenerate after editing .ui/.qrc files:  ./build.sh 05_todo_app
"""
import sys
from pathlib import Path

from PySide6.QtCore import QDate, QSettings, Qt, Slot
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHeaderView,
    QMainWindow,
    QMessageBox,
    QWidget,
)

from models import Task, TaskFilterProxy, TaskModel
from storage import load_tasks, save_tasks
from ui_main_window import Ui_TodoWindow
from ui_task_dialog import Ui_TaskDialog

DATA_FILE = Path(__file__).with_name("tasks.json")

SAMPLE_TASKS = [
    Task("Prepare PySide6 session", "High", QDate.currentDate().toString(Qt.DateFormat.ISODate)),
    Task("Install Qt Designer", "Medium", done=True),
    Task("Try the camera demo", "Low", notes="Grant camera permission to the terminal on macOS"),
    Task("File the report", "High", QDate.currentDate().addDays(-3).toString(Qt.DateFormat.ISODate)),  # overdue
]


class TaskDialog(QDialog, Ui_TaskDialog):
    """Add/edit dialog. Use get_task() after exec() returns Accepted."""

    def __init__(self, parent: QWidget | None = None, task: Task | None = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.dueEdit.setDate(QDate.currentDate())
        self.titleEdit.textChanged.connect(self._validate)

        self._done = False
        if task:
            self.setWindowTitle("Edit task")
            self.titleEdit.setText(task.title)
            self.priorityCombo.setCurrentText(task.priority)
            self.dueCheck.setChecked(bool(task.due))
            if task.due:
                self.dueEdit.setDate(QDate.fromString(task.due, Qt.DateFormat.ISODate))
            self.notesEdit.setPlainText(task.notes)
            self._done = task.done
        else:
            self.setWindowTitle("New task")
            self.priorityCombo.setCurrentText("Medium")
        self._validate()

    @Slot()
    def _validate(self) -> None:
        ok = self.buttonBox.button(self.buttonBox.StandardButton.Ok)
        ok.setEnabled(bool(self.titleEdit.text().strip()))

    def get_task(self) -> Task:
        return Task(
            title=self.titleEdit.text().strip(),
            priority=self.priorityCombo.currentText(),
            due=self.dueEdit.date().toString(Qt.DateFormat.ISODate) if self.dueCheck.isChecked() else "",
            notes=self.notesEdit.toPlainText().strip(),
            done=self._done,
        )


class TodoWindow(QMainWindow, Ui_TodoWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        # --- Model/View wiring:  TaskModel -> TaskFilterProxy -> QTableView
        tasks = load_tasks(DATA_FILE) if DATA_FILE.exists() else SAMPLE_TASKS
        self.model = TaskModel(tasks)
        self.proxy = TaskFilterProxy()
        self.proxy.setSourceModel(self.model)
        self.tableView.setModel(self.proxy)
        self.tableView.sortByColumn(TaskModel.DUE, Qt.SortOrder.AscendingOrder)

        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(TaskModel.TITLE, QHeaderView.ResizeMode.Stretch)

        # --- Actions
        self.actionNew.triggered.connect(self.new_task)
        self.actionEdit.triggered.connect(self.edit_task)
        self.actionDelete.triggered.connect(self.delete_task)
        # TODO(exercise 1): add actionClearCompleted to the Task menu in Designer, rebuild,
        #                   then connect it to self.clear_completed
        self.tableView.doubleClicked.connect(self.edit_task)
        self.menuView.addAction(self.filterDock.toggleViewAction())  # free "show/hide dock" action
        self.menuView.addAction(self.toolBar.toggleViewAction())

        # --- Filters (dock widget)
        self.searchEdit.textChanged.connect(self.proxy.setFilterFixedString)
        self.statusCombo.currentIndexChanged.connect(self.proxy.set_status_filter)

        # --- Our custom signal: any data change -> save + refresh status bar
        self.model.tasks_changed.connect(self.refresh_after_change)
        self.tableView.selectionModel().selectionChanged.connect(self.update_actions)

        self.restore_settings()
        self.refresh_after_change()
        self.update_actions()

    # ---- helpers --------------------------------------------------------------
    def selected_source_row(self) -> int | None:
        rows = self.tableView.selectionModel().selectedRows()
        if not rows:
            return None
        # the view shows PROXY indexes; the model needs SOURCE rows
        return self.proxy.mapToSource(rows[0]).row()

    # ---- slots ----------------------------------------------------------------
    @Slot()
    def new_task(self) -> None:
        dialog = TaskDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.model.add_task(dialog.get_task())

    @Slot()
    def edit_task(self) -> None:
        row = self.selected_source_row()
        if row is None:
            return
        dialog = TaskDialog(self, self.model.task(row))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.model.update_task(row, dialog.get_task())

    @Slot()
    def delete_task(self) -> None:
        row = self.selected_source_row()
        if row is None:
            return
        title = self.model.task(row).title
        answer = QMessageBox.question(self, "Delete task", f"Delete “{title}”?")
        if answer == QMessageBox.StandardButton.Yes:
            self.model.remove_task(row)

    @Slot()
    def clear_completed(self) -> None:
        # TODO(exercise 1): if nothing is done, show a status bar message and return.
        #                   Otherwise ask with QMessageBox.question, then call self.model.remove_done()
        raise NotImplementedError

    @Slot()
    def refresh_after_change(self) -> None:
        save_tasks(DATA_FILE, self.model.tasks())
        total, done = self.model.counts()
        self.statusbar.showMessage(f"{total} tasks · {done} done · {total - done} open")

    @Slot()
    def update_actions(self) -> None:
        has_selection = self.selected_source_row() is not None
        self.actionEdit.setEnabled(has_selection)
        self.actionDelete.setEnabled(has_selection)
        # TODO(exercise 1, optional): enable actionClearCompleted only when some task is done
        #                             (and call update_actions() from refresh_after_change)

    # ---- QSettings: remember window geometry, dock/toolbar layout, filter ----
    def restore_settings(self) -> None:
        settings = QSettings()
        if geometry := settings.value("window/geometry"):
            self.restoreGeometry(geometry)
        if state := settings.value("window/state"):
            self.restoreState(state)
        self.statusCombo.setCurrentIndex(int(settings.value("filter/status", 0)))

    def closeEvent(self, event: QCloseEvent) -> None:
        settings = QSettings()
        settings.setValue("window/geometry", self.saveGeometry())
        settings.setValue("window/state", self.saveState())
        settings.setValue("filter/status", self.statusCombo.currentIndex())
        super().closeEvent(event)


def main() -> None:
    app = QApplication(sys.argv)
    # QSettings() with no args uses these to pick the storage location
    # (macOS: ~/Library/Preferences/com.pyside-session.Todo Manager.plist)
    app.setOrganizationName("pyside-session")
    app.setOrganizationDomain("pyside-session.local")
    app.setApplicationName("Todo Manager (starter)")

    window = TodoWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
