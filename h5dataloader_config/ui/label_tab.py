# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dataloader_labeltab.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(757, 609)
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.srcLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.srcLayout.setObjectName(u"srcLayout")
        self.srcLayout.setContentsMargins(0, 0, 0, 0)
        self.srcHeaderLayout = QHBoxLayout()
        self.srcHeaderLayout.setObjectName(u"srcHeaderLayout")
        self.srcLabel = QLabel(self.verticalLayoutWidget)
        self.srcLabel.setObjectName(u"srcLabel")

        self.srcHeaderLayout.addWidget(self.srcLabel)

        self.srcComboBox = QComboBox(self.verticalLayoutWidget)
        self.srcComboBox.setObjectName(u"srcComboBox")

        self.srcHeaderLayout.addWidget(self.srcComboBox)

        self.srcHeaderLayout.setStretch(1, 1)

        self.srcLayout.addLayout(self.srcHeaderLayout)

        self.srcTree = QTreeWidget(self.verticalLayoutWidget)
        self.srcTree.setObjectName(u"srcTree")
        self.srcTree.setSortingEnabled(True)

        self.srcLayout.addWidget(self.srcTree)

        self.splitter.addWidget(self.verticalLayoutWidget)
        self.verticalLayoutWidget_2 = QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.dstLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.dstLayout.setObjectName(u"dstLayout")
        self.dstLayout.setContentsMargins(0, 0, 0, 0)
        self.dstHeaderLayout = QHBoxLayout()
        self.dstHeaderLayout.setObjectName(u"dstHeaderLayout")
        self.dstLabel = QLabel(self.verticalLayoutWidget_2)
        self.dstLabel.setObjectName(u"dstLabel")

        self.dstHeaderLayout.addWidget(self.dstLabel)

        self.dstImportButton = QPushButton(self.verticalLayoutWidget_2)
        self.dstImportButton.setObjectName(u"dstImportButton")

        self.dstHeaderLayout.addWidget(self.dstImportButton)

        self.dstAddButton = QPushButton(self.verticalLayoutWidget_2)
        self.dstAddButton.setObjectName(u"dstAddButton")

        self.dstHeaderLayout.addWidget(self.dstAddButton)

        self.dstDeleteButton = QPushButton(self.verticalLayoutWidget_2)
        self.dstDeleteButton.setObjectName(u"dstDeleteButton")

        self.dstHeaderLayout.addWidget(self.dstDeleteButton)

        self.dstUpButton = QPushButton(self.verticalLayoutWidget_2)
        self.dstUpButton.setObjectName(u"dstUpButton")

        self.dstHeaderLayout.addWidget(self.dstUpButton)

        self.dstDownButton = QPushButton(self.verticalLayoutWidget_2)
        self.dstDownButton.setObjectName(u"dstDownButton")

        self.dstHeaderLayout.addWidget(self.dstDownButton)

        self.dstHeaderLayout.setStretch(0, 1)

        self.dstLayout.addLayout(self.dstHeaderLayout)

        self.dstTree = QTreeWidget(self.verticalLayoutWidget_2)
        self.dstTree.setObjectName(u"dstTree")
        self.dstTree.setSortingEnabled(True)

        self.dstLayout.addWidget(self.dstTree)

        self.splitter.addWidget(self.verticalLayoutWidget_2)

        self.verticalLayout_3.addWidget(self.splitter)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.srcLabel.setText(QCoreApplication.translate("Form", u"Source", None))
        ___qtreewidgetitem = self.srcTree.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Form", u"Destination", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Form", u"Color", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Form", u"Tag", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"Index", None));
        self.dstLabel.setText(QCoreApplication.translate("Form", u"Destination", None))
        self.dstImportButton.setText(QCoreApplication.translate("Form", u">", None))
        self.dstAddButton.setText(QCoreApplication.translate("Form", u"Add", None))
        self.dstDeleteButton.setText(QCoreApplication.translate("Form", u"Delete", None))
        self.dstUpButton.setText(QCoreApplication.translate("Form", u"Up", None))
        self.dstDownButton.setText(QCoreApplication.translate("Form", u"Down", None))
        ___qtreewidgetitem1 = self.dstTree.headerItem()
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("Form", u"Color", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Form", u"Tag", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Form", u"Index", None));
    # retranslateUi

