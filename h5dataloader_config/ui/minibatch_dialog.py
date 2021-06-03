# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dataloader_dialog.ui'
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
        Dialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.tagLabel = QLabel(Dialog)
        self.tagLabel.setObjectName(u"tagLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.tagLabel)

        self.tagLineEdit = QLineEdit(Dialog)
        self.tagLineEdit.setObjectName(u"tagLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.tagLineEdit)

        self.typeLabel = QLabel(Dialog)
        self.typeLabel.setObjectName(u"typeLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.typeLabel)

        self.typeComboBox = QComboBox(Dialog)
        self.typeComboBox.setObjectName(u"typeComboBox")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.typeComboBox)

        self.fromLabel = QLabel(Dialog)
        self.fromLabel.setObjectName(u"fromLabel")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.fromLabel)

        self.fromTabWidget = QTabWidget(Dialog)
        self.fromTabWidget.setObjectName(u"fromTabWidget")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.fromTabWidget)

        self.shapeLabel = QLabel(Dialog)
        self.shapeLabel.setObjectName(u"shapeLabel")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.shapeLabel)

        self.shapeLayout = QHBoxLayout()
        self.shapeLayout.setObjectName(u"shapeLayout")

        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.shapeLayout)

        self.normalizeLabel = QLabel(Dialog)
        self.normalizeLabel.setObjectName(u"normalizeLabel")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.normalizeLabel)

        self.normalizeCheckBox = QCheckBox(Dialog)
        self.normalizeCheckBox.setObjectName(u"normalizeCheckBox")
        self.normalizeCheckBox.setChecked(False)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.normalizeCheckBox)

        self.rangeLabel = QLabel(Dialog)
        self.rangeLabel.setObjectName(u"rangeLabel")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.rangeLabel)

        self.rangeLayout = QHBoxLayout()
        self.rangeLayout.setObjectName(u"rangeLayout")
        self.rangeMinGroupBox = QGroupBox(Dialog)
        self.rangeMinGroupBox.setObjectName(u"rangeMinGroupBox")
        self.horizontalLayout_7 = QHBoxLayout(self.rangeMinGroupBox)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.rangeMinLineEdit = QLineEdit(self.rangeMinGroupBox)
        self.rangeMinLineEdit.setObjectName(u"rangeMinLineEdit")

        self.horizontalLayout_7.addWidget(self.rangeMinLineEdit)


        self.rangeLayout.addWidget(self.rangeMinGroupBox)

        self.rangeMaxGroupBox = QGroupBox(Dialog)
        self.rangeMaxGroupBox.setObjectName(u"rangeMaxGroupBox")
        self.horizontalLayout_6 = QHBoxLayout(self.rangeMaxGroupBox)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.rangeMaxLineEdit = QLineEdit(self.rangeMaxGroupBox)
        self.rangeMaxLineEdit.setObjectName(u"rangeMaxLineEdit")

        self.horizontalLayout_6.addWidget(self.rangeMaxLineEdit)


        self.rangeLayout.addWidget(self.rangeMaxGroupBox)


        self.formLayout.setLayout(6, QFormLayout.FieldRole, self.rangeLayout)

        self.frameidLabel = QLabel(Dialog)
        self.frameidLabel.setObjectName(u"frameidLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.frameidLabel)

        self.frameidComboBox = QComboBox(Dialog)
        self.frameidComboBox.setObjectName(u"frameidComboBox")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.frameidComboBox)

        self.labelLabel = QLabel(Dialog)
        self.labelLabel.setObjectName(u"labelLabel")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.labelLabel)

        self.labelComboBox = QComboBox(Dialog)
        self.labelComboBox.setObjectName(u"labelComboBox")

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.labelComboBox)


        self.verticalLayout.addLayout(self.formLayout)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setObjectName(u"bottomLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.bottomLayout.addItem(self.horizontalSpacer)

        self.okButton = QPushButton(Dialog)
        self.okButton.setObjectName(u"okButton")

        self.bottomLayout.addWidget(self.okButton)

        self.cancelButton = QPushButton(Dialog)
        self.cancelButton.setObjectName(u"cancelButton")

        self.bottomLayout.addWidget(self.cancelButton)


        self.verticalLayout.addLayout(self.bottomLayout)

        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"MiniBatch Config", None))
        self.tagLabel.setText(QCoreApplication.translate("Dialog", u"Tag", None))
        self.typeLabel.setText(QCoreApplication.translate("Dialog", u"Type", None))
        self.fromLabel.setText(QCoreApplication.translate("Dialog", u"From", None))
        self.shapeLabel.setText(QCoreApplication.translate("Dialog", u"Shape", None))
        self.normalizeLabel.setText(QCoreApplication.translate("Dialog", u"Normalize", None))
        self.normalizeCheckBox.setText("")
        self.rangeLabel.setText(QCoreApplication.translate("Dialog", u"Range", None))
        self.rangeMinGroupBox.setTitle(QCoreApplication.translate("Dialog", u"min", None))
        self.rangeMaxGroupBox.setTitle(QCoreApplication.translate("Dialog", u"max", None))
        self.frameidLabel.setText(QCoreApplication.translate("Dialog", u"Frame ID", None))
        self.labelLabel.setText(QCoreApplication.translate("Dialog", u"Label", None))
        self.okButton.setText(QCoreApplication.translate("Dialog", u"&OK", None))
        self.cancelButton.setText(QCoreApplication.translate("Dialog", u"&Cancel", None))
    # retranslateUi

