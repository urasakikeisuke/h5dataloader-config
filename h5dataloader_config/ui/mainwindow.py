# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dataloader_config.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(787, 734)
        self.action_Open = QAction(MainWindow)
        self.action_Open.setObjectName(u"action_Open")
        self.action_Save = QAction(MainWindow)
        self.action_Save.setObjectName(u"action_Save")
        self.action_Exit = QAction(MainWindow)
        self.action_Exit.setObjectName(u"action_Exit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.minibatchTab = QWidget()
        self.minibatchTab.setObjectName(u"minibatchTab")
        self.verticalLayout_3 = QVBoxLayout(self.minibatchTab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.splitter = QSplitter(self.minibatchTab)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.minibatchSrcLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.minibatchSrcLayout.setObjectName(u"minibatchSrcLayout")
        self.minibatchSrcLayout.setContentsMargins(0, 0, 0, 0)
        self.minibatchSrcHeaderLabel = QLabel(self.verticalLayoutWidget)
        self.minibatchSrcHeaderLabel.setObjectName(u"minibatchSrcHeaderLabel")

        self.minibatchSrcLayout.addWidget(self.minibatchSrcHeaderLabel)

        self.minibatchSrcVerticalSplitter = QSplitter(self.verticalLayoutWidget)
        self.minibatchSrcVerticalSplitter.setObjectName(u"minibatchSrcVerticalSplitter")
        self.minibatchSrcVerticalSplitter.setOrientation(Qt.Vertical)
        self.verticalLayoutWidget_4 = QWidget(self.minibatchSrcVerticalSplitter)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.minibatchSrcDataLayout = QVBoxLayout(self.verticalLayoutWidget_4)
        self.minibatchSrcDataLayout.setObjectName(u"minibatchSrcDataLayout")
        self.minibatchSrcDataLayout.setContentsMargins(0, 0, 0, 0)
        self.minibatchSrcPathLineEdit = QLineEdit(self.verticalLayoutWidget_4)
        self.minibatchSrcPathLineEdit.setObjectName(u"minibatchSrcPathLineEdit")
        self.minibatchSrcPathLineEdit.setReadOnly(True)

        self.minibatchSrcDataLayout.addWidget(self.minibatchSrcPathLineEdit)

        self.minibatchSrcDataTree = QTreeWidget(self.verticalLayoutWidget_4)
        self.minibatchSrcDataTree.setObjectName(u"minibatchSrcDataTree")
        self.minibatchSrcDataTree.setSortingEnabled(True)

        self.minibatchSrcDataLayout.addWidget(self.minibatchSrcDataTree)

        self.minibatchSrcVerticalSplitter.addWidget(self.verticalLayoutWidget_4)
        self.verticalLayoutWidget_3 = QWidget(self.minibatchSrcVerticalSplitter)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.minibatchSrcPropertyLayout = QVBoxLayout(self.verticalLayoutWidget_3)
        self.minibatchSrcPropertyLayout.setObjectName(u"minibatchSrcPropertyLayout")
        self.minibatchSrcPropertyLayout.setContentsMargins(0, 0, 0, 0)
        self.minibatchSrcPropertyLabel = QLabel(self.verticalLayoutWidget_3)
        self.minibatchSrcPropertyLabel.setObjectName(u"minibatchSrcPropertyLabel")

        self.minibatchSrcPropertyLayout.addWidget(self.minibatchSrcPropertyLabel)

        self.minibatchSrcPropertyTree = QTreeWidget(self.verticalLayoutWidget_3)
        self.minibatchSrcPropertyTree.setObjectName(u"minibatchSrcPropertyTree")
        self.minibatchSrcPropertyTree.setSortingEnabled(True)

        self.minibatchSrcPropertyLayout.addWidget(self.minibatchSrcPropertyTree)

        self.minibatchSrcVerticalSplitter.addWidget(self.verticalLayoutWidget_3)

        self.minibatchSrcLayout.addWidget(self.minibatchSrcVerticalSplitter)

        self.splitter.addWidget(self.verticalLayoutWidget)
        self.verticalLayoutWidget_2 = QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.minibatchDstLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.minibatchDstLayout.setObjectName(u"minibatchDstLayout")
        self.minibatchDstLayout.setContentsMargins(0, 0, 0, 0)
        self.minibatchDstHeaderLabel = QLabel(self.verticalLayoutWidget_2)
        self.minibatchDstHeaderLabel.setObjectName(u"minibatchDstHeaderLabel")

        self.minibatchDstLayout.addWidget(self.minibatchDstHeaderLabel)

        self.minibatchDstVerticalSplitter = QSplitter(self.verticalLayoutWidget_2)
        self.minibatchDstVerticalSplitter.setObjectName(u"minibatchDstVerticalSplitter")
        self.minibatchDstVerticalSplitter.setOrientation(Qt.Vertical)
        self.verticalLayoutWidget_5 = QWidget(self.minibatchDstVerticalSplitter)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.minibatchDstDataLayout = QVBoxLayout(self.verticalLayoutWidget_5)
        self.minibatchDstDataLayout.setObjectName(u"minibatchDstDataLayout")
        self.minibatchDstDataLayout.setContentsMargins(0, 0, 0, 0)
        self.minibatchDstButtonLayout = QHBoxLayout()
        self.minibatchDstButtonLayout.setObjectName(u"minibatchDstButtonLayout")
        self.addButton = QPushButton(self.verticalLayoutWidget_5)
        self.addButton.setObjectName(u"addButton")
        self.addButton.setEnabled(False)

        self.minibatchDstButtonLayout.addWidget(self.addButton)

        self.editButton = QPushButton(self.verticalLayoutWidget_5)
        self.editButton.setObjectName(u"editButton")
        self.editButton.setEnabled(False)

        self.minibatchDstButtonLayout.addWidget(self.editButton)

        self.deleteButton = QPushButton(self.verticalLayoutWidget_5)
        self.deleteButton.setObjectName(u"deleteButton")
        self.deleteButton.setEnabled(False)

        self.minibatchDstButtonLayout.addWidget(self.deleteButton)


        self.minibatchDstDataLayout.addLayout(self.minibatchDstButtonLayout)

        self.minibatchDstDataTree = QTreeWidget(self.verticalLayoutWidget_5)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Tag");
        self.minibatchDstDataTree.setHeaderItem(__qtreewidgetitem)
        self.minibatchDstDataTree.setObjectName(u"minibatchDstDataTree")
        self.minibatchDstDataTree.setSortingEnabled(True)

        self.minibatchDstDataLayout.addWidget(self.minibatchDstDataTree)

        self.minibatchDstVerticalSplitter.addWidget(self.verticalLayoutWidget_5)
        self.verticalLayoutWidget_6 = QWidget(self.minibatchDstVerticalSplitter)
        self.verticalLayoutWidget_6.setObjectName(u"verticalLayoutWidget_6")
        self.minibatchDstPropertyLayout = QVBoxLayout(self.verticalLayoutWidget_6)
        self.minibatchDstPropertyLayout.setObjectName(u"minibatchDstPropertyLayout")
        self.minibatchDstPropertyLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget_6)
        self.label.setObjectName(u"label")

        self.minibatchDstPropertyLayout.addWidget(self.label)

        self.minibatchDstPropertyTree = QTreeWidget(self.verticalLayoutWidget_6)
        self.minibatchDstPropertyTree.setObjectName(u"minibatchDstPropertyTree")
        self.minibatchDstPropertyTree.setSortingEnabled(True)

        self.minibatchDstPropertyLayout.addWidget(self.minibatchDstPropertyTree)

        self.minibatchDstVerticalSplitter.addWidget(self.verticalLayoutWidget_6)

        self.minibatchDstLayout.addWidget(self.minibatchDstVerticalSplitter)

        self.splitter.addWidget(self.verticalLayoutWidget_2)

        self.verticalLayout_3.addWidget(self.splitter)

        self.tabWidget.addTab(self.minibatchTab, "")
        self.labelTab = QWidget()
        self.labelTab.setObjectName(u"labelTab")
        self.verticalLayout_4 = QVBoxLayout(self.labelTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.labelTabWidget = QTabWidget(self.labelTab)
        self.labelTabWidget.setObjectName(u"labelTabWidget")
        self.labelTabWidget.setTabsClosable(True)

        self.verticalLayout_4.addWidget(self.labelTabWidget)

        self.tabWidget.addTab(self.labelTab, "")
        self.tfTab = QWidget()
        self.tfTab.setObjectName(u"tfTab")
        self.verticalLayout_2 = QVBoxLayout(self.tfTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.treeWidget = QTreeWidget(self.tfTab)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setSortingEnabled(True)

        self.verticalLayout_2.addWidget(self.treeWidget)

        self.tabWidget.addTab(self.tfTab, "")

        self.verticalLayout_5.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 787, 28))
        self.menu_File = QMenu(self.menubar)
        self.menu_File.setObjectName(u"menu_File")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_File.menuAction())
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addAction(self.action_Exit)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.labelTabWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"H5 DataLoader Setting", None))
        self.action_Open.setText(QCoreApplication.translate("MainWindow", u"&Open", None))
