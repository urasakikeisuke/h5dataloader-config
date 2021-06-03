# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dataloader_dstlabel_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(230, 139)
        self.formLayout = QFormLayout(Dialog)
        self.formLayout.setObjectName(u"formLayout")
        self.indexLabel = QLabel(Dialog)
        self.indexLabel.setObjectName(u"indexLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.indexLabel)

        self.indexSpinBox = QSpinBox(Dialog)
        self.indexSpinBox.setObjectName(u"indexSpinBox")
        self.indexSpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.indexSpinBox.setMinimum(-127)
        self.indexSpinBox.setMaximum(255)
        self.indexSpinBox.setValue(0)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.indexSpinBox)

        self.tagLabel = QLabel(Dialog)
        self.tagLabel.setObjectName(u"tagLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.tagLabel)

        self.tagLineEdit = QLineEdit(Dialog)
        self.tagLineEdit.setObjectName(u"tagLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.tagLineEdit)

        self.colorLabel = QLabel(Dialog)
        self.colorLabel.setObjectName(u"colorLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.colorLabel)

        self.colorButton = QPushButton(Dialog)
        self.colorButton.setObjectName(u"colorButton")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.colorButton)

        self.footerLayout = QHBoxLayout()
        self.footerLayout.setObjectName(u"footerLayout")
        self.okButton = QPushButton(Dialog)
        self.okButton.setObjectName(u"okButton")

        self.footerLayout.addWidget(self.okButton)

        self.cancelButton = QPushButton(Dialog)
        self.cancelButton.setObjectName(u"cancelButton")

        self.footerLayout.addWidget(self.cancelButton)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.footerLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.indexLabel.setText(QCoreApplication.translate("Dialog", u"Index", None))
        self.tagLabel.setText(QCoreApplication.translate("Dialog", u"Tag", None))
        self.colorLabel.setText(QCoreApplication.translate("Dialog", u"Color", None))
        self.colorButton.setText(QCoreApplication.translate("Dialog", u"Change", None))
        self.okButton.setText(QCoreApplication.translate("Dialog", u"OK", None))
        self.cancelButton.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

