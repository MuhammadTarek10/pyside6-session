"""Model/View: the data (Task list) lives here; QTableView only displays it."""
from dataclasses import dataclass

from PySide6.QtCore import (
    QDate,
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    QSortFilterProxyModel,
    Qt,
    Signal,
)
from PySide6.QtGui import QBrush, QColor, QFont

PRIORITIES = ["Low", "Medium", "High"]
PRIORITY_COLORS = {"Low": "#2f855a", "Medium": "#b7791f", "High": "#c53030"}

Index = QModelIndex | QPersistentModelIndex


@dataclass
class Task:
    title: str
    priority: str = "Medium"
    due: str = ""  # ISO date "2026-09-27" or "" for no due date
    notes: str = ""
    done: bool = False


class TaskModel(QAbstractTableModel):
    """A table model: rows are tasks, columns are fields."""

    COLUMNS = ["Done", "Title", "Priority", "Due"]
    DONE, TITLE, PRIORITY, DUE = range(4)

    tasks_changed = Signal()  # custom signal: emitted after ANY change to the data

    def __init__(self, tasks: list[Task] | None = None) -> None:
        super().__init__()
        self._tasks: list[Task] = tasks or []
        # one signal to rule them all: any structural or data change → tasks_changed
        for sig in (self.dataChanged, self.rowsInserted, self.rowsRemoved, self.modelReset):
            sig.connect(self.tasks_changed)

    # ---- required overrides -------------------------------------------------
    def rowCount(self, parent: Index = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._tasks)

    def columnCount(self, parent: Index = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self.COLUMNS)

    def data(self, index: Index, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        task = self._tasks[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if col == self.TITLE:
                return task.title
            if col == self.PRIORITY:
                return task.priority
            if col == self.DUE:
                return task.due or "—"
        if role == Qt.ItemDataRole.CheckStateRole and col == self.DONE:
            return Qt.CheckState.Checked if task.done else Qt.CheckState.Unchecked
        if role == Qt.ItemDataRole.ToolTipRole and col == self.TITLE and task.notes:
            return task.notes
        if role == Qt.ItemDataRole.ForegroundRole:
            if task.done:
                return QBrush(QColor("#a0aec0"))
            if col == self.PRIORITY:
                return QBrush(QColor(PRIORITY_COLORS[task.priority]))
            # TODO(exercise 2): overdue due dates in red. Use self.is_overdue(task) on the DUE column
        # TODO(bonus): answer Qt.ItemDataRole.EditRole for the TITLE column (the editor's initial text)
        if role == Qt.ItemDataRole.FontRole and col == self.TITLE and task.done:
            font = QFont()
            font.setStrikeOut(True)
            return font
        if role == Qt.ItemDataRole.UserRole:  # sort key used by the proxy
            return [task.done, task.title.lower(), PRIORITIES.index(task.priority), task.due or "9999"][col]
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.COLUMNS[section]
        return None

    # ---- editing ------------------------------------------------------------
    def flags(self, index: Index) -> Qt.ItemFlag:
        flags = super().flags(index)
        if index.column() == self.DONE:
            flags |= Qt.ItemFlag.ItemIsUserCheckable
        # TODO(bonus): make the TITLE column editable (Qt.ItemFlag.ItemIsEditable)
        return flags

    def setData(self, index: Index, value, role: int = Qt.ItemDataRole.EditRole) -> bool:
        if role == Qt.ItemDataRole.CheckStateRole and index.column() == self.DONE:
            self._tasks[index.row()].done = Qt.CheckState(value) == Qt.CheckState.Checked
            # the whole row changes look (strike-out, colors), so tell views about all columns
            self.dataChanged.emit(index.siblingAtColumn(0), index.siblingAtColumn(self.columnCount() - 1))
            return True
        # TODO(bonus): handle EditRole on the TITLE column: reject empty titles (return False),
        #              otherwise store it, emit dataChanged, return True
        return False

    # ---- our own API (used by the window) -----------------------------------
    def tasks(self) -> list[Task]:
        return list(self._tasks)

    def task(self, row: int) -> Task:
        return self._tasks[row]

    def set_tasks(self, tasks: list[Task]) -> None:
        self.beginResetModel()
        self._tasks = list(tasks)
        self.endResetModel()

    def add_task(self, task: Task) -> None:
        row = len(self._tasks)
        self.beginInsertRows(QModelIndex(), row, row)  # views MUST be told before...
        self._tasks.append(task)
        self.endInsertRows()  # ...and after

    def update_task(self, row: int, task: Task) -> None:
        self._tasks[row] = task
        self.dataChanged.emit(self.index(row, 0), self.index(row, self.columnCount() - 1))

    def remove_task(self, row: int) -> None:
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._tasks[row]
        self.endRemoveRows()

    def remove_done(self) -> int:
        """TODO(exercise 1): remove all completed tasks and return how many were removed.

        Use self.remove_task(row) so views are notified. Think about the ORDER you remove rows in!
        """
        raise NotImplementedError

    @staticmethod
    def is_overdue(task: Task) -> bool:
        """TODO(exercise 2): True if the task is not done, has a due date, and that date is before today.

        Hint: QDate.fromString(task.due, Qt.DateFormat.ISODate) and QDate.currentDate()
        """
        return False

    def counts(self) -> tuple[int, int]:
        return len(self._tasks), sum(t.done for t in self._tasks)


class TaskFilterProxy(QSortFilterProxyModel):
    """Sits between the model and the view: filters by text and status, and sorts."""

    ALL, OPEN, DONE = range(3)

    def __init__(self) -> None:
        super().__init__()
        self._status = self.ALL
        self.setFilterKeyColumn(TaskModel.TITLE)
        self.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setSortRole(Qt.ItemDataRole.UserRole)

    def set_status_filter(self, status: int) -> None:
        self.beginFilterChange()
        self._status = status
        self.endFilterChange(QSortFilterProxyModel.Direction.Rows)

    def filterAcceptsRow(self, source_row: int, source_parent: Index) -> bool:
        if not super().filterAcceptsRow(source_row, source_parent):  # the text filter
            return False
        if self._status == self.ALL:
            return True
        done = self.sourceModel().task(source_row).done
        return done if self._status == self.DONE else not done