#if QT_CONFIG(shortcut)
        self.action_Open.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.action_Save.setText(QCoreApplication.translate("MainWindow", u"&Save", None))
#if QT_CONFIG(shortcut)
        self.action_Save.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_Exit.setText(QCoreApplication.translate("MainWindow", u"&Exit", None))
#if QT_CONFIG(shortcut)
        self.action_Exit.setShortcut(QCoreApplication.translate("MainWindow", u"Esc", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(accessibility)
        self.minibatchTab.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.minibatchSrcHeaderLabel.setText(QCoreApplication.translate("MainWindow", u"in HDF5 Dataset", None))
        ___qtreewidgetitem = self.minibatchSrcDataTree.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"Frame ID", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Type", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Tag", None));
        self.minibatchSrcPropertyLabel.setText(QCoreApplication.translate("MainWindow", u"Property", None))
        ___qtreewidgetitem1 = self.minibatchSrcPropertyTree.headerItem()
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("MainWindow", u"Value", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"Property", None));
        self.minibatchDstHeaderLabel.setText(QCoreApplication.translate("MainWindow", u"Mini Batch", None))
        self.addButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.editButton.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.deleteButton.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        ___qtreewidgetitem2 = self.minibatchDstDataTree.headerItem()
        ___qtreewidgetitem2.setText(2, QCoreApplication.translate("MainWindow", u"Frame ID", None));
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("MainWindow", u"Type", None));
        self.label.setText(QCoreApplication.translate("MainWindow", u"Property", None))
        ___qtreewidgetitem3 = self.minibatchDstPropertyTree.headerItem()
        ___qtreewidgetitem3.setText(1, QCoreApplication.translate("MainWindow", u"Value", None));
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("MainWindow", u"Property", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.minibatchTab), QCoreApplication.translate("MainWindow", u"Mini Batch", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.labelTab), QCoreApplication.translate("MainWindow", u"Label", None))
        ___qtreewidgetitem4 = self.treeWidget.headerItem()
        ___qtreewidgetitem4.setText(1, QCoreApplication.translate("MainWindow", u"Data", None));
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("MainWindow", u"Frame ID", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tfTab), QCoreApplication.translate("MainWindow", u"TF", None))
        self.menu_File.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
    # retranslateUi

