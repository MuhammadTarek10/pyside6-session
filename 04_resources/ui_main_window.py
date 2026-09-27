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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenu,
    QMenuBar, QScrollArea, QSizePolicy, QStatusBar,
    QToolBar, QVBoxLayout, QWidget)
import resources_rc

class Ui_ImageViewer(object):
    def setupUi(self, ImageViewer):
        if not ImageViewer.objectName():
            ImageViewer.setObjectName(u"ImageViewer")
        ImageViewer.resize(800, 600)
        icon = QIcon()
        icon.addFile(u":/images/logo.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        ImageViewer.setWindowIcon(icon)
        self.actionOpen = QAction(ImageViewer)
        self.actionOpen.setObjectName(u"actionOpen")
        icon1 = QIcon()
        icon1.addFile(u":/icons/open.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionOpen.setIcon(icon1)
        self.actionZoomIn = QAction(ImageViewer)
        self.actionZoomIn.setObjectName(u"actionZoomIn")
        icon2 = QIcon()
        icon2.addFile(u":/icons/zoom-in.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionZoomIn.setIcon(icon2)
        self.actionZoomOut = QAction(ImageViewer)
        self.actionZoomOut.setObjectName(u"actionZoomOut")
        icon3 = QIcon()
        icon3.addFile(u":/icons/zoom-out.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionZoomOut.setIcon(icon3)
        self.actionFit = QAction(ImageViewer)
        self.actionFit.setObjectName(u"actionFit")
        icon4 = QIcon()
        icon4.addFile(u":/icons/fit.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionFit.setIcon(icon4)
        self.actionAbout = QAction(ImageViewer)
        self.actionAbout.setObjectName(u"actionAbout")
        icon5 = QIcon()
        icon5.addFile(u":/icons/about.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionAbout.setIcon(icon5)
        self.actionQuit = QAction(ImageViewer)
        self.actionQuit.setObjectName(u"actionQuit")
        icon6 = QIcon()
        icon6.addFile(u":/icons/quit.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionQuit.setIcon(icon6)
        self.centralwidget = QWidget(ImageViewer)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralLayout = QVBoxLayout(self.centralwidget)
        self.centralLayout.setObjectName(u"centralLayout")
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageLabel = QLabel()
        self.imageLabel.setObjectName(u"imageLabel")
        self.imageLabel.setGeometry(QRect(0, 0, 200, 200))
        self.imageLabel.setPixmap(QPixmap(u":/images/logo.svg"))
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scrollArea.setWidget(self.imageLabel)

        self.centralLayout.addWidget(self.scrollArea)

        ImageViewer.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(ImageViewer)
        self.menubar.setObjectName(u"menubar")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        ImageViewer.setMenuBar(self.menubar)
        self.toolBar = QToolBar(ImageViewer)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setIconSize(QSize(24, 24))
        ImageViewer.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.statusbar = QStatusBar(ImageViewer)
        self.statusbar.setObjectName(u"statusbar")
        ImageViewer.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuView.addAction(self.actionZoomIn)
        self.menuView.addAction(self.actionZoomOut)
        self.menuView.addAction(self.actionFit)
        self.menuHelp.addAction(self.actionAbout)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionZoomIn)
        self.toolBar.addAction(self.actionZoomOut)
        self.toolBar.addAction(self.actionFit)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAbout)

        self.retranslateUi(ImageViewer)
        self.actionQuit.triggered.connect(ImageViewer.close)

        QMetaObject.connectSlotsByName(ImageViewer)
    # setupUi

    def retranslateUi(self, ImageViewer):
        ImageViewer.setWindowTitle(QCoreApplication.translate("ImageViewer", u"Image Viewer", None))
        self.actionOpen.setText(QCoreApplication.translate("ImageViewer", u"&Open\u2026", None))
#if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("ImageViewer", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionZoomIn.setText(QCoreApplication.translate("ImageViewer", u"Zoom &In", None))
#if QT_CONFIG(shortcut)
        self.actionZoomIn.setShortcut(QCoreApplication.translate("ImageViewer", u"Ctrl++", None))
#endif // QT_CONFIG(shortcut)
        self.actionZoomOut.setText(QCoreApplication.translate("ImageViewer", u"Zoom &Out", None))
#if QT_CONFIG(shortcut)
        self.actionZoomOut.setShortcut(QCoreApplication.translate("ImageViewer", u"Ctrl+-", None))
#endif // QT_CONFIG(shortcut)
        self.actionFit.setText(QCoreApplication.translate("ImageViewer", u"&Fit to Window", None))
#if QT_CONFIG(shortcut)
        self.actionFit.setShortcut(QCoreApplication.translate("ImageViewer", u"Ctrl+0", None))
#endif // QT_CONFIG(shortcut)
        self.actionAbout.setText(QCoreApplication.translate("ImageViewer", u"&About", None))
#if QT_CONFIG(shortcut)
        self.actionAbout.setShortcut(QCoreApplication.translate("ImageViewer", u"F1", None))
#endif // QT_CONFIG(shortcut)
        self.actionQuit.setText(QCoreApplication.translate("ImageViewer", u"&Quit", None))
#if QT_CONFIG(shortcut)
        self.actionQuit.setShortcut(QCoreApplication.translate("ImageViewer", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.menuFile.setTitle(QCoreApplication.translate("ImageViewer", u"&File", None))
        self.menuView.setTitle(QCoreApplication.translate("ImageViewer", u"&View", None))
        self.menuHelp.setTitle(QCoreApplication.translate("ImageViewer", u"&Help", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("ImageViewer", u"Main toolbar", None))
    # retranslateUi

