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
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QStatusBar, QVBoxLayout, QWidget)

class Ui_CameraWindow(object):
    def setupUi(self, CameraWindow):
        if not CameraWindow.objectName():
            CameraWindow.setObjectName(u"CameraWindow")
        CameraWindow.resize(800, 560)
        self.centralwidget = QWidget(CameraWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.videoLabel = QLabel(self.centralwidget)
        self.videoLabel.setObjectName(u"videoLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.videoLabel.sizePolicy().hasHeightForWidth())
        self.videoLabel.setSizePolicy(sizePolicy)
        self.videoLabel.setMinimumSize(QSize(320, 240))
        self.videoLabel.setStyleSheet(u"background: #1a202c; color: #a0aec0; border-radius: 8px;")
        self.videoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.mainLayout.addWidget(self.videoLabel)

        self.controlsLayout = QHBoxLayout()
        self.controlsLayout.setObjectName(u"controlsLayout")
        self.cameraSpin = QSpinBox(self.centralwidget)
        self.cameraSpin.setObjectName(u"cameraSpin")
        self.cameraSpin.setMaximum(9)

        self.controlsLayout.addWidget(self.cameraSpin)

        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")

        self.controlsLayout.addWidget(self.startButton)

        self.stopButton = QPushButton(self.centralwidget)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setEnabled(False)

        self.controlsLayout.addWidget(self.stopButton)

        self.controlsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.controlsLayout.addItem(self.controlsSpacer)

        self.mirrorCheck = QCheckBox(self.centralwidget)
        self.mirrorCheck.setObjectName(u"mirrorCheck")
        self.mirrorCheck.setChecked(True)

        self.controlsLayout.addWidget(self.mirrorCheck)

        self.grayCheck = QCheckBox(self.centralwidget)
        self.grayCheck.setObjectName(u"grayCheck")

        self.controlsLayout.addWidget(self.grayCheck)

        self.edgesCheck = QCheckBox(self.centralwidget)
        self.edgesCheck.setObjectName(u"edgesCheck")

        self.controlsLayout.addWidget(self.edgesCheck)

        self.facesCheck = QCheckBox(self.centralwidget)
        self.facesCheck.setObjectName(u"facesCheck")

        self.controlsLayout.addWidget(self.facesCheck)

        self.snapshotButton = QPushButton(self.centralwidget)
        self.snapshotButton.setObjectName(u"snapshotButton")
        self.snapshotButton.setEnabled(False)

        self.controlsLayout.addWidget(self.snapshotButton)

        self.recordButton = QPushButton(self.centralwidget)
        self.recordButton.setObjectName(u"recordButton")
        self.recordButton.setEnabled(False)
        self.recordButton.setCheckable(True)

        self.controlsLayout.addWidget(self.recordButton)


        self.mainLayout.addLayout(self.controlsLayout)

        CameraWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(CameraWindow)
        self.statusbar.setObjectName(u"statusbar")
        CameraWindow.setStatusBar(self.statusbar)

        self.retranslateUi(CameraWindow)

        QMetaObject.connectSlotsByName(CameraWindow)
    # setupUi

    def retranslateUi(self, CameraWindow):
        CameraWindow.setWindowTitle(QCoreApplication.translate("CameraWindow", u"Camera (answer)", None))
        self.videoLabel.setText(QCoreApplication.translate("CameraWindow", u"Camera stopped", None))
        self.cameraSpin.setPrefix(QCoreApplication.translate("CameraWindow", u"Camera ", None))
        self.startButton.setText(QCoreApplication.translate("CameraWindow", u"Start", None))
        self.stopButton.setText(QCoreApplication.translate("CameraWindow", u"Stop", None))
        self.mirrorCheck.setText(QCoreApplication.translate("CameraWindow", u"Mirror", None))
        self.grayCheck.setText(QCoreApplication.translate("CameraWindow", u"Grayscale", None))
        self.edgesCheck.setText(QCoreApplication.translate("CameraWindow", u"Edges", None))
        self.facesCheck.setText(QCoreApplication.translate("CameraWindow", u"Faces", None))
        self.snapshotButton.setText(QCoreApplication.translate("CameraWindow", u"\U0001f4f8 Snapshot", None))
        self.recordButton.setText(QCoreApplication.translate("CameraWindow", u"\u23fa Record", None))
    # retranslateUi

