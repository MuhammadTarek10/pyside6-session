# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QDockWidget,
    QHeaderView, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QSpacerItem, QStatusBar,
    QTableView, QToolBar, QVBoxLayout, QWidget)
import resources_rc

class Ui_TodoWindow(object):
    def setupUi(self, TodoWindow):
        if not TodoWindow.objectName():
            TodoWindow.setObjectName(u"TodoWindow")
        TodoWindow.resize(820, 520)
        icon = QIcon()
        icon.addFile(u":/icons/app.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        TodoWindow.setWindowIcon(icon)
        self.actionNew = QAction(TodoWindow)
        self.actionNew.setObjectName(u"actionNew")
        icon1 = QIcon()
        icon1.addFile(u":/icons/add.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionNew.setIcon(icon1)
        self.actionEdit = QAction(TodoWindow)
        self.actionEdit.setObjectName(u"actionEdit")
        icon2 = QIcon()
        icon2.addFile(u":/icons/edit.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionEdit.setIcon(icon2)
        self.actionDelete = QAction(TodoWindow)
        self.actionDelete.setObjectName(u"actionDelete")
        icon3 = QIcon()
        icon3.addFile(u":/icons/delete.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionDelete.setIcon(icon3)
        self.actionQuit = QAction(TodoWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.centralwidget = QWidget(TodoWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralLayout = QVBoxLayout(self.centralwidget)
        self.centralLayout.setObjectName(u"centralLayout")
        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableView.setSortingEnabled(True)
        self.tableView.horizontalHeader().setStretchLastSection(False)
        self.tableView.verticalHeader().setVisible(False)

        self.centralLayout.addWidget(self.tableView)

        TodoWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(TodoWindow)
        self.menubar.setObjectName(u"menubar")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuTask = QMenu(self.menubar)
        self.menuTask.setObjectName(u"menuTask")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        TodoWindow.setMenuBar(self.menubar)
        self.toolBar = QToolBar(TodoWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        TodoWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.statusbar = QStatusBar(TodoWindow)
        self.statusbar.setObjectName(u"statusbar")
        TodoWindow.setStatusBar(self.statusbar)
        self.filterDock = QDockWidget(TodoWindow)
        self.filterDock.setObjectName(u"filterDock")
        self.filterDockContents = QWidget()
        self.filterDockContents.setObjectName(u"filterDockContents")
        self.filterLayout = QVBoxLayout(self.filterDockContents)
        self.filterLayout.setObjectName(u"filterLayout")
        self.searchEdit = QLineEdit(self.filterDockContents)
        self.searchEdit.setObjectName(u"searchEdit")
        self.searchEdit.setClearButtonEnabled(True)

        self.filterLayout.addWidget(self.searchEdit)

        self.statusCombo = QComboBox(self.filterDockContents)
        self.statusCombo.addItem("")
        self.statusCombo.addItem("")
        self.statusCombo.addItem("")
        self.statusCombo.setObjectName(u"statusCombo")

        self.filterLayout.addWidget(self.statusCombo)

        self.filterSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.filterLayout.addItem(self.filterSpacer)

        self.filterDock.setWidget(self.filterDockContents)
        TodoWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.filterDock)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTask.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menuFile.addAction(self.actionQuit)
        self.menuTask.addAction(self.actionNew)
        self.menuTask.addAction(self.actionEdit)
        self.menuTask.addAction(self.actionDelete)
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionEdit)
        self.toolBar.addAction(self.actionDelete)

        self.retranslateUi(TodoWindow)
        self.actionQuit.triggered.connect(TodoWindow.close)

        QMetaObject.connectSlotsByName(TodoWindow)
    # setupUi

    def retranslateUi(self, TodoWindow):
        TodoWindow.setWindowTitle(QCoreApplication.translate("TodoWindow", u"Todo Manager (starter)", None))
        self.actionNew.setText(QCoreApplication.translate("TodoWindow", u"&New Task\u2026", None))
#if QT_CONFIG(shortcut)
        self.actionNew.setShortcut(QCoreApplication.translate("TodoWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionEdit.setText(QCoreApplication.translate("TodoWindow", u"&Edit\u2026", None))
#if QT_CONFIG(shortcut)
        self.actionEdit.setShortcut(QCoreApplication.translate("TodoWindow", u"Ctrl+E", None))
#endif // QT_CONFIG(shortcut)
        self.actionDelete.setText(QCoreApplication.translate("TodoWindow", u"&Delete", None))
#if QT_CONFIG(shortcut)
        self.actionDelete.setShortcut(QCoreApplication.translate("TodoWindow", u"Del", None))
#endif // QT_CONFIG(shortcut)
        self.actionQuit.setText(QCoreApplication.translate("TodoWindow", u"&Quit", None))
#if QT_CONFIG(shortcut)
        self.actionQuit.setShortcut(QCoreApplication.translate("TodoWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.menuFile.setTitle(QCoreApplication.translate("TodoWindow", u"&File", None))
        self.menuTask.setTitle(QCoreApplication.translate("TodoWindow", u"&Task", None))
        self.menuView.setTitle(QCoreApplication.translate("TodoWindow", u"&View", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("TodoWindow", u"Toolbar", None))
        self.filterDock.setWindowTitle(QCoreApplication.translate("TodoWindow", u"Filter", None))
        self.searchEdit.setPlaceholderText(QCoreApplication.translate("TodoWindow", u"Search titles\u2026", None))
        self.statusCombo.setItemText(0, QCoreApplication.translate("TodoWindow", u"All tasks", None))
        self.statusCombo.setItemText(1, QCoreApplication.translate("TodoWindow", u"Open", None))
        self.statusCombo.setItemText(2, QCoreApplication.translate("TodoWindow", u"Done", None))

    # retranslateUi

