# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'task_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDateEdit, QDialog, QDialogButtonBox, QFormLayout,
    QLabel, QLineEdit, QPlainTextEdit, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_TaskDialog(object):
    def setupUi(self, TaskDialog):
        if not TaskDialog.objectName():
            TaskDialog.setObjectName(u"TaskDialog")
        TaskDialog.resize(400, 300)
        TaskDialog.setModal(True)
        self.mainLayout = QVBoxLayout(TaskDialog)
        self.mainLayout.setObjectName(u"mainLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.titleLabel = QLabel(TaskDialog)
        self.titleLabel.setObjectName(u"titleLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.titleLabel)

        self.titleEdit = QLineEdit(TaskDialog)
        self.titleEdit.setObjectName(u"titleEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.titleEdit)

        self.priorityLabel = QLabel(TaskDialog)
        self.priorityLabel.setObjectName(u"priorityLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.priorityLabel)

        self.priorityCombo = QComboBox(TaskDialog)
        self.priorityCombo.addItem("")
        self.priorityCombo.addItem("")
        self.priorityCombo.addItem("")
        self.priorityCombo.setObjectName(u"priorityCombo")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.priorityCombo)

        self.dueCheck = QCheckBox(TaskDialog)
        self.dueCheck.setObjectName(u"dueCheck")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.dueCheck)

        self.dueEdit = QDateEdit(TaskDialog)
        self.dueEdit.setObjectName(u"dueEdit")
        self.dueEdit.setEnabled(False)
        self.dueEdit.setCalendarPopup(True)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.dueEdit)

        self.notesLabel = QLabel(TaskDialog)
        self.notesLabel.setObjectName(u"notesLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.notesLabel)

        self.notesEdit = QPlainTextEdit(TaskDialog)
        self.notesEdit.setObjectName(u"notesEdit")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.notesEdit)


        self.mainLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(TaskDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.mainLayout.addWidget(self.buttonBox)

#if QT_CONFIG(shortcut)
        self.titleLabel.setBuddy(self.titleEdit)
        self.priorityLabel.setBuddy(self.priorityCombo)
        self.notesLabel.setBuddy(self.notesEdit)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(TaskDialog)
        self.buttonBox.accepted.connect(TaskDialog.accept)
        self.buttonBox.rejected.connect(TaskDialog.reject)
        self.dueCheck.toggled.connect(self.dueEdit.setEnabled)

        QMetaObject.connectSlotsByName(TaskDialog)
    # setupUi

    def retranslateUi(self, TaskDialog):
        TaskDialog.setWindowTitle(QCoreApplication.translate("TaskDialog", u"Task", None))
        self.titleLabel.setText(QCoreApplication.translate("TaskDialog", u"&Title", None))
        self.titleEdit.setPlaceholderText(QCoreApplication.translate("TaskDialog", u"What needs doing?", None))
        self.priorityLabel.setText(QCoreApplication.translate("TaskDialog", u"&Priority", None))
        self.priorityCombo.setItemText(0, QCoreApplication.translate("TaskDialog", u"Low", None))
        self.priorityCombo.setItemText(1, QCoreApplication.translate("TaskDialog", u"Medium", None))
        self.priorityCombo.setItemText(2, QCoreApplication.translate("TaskDialog", u"High", None))

        self.dueCheck.setText(QCoreApplication.translate("TaskDialog", u"&Due", None))
        self.dueEdit.setDisplayFormat(QCoreApplication.translate("TaskDialog", u"yyyy-MM-dd", None))
        self.notesLabel.setText(QCoreApplication.translate("TaskDialog", u"&Notes", None))
    # retranslateUi

