# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'greeter.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Greeter(object):
    def setupUi(self, Greeter):
        if not Greeter.objectName():
            Greeter.setObjectName(u"Greeter")
        Greeter.resize(320, 140)
        self.mainLayout = QVBoxLayout(Greeter)
        self.mainLayout.setObjectName(u"mainLayout")
        self.nameEdit = QLineEdit(Greeter)
        self.nameEdit.setObjectName(u"nameEdit")

        self.mainLayout.addWidget(self.nameEdit)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.setObjectName(u"buttonsLayout")
        self.greetButton = QPushButton(Greeter)
        self.greetButton.setObjectName(u"greetButton")

        self.buttonsLayout.addWidget(self.greetButton)

        self.clearButton = QPushButton(Greeter)
        self.clearButton.setObjectName(u"clearButton")

        self.buttonsLayout.addWidget(self.clearButton)


        self.mainLayout.addLayout(self.buttonsLayout)

        self.resultLabel = QLabel(Greeter)
        self.resultLabel.setObjectName(u"resultLabel")
        self.resultLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.mainLayout.addWidget(self.resultLabel)


        self.retranslateUi(Greeter)
        self.nameEdit.returnPressed.connect(self.greetButton.click)

        QMetaObject.connectSlotsByName(Greeter)
    # setupUi

    def retranslateUi(self, Greeter):
        Greeter.setWindowTitle(QCoreApplication.translate("Greeter", u"Greeter (Designer)", None))
        self.nameEdit.setPlaceholderText(QCoreApplication.translate("Greeter", u"Your name", None))
        self.greetButton.setText(QCoreApplication.translate("Greeter", u"Greet", None))
        self.clearButton.setText(QCoreApplication.translate("Greeter", u"Clear", None))
        self.resultLabel.setText(QCoreApplication.translate("Greeter", u"Type a name and press Greet", None))
    # retranslateUi

