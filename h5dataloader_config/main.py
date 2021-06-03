import os
import sys
from typing import Any, Dict, Union
import json
import h5py
from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QPalette
from PySide2.QtWidgets import QApplication, QColorDialog, QComboBox, QDialog, QFileDialog, QFormLayout, QInputDialog, QLabel, QLineEdit, QMainWindow, QPushButton, QTreeWidget, QWidget

from .common.structure import *
from .structure import *
from .ui import mainwindow, minibatch_dialog, label_tab, label_dialog
from .ui.TreeWidget import TreeWidgetItem

DEFAULT_OPEN_DIR:str = os.path.expanduser('~')
DEFAULT_EXPORT_DIR:str = os.path.expanduser('~')

class LabelTab(QWidget):
    def __init__(self, parent=None) -> None:
        super(LabelTab, self).__init__()
        self.ui = label_tab.Ui_Form()
        self.ui.setupUi(self)

class LabelDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super(LabelDialog, self).__init__()
        self.ui = label_dialog.Ui_Dialog()
        self.ui.setupUi(self)

class MinibatchConfigDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super(MinibatchConfigDialog, self).__init__()
        self.ui = minibatch_dialog.Ui_Dialog()
        self.ui.setupUi(self)

class H5DataLoaderConfig(QMainWindow):
    def __init__(self, parent=None) -> None:
        super(H5DataLoaderConfig, self).__init__()

        self.minibatchDialog = MinibatchConfigDialog()
        self.minibatchDialog.ui.typeComboBox.activated.connect(self.__minibatchDialogTypeComboboxActivated_callback)
        self.minibatchDialog.ui.fromTabWidget.tabBarClicked.connect(self.__minibatchDialogFromTabBarClicked_callback)
        self.minibatchDialog.ui.okButton.clicked.connect(self.__minibatchDialogOkButtonClicked_callback)
        self.minibatchDialog.ui.cancelButton.clicked.connect(lambda: self.minibatchDialog.close())
        self.minibatchFromDataList:List[List[Tuple[str, QComboBox]]] = []
        self.minibatchShapeDataList:List[QLineEdit] = []

        self.labelDialog = LabelDialog()
        self.labelDialog.ui.colorButton.clicked.connect(lambda: self.__labelDialogColorButtonClicked_callback())
        self.labelDialog.ui.okButton.clicked.connect(lambda: self.__labelDialogOkButtonClicked_callback())
        self.labelDialog.ui.cancelButton.clicked.connect(lambda: self.labelDialog.close())

        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.action_Open.triggered.connect(lambda: self.__fileOpen_callback())
        self.ui.action_Save.triggered.connect(lambda: self.__fileSave_callback())
        self.ui.action_Exit.triggered.connect(lambda: self.close())
        self.labelConfigAddButton = QPushButton('+', self)
        self.labelConfigAddButton.setFlat(True)
        self.labelConfigAddButton.clicked.connect(self.__labelTabAddButton_callback)
        self.ui.labelTabWidget.setCornerWidget(self.labelConfigAddButton)
        self.ui.labelTabWidget.tabCloseRequested.connect(self.__labelTabCloseRequested_callback)
        self.ui.labelTabWidget.tabBarDoubleClicked.connect(self.__labelTabBarDoubleClicked_callback)

        self.ui.minibatchSrcDataTree.itemSelectionChanged.connect(lambda: self.__minibatchSrcDataTreeItemSelectionChanged_callback())
        self.ui.minibatchDstDataTree.itemSelectionChanged.connect(lambda: self.__minibatchDstDataTreeItemSelectionChanged_callback())

        self.ui.addButton.clicked.connect(lambda: self.__minibatchAdd_callback())
        self.ui.editButton.clicked.connect(lambda: self.__minibatchEdit_callback())
        self.ui.deleteButton.clicked.connect(lambda: self.__minibatchDelete_callback())

    def __fileOpen_callback(self) -> None:
        fname = QFileDialog.getOpenFileName(self,
            'Open HDF5 file', DEFAULT_OPEN_DIR,
            "HDF5, JSON (*.hdf5 *.h5 *.json);;HDF5 (*.hdf5 *.h5);;JSON (*.json)"
        )
        if fname[0] == "": return
        filename = fname[0]
        if os.path.isfile(filename):
            if filename[-5:] == '.hdf5' or filename[-3:] == '.h5':
                self.__loadHdf5(filename)
            elif filename[-5:] == '.json':
                self.__loadJson(filename)
    
    def __fileSave_callback(self) -> None:
        fname = QFileDialog.getSaveFileName(self, 'Save Config file', DEFAULT_EXPORT_DIR, "JSON (*.json)")
        if fname[0] == '': return
        filename = fname[0]
        if filename[-5:] != '.json':
            filename += '.json'
        with open(filename, mode='w') as jsonfile:
            json.dump(self.dataloader_config, jsonfile, indent=2)

    def __loadHdf5(self, h5path:str) -> None:
        if os.path.isfile(h5path) is False:
            return
        with h5py.File(h5path, mode='r') as h5file:
            self.dataloader_config:Dict[str, Dict[str, Dict[str, Dict[str, dict]]]] = {}
            self.dataloader_config[H5_ATTR_FILEPATH] = h5path
            h5file_data:h5py.Group = h5file['data/0']

            config_srcdata_dict = {}
            config_pose_dict = {}

            for key_tag, item_tag in h5file_data.items():
                self.__get_nestData(config_srcdata_dict, key_tag, item_tag)
                self.__get_nestPose(config_pose_dict, key_tag, item_tag)
            
            for key_root, item_root in h5file.items():
                if key_root in [H5_KEY_HEADER, H5_KEY_DATA, H5_KEY_LABEL]: continue
                if isinstance(item_root, h5py.Group):
                    for key_tag, item_tag in item_root.items():
                        self.__get_nestData(config_srcdata_dict, key_tag, item_tag, key_root='/'+key_root)
                        self.__get_nestPose(config_pose_dict, key_tag, item_tag, key_root='/'+key_root)

            self.dataloader_config[CONFIG_TAG_MINIBATCH] = {}
            self.dataloader_config[CONFIG_TAG_SRCDATA] = config_srcdata_dict

            pose_parent = {cf[CONFIG_TAG_FRAMEID] for cf in config_pose_dict.values()}
            pose_children = {cf[CONFIG_TAG_CHILDFRAMEID] for cf in config_pose_dict.values()}
            pose_roots = pose_parent - pose_children
            pose_set = pose_parent | pose_children
            pose_nodes = {}
            for cf in config_pose_dict.values():
                pose_nodes[cf[CONFIG_TAG_CHILDFRAMEID]] = {}
            config_tf_tree_dict = {}
            for cf in config_pose_dict.values():
                child_frame_id = cf[CONFIG_TAG_CHILDFRAMEID]
                frame_id = cf[CONFIG_TAG_FRAMEID]
                node = pose_nodes[child_frame_id]
                if {frame_id} <= pose_roots:
                    if frame_id not in config_tf_tree_dict.keys():
                        config_tf_tree_dict[frame_id] = {}
                    parent = config_tf_tree_dict[frame_id]
                else:
                    parent = pose_nodes[frame_id]
                parent[child_frame_id] = node
            config_tf_dict = {}
            config_tf_dict[CONFIG_TAG_TREE] = config_tf_tree_dict
            config_tf_dict[CONFIG_TAG_LIST] = list(pose_set)
            config_tf_dict[CONFIG_TAG_DATA] = config_pose_dict

            self.dataloader_config[CONFIG_TAG_TF] = config_tf_dict

            config_label_dict = {CONFIG_TAG_SRC: {}, CONFIG_TAG_CONFIG: {}}
            if H5_KEY_LABEL in h5file.keys():
                h5file_label:h5py.Group = h5file[H5_KEY_LABEL]
                key_tag:str
                item_tag:h5py.Group
                for key_tag, item_tag in h5file_label.items():
                    tag_dict = {}
                    config_dict = {CONFIG_TAG_SRC: key_tag, CONFIG_TAG_CONVERT: {}, CONFIG_TAG_DST: {}}
                    for key_idx, item_idx in item_tag.items():
                        config_idx_dict = {}
                        config_idx_dict[CONFIG_TAG_TAG] = byte2str(item_idx[H5_KEY_NAME][()])
                        config_idx_dict[CONFIG_TAG_COLOR] = item_idx[CONFIG_TAG_COLOR][()].tolist()
                        tag_dict[key_idx] = config_idx_dict
                        config_dict[CONFIG_TAG_CONVERT][key_idx] = int(key_idx)
                        config_dict[CONFIG_TAG_DST][key_idx] = config_idx_dict.copy()
                    config_label_dict[CONFIG_TAG_SRC][key_tag] = self.__sort_byIdx(tag_dict)
                    config_label_dict[CONFIG_TAG_CONFIG][key_tag] = config_dict
            
            self.dataloader_config[CONFIG_TAG_LABEL] = config_label_dict
        self.__loadData()
    
    def __loadJson(self, jsonpath:str) -> None:
        if os.path.isfile(jsonpath) is False: return
        with open(jsonpath, mode='r') as jsonfile:
            self.dataloader_config:Dict[str, Dict[str, Dict[str, Dict[str, dict]]]] = json.load(jsonfile)
        self.__loadData()
    
    def __loadData(self) -> None:
        self.ui.minibatchSrcPathLineEdit.setText(self.dataloader_config[H5_ATTR_FILEPATH])
        self.minibatchDialog.ui.frameidComboBox.clear()
        self.minibatchDialog.ui.frameidComboBox.addItems(self.__getTfList())
        self.minibatchDialog.ui.typeComboBox.addItems(self.__get_availableTypes())

        self.ui.minibatchSrcDataTree.clear()
        for key_tag, item_tag in self.dataloader_config[CONFIG_TAG_SRCDATA].items():
            treeitem = TreeWidgetItem([key_tag, item_tag.get(CONFIG_TAG_TYPE), str(item_tag.get(CONFIG_TAG_FRAMEID))])
            self.ui.minibatchSrcDataTree.addTopLevelItem(treeitem)
        self.ui.addButton.setEnabled(True)
        self.ui.editButton.setEnabled(True)
        self.ui.deleteButton.setEnabled(True)
        
        self.ui.minibatchDstDataTree.clear()
        for key_tag, item_tag in self.dataloader_config[CONFIG_TAG_MINIBATCH].items():
            treeItem = TreeWidgetItem([key_tag, item_tag.get(CONFIG_TAG_TYPE), str(item_tag.get(CONFIG_TAG_FRAMEID))])
            self.ui.minibatchDstDataTree.addTopLevelItem(treeItem)

        self.ui.labelTabWidget.clear()
        if len(self.dataloader_config[CONFIG_TAG_LABEL]) > 0:
            self.ui.tabWidget.setCurrentWidget(self.ui.labelTab)
            for key_tag, item_tag in self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_CONFIG].items():
                src_tag:str = item_tag[CONFIG_TAG_SRC]
                tabwidget = self.__labelTabAdd(key_tag, src_tag)

                for i in range(tabwidget.ui.srcTree.topLevelItemCount()):
                    item = tabwidget.ui.srcTree.topLevelItem(i)
                    key = item.text(0)
                    item.setText(3, str(item_tag[CONFIG_TAG_CONVERT][key]))
                self.__labelSrcDstCombobox_update(key_tag)

                for key_idx, item_idx in item_tag[CONFIG_TAG_DST].items():
                    treeitem = TreeWidgetItem([key_idx, item_idx[CONFIG_TAG_TAG], '#{2:02X}{1:02X}{0:02X}'.format(*item_idx[CONFIG_TAG_COLOR])])
                    self.__labelTreeItem_setColor(treeitem)
                    tabwidget.ui.dstTree.addTopLevelItem(treeitem)
                
        self.ui.treeWidget.clear()

        def setTfTree(parentItem:TreeWidgetItem, treeConfig:Dict[str, Union[str, dict]]):
            for key_frameid, item_frameid in treeConfig.items():
                data = self.dataloader_config[CONFIG_TAG_TF][CONFIG_TAG_DATA][key_frameid][CONFIG_TAG_KEY]
                treeItem = TreeWidgetItem([key_frameid, data])
                parentItem.addChild(treeItem)
                setTfTree(treeItem, item_frameid)
                treeItem.setExpanded(True)

        for key_frameid, item_frameid in self.dataloader_config[CONFIG_TAG_TF][CONFIG_TAG_TREE].items():
            item = TreeWidgetItem([key_frameid])
            self.ui.treeWidget.addTopLevelItem(item)
            setTfTree(item, item_frameid)
            item.setExpanded(True)

    def __get_nestPose(self, config:Dict[str, Dict[str, str]], key_tag:str, item_tag:Union[h5py.Dataset, h5py.Group], key_root:str='') -> None:
        key = os.path.join(key_root ,key_tag).replace('\\', '/')
        if isinstance(item_tag, h5py.Group):
            data_type:str = byte2str(item_tag.attrs.get(H5_ATTR_TYPE))
            if data_type in [TYPE_POSE]:
                frame_id:str = byte2str(item_tag.attrs.get(H5_ATTR_FRAMEID))
                child_frame_id:str = byte2str(item_tag.attrs.get(H5_ATTR_CHILDFRAMEID))

                config_pose_dict = {}
                config_pose_dict[CONFIG_TAG_KEY] = key
                config_pose_dict[CONFIG_TAG_FRAMEID] = frame_id
                config_pose_dict[CONFIG_TAG_CHILDFRAMEID] = child_frame_id
                config[child_frame_id] = config_pose_dict

            for key_child, item_child in item_tag.items():
                self.__get_nestPose(config, key_child, item_child, key)

    def __get_nestData(self, config:dict, key_tag:str, item_tag:Union[h5py.Dataset, h5py.Group], key_root:str='') -> None:
        key = os.path.join(key_root, key_tag).replace('\\', '/')
        if isinstance(item_tag, h5py.Group):
            data_type:str = byte2str(item_tag.attrs.get(H5_ATTR_TYPE))
            if data_type in [TYPE_POSE, TYPE_INTRINSIC, TYPE_SEMANTIC3D]:
                config_tag_dict = {}
                config_tag_dict[CONFIG_TAG_TAG] = key
                config_tag_dict[CONFIG_TAG_TYPE] = data_type
                config_tag_dict[CONFIG_TAG_SHAPE] = None
                config_tag_dict[CONFIG_TAG_FRAMEID] = byte2str(item_tag.attrs.get(H5_ATTR_FRAMEID))
                config_tag_dict[CONFIG_TAG_CHILDFRAMEID] = byte2str(item_tag.attrs.get(H5_ATTR_CHILDFRAMEID))
                config_tag_dict[CONFIG_TAG_LABELTAG] = byte2str(item_tag.attrs.get(H5_ATTR_LABELTAG))
                config[key] = config_tag_dict
                if data_type in [TYPE_INTRINSIC]: return

            for key_child, item_child in item_tag.items():
                self.__get_nestData(config, key_child, item_child, key)
        elif isinstance(item_tag, h5py.Dataset):
            data_type:Union[str, None] = byte2str(item_tag.attrs.get(H5_ATTR_TYPE))
            if data_type is None:
                data_type = str(item_tag.dtype)
            config_tag_dict = {}
            config_tag_dict[CONFIG_TAG_TAG] = key
            config_tag_dict[CONFIG_TAG_TYPE] = data_type
            config_tag_dict[CONFIG_TAG_SHAPE] = item_tag.shape
            config_tag_dict[CONFIG_TAG_FRAMEID] = byte2str(item_tag.attrs.get(H5_ATTR_FRAMEID))
            config_tag_dict[CONFIG_TAG_CHILDFRAMEID] = byte2str(item_tag.attrs.get(H5_ATTR_CHILDFRAMEID))
            config_tag_dict[CONFIG_TAG_LABELTAG] = byte2str(item_tag.attrs.get(H5_ATTR_LABELTAG))
            config[key] = config_tag_dict
    
    def __get_availableTypes(self) -> List[str]:
        srcTypes:set = {value[CONFIG_TAG_TYPE] for value in self.dataloader_config[CONFIG_TAG_SRCDATA].values()}
        availableTypes:List[str] = []
        for dstType, fromTypes in FROM_TYPES.items():
            available:bool = False
            for fromTypeComb in fromTypes:
                if set(fromTypeComb) <= srcTypes: available = True
            if available is True:
                availableTypes.append(dstType)
        return availableTypes

    def __minibatchSrcDataTreeItemSelectionChanged_callback(self) -> None:
        dataItem:TreeWidgetItem = self.ui.minibatchSrcDataTree.currentItem()
        if dataItem is None: return
        tag = dataItem.text(0)
        dataDict:Dict[str, Union[str, List[int], List[float]]] = self.dataloader_config[CONFIG_TAG_SRCDATA].get(tag)

        self.ui.minibatchSrcPropertyTree.clear()
        if dataDict is None: return
        for property, value in dataDict.items():
            propertyItem = TreeWidgetItem([property, str(value)])
            self.ui.minibatchSrcPropertyTree.addTopLevelItem(propertyItem)

    def __minibatchDstDataTreeItemSelectionChanged_callback(self) -> None:
        dataItem:TreeWidgetItem = self.ui.minibatchDstDataTree.currentItem()
        if dataItem is None: return
        tag = dataItem.text(0)
        dataDict:Dict[str, Union[str, List[int], List[float], Dict[str, str]]] = self.dataloader_config[CONFIG_TAG_MINIBATCH].get(tag)

        self.ui.minibatchDstPropertyTree.clear()
        if dataDict is None: return
        for property, value in dataDict.items():
            if property == CONFIG_TAG_FROM:
                propertyItem = TreeWidgetItem([property, ''])
                for fromKey, fromItem in value.items():
                    fromTreeItem = TreeWidgetItem([fromKey, fromItem])
                    propertyItem.addChild(fromTreeItem)
            else:
                propertyItem = TreeWidgetItem([property, str(value)])
            self.ui.minibatchDstPropertyTree.addTopLevelItem(propertyItem)
            propertyItem.setExpanded(True)

    def __minibatchAdd_callback(self) -> None:
        self.minibatchDialog_targetTag:str = ''
        self.minibatchDialog.ui.tagLineEdit.setText('')
        treeItem = self.ui.minibatchSrcDataTree.currentItem()
        if treeItem is None:
            initialIdx = 0
            self.minibatchDialog.ui.typeComboBox.setCurrentIndex(initialIdx)
        else:
            dataType:str = treeItem.text(1)
            self.minibatchDialog.ui.typeComboBox.setCurrentText(dataType)
            initialIdx = self.minibatchDialog.ui.typeComboBox.currentIndex()
        self.__minibatchDialogTypeComboboxActivated_callback(initialIdx)

        self.minibatchDialog.exec_()
    
    def __minibatchEdit_callback(self) -> None:
        treeItem = self.ui.minibatchDstDataTree.currentItem()
        if treeItem is None: return

        dataTag:str = treeItem.text(0)
        self.minibatchDialog.ui.tagLineEdit.setText(dataTag)
        minibatchConfig = self.dataloader_config[CONFIG_TAG_MINIBATCH][dataTag]
        dataType:str = minibatchConfig[CONFIG_TAG_TYPE]

        self.minibatchDialog_targetTag:str = dataTag

        self.minibatchDialog.ui.typeComboBox.setCurrentText(minibatchConfig[CONFIG_TAG_TYPE])
        typeIdx = self.minibatchDialog.ui.typeComboBox.currentIndex()
        self.__minibatchDialogTypeComboboxActivated_callback(typeIdx)

        dialogTabIdx:int = 0
        fromTypeSet:set = set(minibatchConfig[CONFIG_TAG_FROM].keys())
        for itr, fromTypeComb in enumerate(FROM_TYPES[dataType]):
            if set(fromTypeComb) == fromTypeSet:
                dialogTabIdx = itr
                break
        for dialogFromLabel, dialogFromCombobox in self.minibatchFromDataList[dialogTabIdx]:
            dialogFromCombobox.setCurrentText(minibatchConfig[CONFIG_TAG_FROM][dialogFromLabel])

        self.minibatchDialog.ui.frameidComboBox.setCurrentText(minibatchConfig[CONFIG_TAG_FRAMEID])
        self.minibatchDialog.ui.normalizeCheckBox.setChecked(minibatchConfig[CONFIG_TAG_NORMALIZE])

        for shapeLineEdit, shapeValue in zip(self.minibatchShapeDataList, minibatchConfig[CONFIG_TAG_SHAPE]):
            if shapeLineEdit.isReadOnly() is False:
                shapeLineEdit.setText(str(shapeValue))
        
        rangeList = DEFAULT_RANGE[dataType]
        if isinstance(rangeList, tuple):
            if rangeList[0] != minibatchConfig[CONFIG_TAG_RANGE][0]:
                self.minibatchDialog.ui.rangeMinLineEdit.setText(str(minibatchConfig[CONFIG_TAG_RANGE][0]))
            if rangeList[1] != minibatchConfig[CONFIG_TAG_RANGE][1]:
                self.minibatchDialog.ui.rangeMaxLineEdit.setText(str(minibatchConfig[CONFIG_TAG_RANGE][1]))
        
        labelTagList = [self.minibatchDialog.ui.labelComboBox.itemText(i) for i in range(self.minibatchDialog.ui.labelComboBox.count())]
        labelTag = minibatchConfig[CONFIG_TAG_LABELTAG]
        if labelTag in labelTagList:
            self.minibatchDialog.ui.labelComboBox.setCurrentText(labelTag)

        self.minibatchDialog.exec_()
    
    def __minibatchDelete_callback(self) -> None:
        treeItem = self.ui.minibatchDstDataTree.currentItem()
        if treeItem is None: return

        dataTag:str = treeItem.text(0)
        self.dataloader_config[CONFIG_TAG_MINIBATCH].pop(dataTag, None)
        treeItemIndex:int = self.ui.minibatchDstDataTree.indexOfTopLevelItem(treeItem)
        self.ui.minibatchDstDataTree.takeTopLevelItem(treeItemIndex)

    def __minibatchDialogTypeComboboxActivated_callback(self, idx:int):
        dataType:str = self.minibatchDialog.ui.typeComboBox.itemText(idx)
        dataFromTypes = FROM_TYPES[dataType]
        
        # Shape
        for shapeDataWidget in self.minibatchShapeDataList:
            self.minibatchDialog.ui.shapeLayout.removeWidget(shapeDataWidget)
            shapeDataWidget.setHidden(True)
        self.minibatchShapeDataList:List[QLineEdit] = []
        shapeTuple = SHAPE_TYPES[dataType]
        shapePlaceholder = SHAPE_PLACEHOLDER[dataType]
        if isinstance(shapeTuple, tuple):
            for val, ph in zip(shapeTuple, shapePlaceholder):
                shapeDataWidget = QLineEdit()
                if isinstance(val, QValidator):
                    shapeDataWidget.setValidator(val)
                    shapeDataWidget.setPlaceholderText(ph)
                elif isinstance(val, int):
                    shapeDataWidget.setText(str(val))
                    shapeDataWidget.setReadOnly(True)
                else:
                    shapeDataWidget.setText('N')
                    shapeDataWidget.setReadOnly(True)
                self.minibatchDialog.ui.shapeLayout.addWidget(shapeDataWidget)
                self.minibatchShapeDataList.append(shapeDataWidget)
        
        # FromTab
        self.minibatchDialog.ui.fromTabWidget.clear()
        self.minibatchFromDataList:List[List[Tuple[str, QComboBox]]] = []
        initialIdx:int = -1
        for tabItr, dataFromTypeComb in enumerate(dataFromTypes):
            dataFromWidget = QWidget()
            self.minibatchDialog.ui.fromTabWidget.addTab(dataFromWidget, '')
            dataFromLayout = QFormLayout(dataFromWidget)
            minibatchFromData:List[Tuple[str, QComboBox]] = []
            isDataExist:bool = False
            for fromItr, dataFromType in enumerate(dataFromTypeComb):
                dataCombobox = QComboBox()
                dataCombobox.activated.connect(lambda index, tabItr=tabItr, fromItr=fromItr: self.__minibatchDialogFromComboboxActivated_callback(index, tabItr, fromItr))
                if dataFromType == TYPE_POSE:
                    tfList:List[str] = self.__getTfList()
                    isDataExist = True if len(tfList) > 0 else isDataExist
                    dataCombobox.addItems(tfList)
                    dataFromLayout.addRow(QLabel(dataFromType + ' (Frame ID)'), dataCombobox)
                else:
                    dataList:List[str] = self.__minibatchSrcTypeFilter(dataFromType)
                    isDataExist = True if len(dataList) > 0 else isDataExist
                    dataCombobox.addItems(dataList)
                    dataFromLayout.addRow(QLabel(dataFromType), dataCombobox)
                minibatchFromData.append((dataFromType, dataCombobox))
            if initialIdx < 0 and isDataExist is True:
                initialIdx = tabItr
            self.minibatchFromDataList.append(minibatchFromData)
        if initialIdx >= 0:
            self.minibatchDialog.ui.fromTabWidget.setCurrentIndex(initialIdx)
            self.__minibatchDialogFromTabBarClicked_callback(initialIdx)
        
        # Normalize
        if ENABLE_NORMALIZE[dataType] is True:
            self.minibatchDialog.ui.normalizeCheckBox.setEnabled(True)
        else:
            self.minibatchDialog.ui.normalizeCheckBox.setChecked(False)
            self.minibatchDialog.ui.normalizeCheckBox.setEnabled(False)
        
        # Range
        self.minibatchDialog.ui.rangeMinLineEdit.setText('')
        self.minibatchDialog.ui.rangeMaxLineEdit.setText('')
        rangeTuple = DEFAULT_RANGE[dataType]
        rangeValidator = RANGE_VALIDATOR[dataType]
        if isinstance(rangeTuple, tuple):
            self.minibatchDialog.ui.rangeMinLineEdit.setEnabled(True)
            self.minibatchDialog.ui.rangeMaxLineEdit.setEnabled(True)
            self.minibatchDialog.ui.rangeMinLineEdit.setPlaceholderText(str(rangeTuple[0]))
            self.minibatchDialog.ui.rangeMaxLineEdit.setPlaceholderText(str(rangeTuple[1]))
            self.minibatchDialog.ui.rangeMinLineEdit.setValidator(rangeValidator)
            self.minibatchDialog.ui.rangeMaxLineEdit.setValidator(rangeValidator)
        else:
            self.minibatchDialog.ui.rangeMinLineEdit.setEnabled(False)
            self.minibatchDialog.ui.rangeMaxLineEdit.setEnabled(False)
            self.minibatchDialog.ui.rangeMinLineEdit.setPlaceholderText('')
            self.minibatchDialog.ui.rangeMaxLineEdit.setPlaceholderText('')
    
    def __minibatchSrcTypeFilter(self, dataType:str) -> List[str]:
        dataList:List[str] = []
        for itr in range(self.ui.minibatchSrcDataTree.topLevelItemCount()):
            treeItem:TreeWidgetItem = self.ui.minibatchSrcDataTree.topLevelItem(itr)
            if treeItem.text(1) == dataType:
                dataList.append(treeItem.text(0))
        return sorted(dataList)
    
    def __minibatchDialogFromTabBarClicked_callback(self, idx) -> None:
        labelTagEnable:bool = False
        self.minibatchDialog.ui.labelComboBox.clear()
        for fromItr, (fromLabel, fromCombobox) in enumerate(self.minibatchFromDataList[idx]):
            itemIdx:int = fromCombobox.currentIndex()
            self.__minibatchDialogFromComboboxActivated_callback(itemIdx, idx, fromItr)
            labelTagEnable |= USE_LABEL[fromLabel]
        self.minibatchDialog.ui.labelComboBox.setEnabled(labelTagEnable)

    def __minibatchDialogFromComboboxActivated_callback(self, idx:int, tabIdx:int, fromIdx:int) -> None:
        fromLabel, fromDataCombobox = self.minibatchFromDataList[tabIdx][fromIdx]
        if fromDataCombobox.count() < 1: return
        fromData:str = fromDataCombobox.itemText(idx)

        if fromLabel in [TYPE_POSE]:
            pass
        else:
            if fromIdx == 0:
                frameId = self.dataloader_config[CONFIG_TAG_SRCDATA][fromData].get(CONFIG_TAG_FRAMEID)
                if isinstance(frameId, str):
                    self.minibatchDialog.ui.frameidComboBox.setCurrentText(frameId)
                if len(self.minibatchFromDataList[tabIdx]) > 1:
                    for tmpFromLabel, tmpFromDataCombobox in self.minibatchFromDataList[tabIdx][1:]:
                        if tmpFromLabel in [TYPE_POSE]:
                            tmpFromDataCombobox.setCurrentText(frameId)
            if fromLabel == self.minibatchDialog.ui.typeComboBox.currentText():
                for shapeLineEdit, shapeValue in zip(self.minibatchShapeDataList, self.dataloader_config[CONFIG_TAG_SRCDATA][fromData][CONFIG_TAG_SHAPE]):
                    if shapeLineEdit.isReadOnly() is False:
                        shapeLineEdit.setText(str(shapeValue))
            if USE_LABEL[fromLabel] is True:
                self.minibatchDialog.ui.labelComboBox.clear()
                labelTag:str = self.dataloader_config[CONFIG_TAG_SRCDATA][fromData][CONFIG_TAG_LABELTAG]
                labelConfigList:List[str] = [key for key, item in self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_CONFIG].items() if item[CONFIG_TAG_SRC] == labelTag]
                self.minibatchDialog.ui.labelComboBox.addItems(labelConfigList)

    def __minibatchDialogOkButtonClicked_callback(self) -> None:
        dstTag:str = self.minibatchDialog.ui.tagLineEdit.text()
        dstType:str = self.minibatchDialog.ui.typeComboBox.currentText()
        dstFrameId:str = self.minibatchDialog.ui.frameidComboBox.currentText()
        fromTabIdx:int = self.minibatchDialog.ui.fromTabWidget.currentIndex()
        fromTupleList:List[Tuple[str, str]] = [(fromType, fromDataCombobox.currentText()) for fromType, fromDataCombobox in self.minibatchFromDataList[fromTabIdx]]
        dstShapeList:List[str] = [shapeLineEdit.text() for shapeLineEdit in self.minibatchShapeDataList]
        dstNormalize:bool = self.minibatchDialog.ui.normalizeCheckBox.isChecked()
        dstRange:Tuple[str, str] = (self.minibatchDialog.ui.rangeMinLineEdit.text(), self.minibatchDialog.ui.rangeMaxLineEdit.text())
        dstLabelTag:str = self.minibatchDialog.ui.labelComboBox.currentText()

        if dstTag == '': return
        if dstTag in self.dataloader_config[CONFIG_TAG_MINIBATCH].keys():
            if dstTag != self.minibatchDialog_targetTag: return
        if dstType == '': return

        hasBlank:bool = False
        for fromTuple in fromTupleList:
            if fromTuple[1] == '': hasBlank = True
        if hasBlank is True: return

        hasBlank:bool = False
        for dstShapeStr in dstShapeList:
            if dstShapeStr == '': hasBlank = True
        if hasBlank is True: return

        if USE_LABEL[dstType] is True:
            if dstLabelTag == '': return

        minibatchConfig:Dict[str, Union[str, list, dict]] = {}
        minibatchConfig[CONFIG_TAG_TYPE] = dstType
        minibatchConfig[CONFIG_TAG_FRAMEID] = dstFrameId

        minibatchConfig[CONFIG_TAG_FROM] = {}
        useLabel:bool = False
        for key, value in fromTupleList:
            minibatchConfig[CONFIG_TAG_FROM][key] = value
            useLabel |= USE_LABEL[key]
        if useLabel is True:
            if dstLabelTag == '': return

        dstShape:List[Union[int, None]] = []
        for dstShapeStr in dstShapeList:
            if dstShapeStr.isdecimal():
                dstShape.append(int(dstShapeStr))
            else:
                dstShape.append(None)
        minibatchConfig[CONFIG_TAG_SHAPE] = dstShape

        minibatchConfig[CONFIG_TAG_NORMALIZE] = dstNormalize

        defaultValidator = RANGE_VALIDATOR[dstType]
        dstRangeMin, dstRangeMax = dstRange
        if isinstance(defaultValidator, QIntValidator):
            minibatchConfig[CONFIG_TAG_RANGE] = [
                DEFAULT_RANGE[dstType][0] if dstRangeMin == '' else int(dstRangeMin),
                DEFAULT_RANGE[dstType][1] if dstRangeMax == '' else int(dstRangeMax)
            ]
        elif isinstance(defaultValidator, QDoubleValidator):
            minibatchConfig[CONFIG_TAG_RANGE] = [
                DEFAULT_RANGE[dstType][0] if dstRangeMin == '' else float(dstRangeMin),
                DEFAULT_RANGE[dstType][1] if dstRangeMax == '' else float(dstRangeMax)
            ]
        else:
            minibatchConfig[CONFIG_TAG_RANGE] = None

        minibatchConfig[CONFIG_TAG_LABELTAG] = dstLabelTag

        self.dataloader_config[CONFIG_TAG_MINIBATCH][dstTag] = minibatchConfig

        if self.minibatchDialog_targetTag == '':
            self.__minibatchDstDataTree_addItem(dstTag)
        else:
            self.__minibatchDstDataTree_editItem(dstTag)
        
        self.minibatchDialog.close()

    def __minibatchDstDataTree_addItem(self, minibatchTag:str) -> None:
        minibatchConfig = self.dataloader_config[CONFIG_TAG_MINIBATCH][minibatchTag]
        treeItem = TreeWidgetItem([minibatchTag, minibatchConfig[CONFIG_TAG_TYPE], minibatchConfig[CONFIG_TAG_FRAMEID]])
        self.ui.minibatchDstDataTree.addTopLevelItem(treeItem)
    
    def __minibatchDstDataTree_editItem(self, minibatchTag:str) -> None:
        minibatchConfig = self.dataloader_config[CONFIG_TAG_MINIBATCH][minibatchTag]
        treeItem:TreeWidgetItem = self.ui.minibatchDstDataTree.currentItem()
        treeItem.setText(0, minibatchTag)
        treeItem.setText(1, minibatchConfig[CONFIG_TAG_TYPE])
        treeItem.setText(2, minibatchConfig[CONFIG_TAG_FRAMEID])

    def __getTfList(self) -> List[str]:
        return sorted(self.dataloader_config[CONFIG_TAG_TF][CONFIG_TAG_LIST])

    def __labelTabAddButton_callback(self) -> None:
        newLabelConfigTag, status = QInputDialog.getText(self.ui.labelTabWidget, 'Add New Label Config', 'Specify new label-config tag', QLineEdit.Normal)
        if not status: return
        srcTag = list(self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_SRC].keys())[0]
        config_dict = {CONFIG_TAG_SRC: srcTag, CONFIG_TAG_CONVERT: {}, CONFIG_TAG_DST: {}}
        self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_CONFIG][newLabelConfigTag] = config_dict
        self.__labelTabAdd(newLabelConfigTag, srcTag)

    def __labelTabAdd(self, configTag:str, srcTag:str) -> LabelTab:
        tabwidget = LabelTab()
        self.ui.labelTabWidget.addTab(tabwidget, configTag)

        if self.ui.labelTabWidget.count() > 1:
            self.ui.labelTabWidget.setTabsClosable(True)
        else:
            self.ui.labelTabWidget.setTabsClosable(False)

        srcTags = list(self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_SRC].keys())
        tabwidget.ui.srcComboBox.addItems(srcTags)
        tabwidget.ui.srcComboBox.setCurrentText(srcTag)
        tabwidget.ui.srcComboBox.activated.connect(self.__labelSrcComboboxActivated_callback)
        self.__labelSrcTree_load(tabwidget.ui.srcTree, srcTag, configTag)

        tabwidget.ui.dstImportButton.clicked.connect(lambda: self.__labelDstImportClicked_callback())
        tabwidget.ui.dstAddButton.clicked.connect(lambda: self.__labelDstAddClicked_callback())
        tabwidget.ui.dstDeleteButton.clicked.connect(lambda: self.__labelDstDeleteClicked_callback())
        tabwidget.ui.dstUpButton.clicked.connect(lambda: self.__labelDstUpClicked_callback())
        tabwidget.ui.dstDownButton.clicked.connect(lambda: self.__labelDstDownClicked_callback())
        tabwidget.ui.dstTree.itemDoubleClicked.connect(self.__labelDstTreeDoubleClicked_callback)
        return tabwidget
    
    def __labelTabBarDoubleClicked_callback(self, index:int):
        renamedLabelConfigTag, status = QInputDialog.getText(self.ui.labelTabWidget, 'Rename Label Config', 'Specify label-config tag', QLineEdit.Normal)
        if not status: return
        srcConfigTag:str = self.ui.labelTabWidget.tabText(index)
        tmp_configDict:dict = self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_CONFIG].pop(srcConfigTag)
        self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_CONFIG][renamedLabelConfigTag] = tmp_configDict
        self.ui.labelTabWidget.setTabText(index, renamedLabelConfigTag)

    def __labelTabCloseRequested_callback(self, index:int):
        if self.ui.labelTabWidget.count() < 2: return

        configTag:str = self.ui.labelTabWidget.tabText(index)
        self.ui.labelTabWidget.removeTab(index)
        self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_CONFIG].pop(configTag, None)

        if self.ui.labelTabWidget.count() > 1:
            self.ui.labelTabWidget.setTabsClosable(True)
        else:
            self.ui.labelTabWidget.setTabsClosable(False)

    def __labelSrcComboboxActivated_callback(self, idx:int) -> None:
        tab_idx = self.ui.labelTabWidget.currentIndex()
        tab_label = self.ui.labelTabWidget.tabText(tab_idx)

        currentTab:LabelTab = self.ui.labelTabWidget.widget(tab_idx)
        targetSrc:str = currentTab.ui.srcComboBox.itemText(idx)

        config_dict = self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_CONFIG][tab_label]
        config_dict[CONFIG_TAG_SRC] = targetSrc
        convert_dict = {}
        for key in self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_SRC][targetSrc].keys():
            convert_dict[key] = int(key)
        config_dict[CONFIG_TAG_CONVERT] = convert_dict

        self.__labelSrcTree_load(currentTab.ui.srcTree, targetSrc, tab_label)

    def __labelSrcTree_load(self, srcTreeWidget:QTreeWidget, targetSrc:str, labelConfigTag:str) -> None:
        srcTreeWidget.clear()
        for key_idx, item_idx in self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_SRC][targetSrc].items():
            treeItem = TreeWidgetItem([key_idx, item_idx[CONFIG_TAG_TAG], '#{2:02X}{1:02X}{0:02X}'.format(*item_idx[CONFIG_TAG_COLOR]), ''])
            self.__labelTreeItem_setColor(treeItem)
            srcTreeWidget.addTopLevelItem(treeItem)
            dstCombobox = QComboBox()
            dstCombobox.activated.connect(lambda index, item=treeItem, cb=dstCombobox: self.__labelSrcDstComboboxActivated_callback(item, cb))
            srcTreeWidget.setItemWidget(treeItem, 3, dstCombobox)
        # self.__labelSrcDstCombobox_update(labelConfigTag)

    def __labelSrcDstCombobox_update(self, labelConfigTag:str) -> None:
        for i in range(self.ui.labelTabWidget.count()):
            if self.ui.labelTabWidget.tabText(i) == labelConfigTag:
                targetTab:LabelTab = self.ui.labelTabWidget.widget(i)
                break
        dstList:List[str] = self.__labelDstList_get(labelConfigTag)
        for i in range(targetTab.ui.srcTree.topLevelItemCount()):
            item = targetTab.ui.srcTree.topLevelItem(i)
            dstCombobox:QComboBox = targetTab.ui.srcTree.itemWidget(item, 3)
            dstCombobox.clear()
            dstCombobox.addItems(dstList)
            srcIndex:str = item.text(0)
            dstIndex:str = item.text(3)
            if dstIndex == '':
                dstIndex:int = i if i < len(dstList) else len(dstList) - 1
                dstCombobox.setCurrentIndex(dstIndex)
                dstIndex:str = dstCombobox.currentText().split(':')[0]
            else:
                dstTexts:List[str] = [dst for dst in dstList if dst.startswith(dstIndex+':')]
                if len(dstTexts) > 0:
                    dstCombobox.setCurrentText(dstTexts[0])
                else:
                    dstIndex:int = len(dstList) - 1
                    dstCombobox.setCurrentIndex(dstIndex)
                    dstIndex:str = dstCombobox.currentText().split(':')[0]
            item.setText(3, dstIndex)
            if dstIndex == '':
                self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_CONFIG][labelConfigTag][CONFIG_TAG_CONVERT][srcIndex] = None
            else:
                self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_CONFIG][labelConfigTag][CONFIG_TAG_CONVERT][srcIndex] = int(dstIndex)

    def __labelDstList_get(self, labelConfigTag:str) -> List[str]:
        dst_dict = self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_CONFIG][labelConfigTag][CONFIG_TAG_DST]
        dst_dict = self.__sort_byIdx(dst_dict)
        return ['{0:s}: {1:s}'.format(key, item[CONFIG_TAG_TAG]) for key, item in dst_dict.items()]

    def __labelSrcDstComboboxActivated_callback(self, treeItem:TreeWidgetItem, comboBox:QComboBox) -> None:
        tab_idx = self.ui.labelTabWidget.currentIndex()
        tab_label = self.ui.labelTabWidget.tabText(tab_idx)

        srcIdx:str = treeItem.text(0)
        dstIdx:str = comboBox.currentText().split(':')[0]
        treeItem.setText(3, dstIdx)
        self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_CONFIG][tab_label][CONFIG_TAG_CONVERT][srcIdx] = int(dstIdx)

    def __labelDstAddClicked_callback(self) -> None:
        self.labelDialog_targetIdx:str = ''

        tab_idx = self.ui.labelTabWidget.currentIndex()
        tab_label = self.ui.labelTabWidget.tabText(tab_idx)

        for i in range(256):
            if str(i) not in self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_CONFIG][tab_label][CONFIG_TAG_DST].keys():
                idx:int = i
                break
        color:str = '#000000'

        self.__labelDialogExec(idx, '', color)
    
    def __labelDstImportClicked_callback(self) -> None:
        self.labelDialog_targetIdx = ""
        currentTab:LabelTab = self.ui.labelTabWidget.currentWidget()
        srcItem:TreeWidgetItem = currentTab.ui.srcTree.currentItem()
        if srcItem is None: return

        tab_idx = self.ui.labelTabWidget.currentIndex()
        tab_label = self.ui.labelTabWidget.tabText(tab_idx)

        for i in range(256):
            if str(i) not in self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_CONFIG][tab_label][CONFIG_TAG_DST].keys():
                idx:int = i
                break

        tag:str = srcItem.text(1)
        color:str = srcItem.text(2)
        self.__labelDstTree_addItem(tab_label, str(idx), tag, color)

    def __labelDstDeleteClicked_callback(self) -> None:
        currentTab:LabelTab = self.ui.labelTabWidget.currentWidget()
        dstItem:TreeWidgetItem = currentTab.ui.dstTree.currentItem()
        if dstItem is None: return

        idx:int = currentTab.ui.dstTree.indexOfTopLevelItem(dstItem)
        removed_item = currentTab.ui.dstTree.takeTopLevelItem(idx)
        removed_idx:str = removed_item.text(0)

        tab_idx = self.ui.labelTabWidget.currentIndex()
        tab_label = self.ui.labelTabWidget.tabText(tab_idx)

        self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_CONFIG][tab_label][CONFIG_TAG_DST].pop(removed_idx, None)
        self.__labelSrcDstCombobox_update(tab_label)

    def __labelDstUpClicked_callback(self) -> None:
        currentTab:LabelTab = self.ui.labelTabWidget.currentWidget()
        dstItem:TreeWidgetItem = currentTab.ui.dstTree.currentItem()
        if dstItem is None: return

        srcIdx = currentTab.ui.dstTree.indexOfTopLevelItem(dstItem)
        if srcIdx <= 0: return
        targetIdx = srcIdx - 1
        self.__labelDstUpDownCommon(srcIdx, targetIdx)

    def __labelDstDownClicked_callback(self) -> None:
        currentTab:LabelTab = self.ui.labelTabWidget.currentWidget()
        dstItem:TreeWidgetItem = currentTab.ui.dstTree.currentItem()
        if dstItem is None: return

        srcIdx = currentTab.ui.dstTree.indexOfTopLevelItem(dstItem)
        if srcIdx >= currentTab.ui.dstTree.topLevelItemCount() - 1: return
        targetIdx = srcIdx + 1
        self.__labelDstUpDownCommon(srcIdx, targetIdx)
    
    def __labelDstUpDownCommon(self, srcIdx, targetIdx) -> None:
        currentTab:LabelTab = self.ui.labelTabWidget.currentWidget()
        srcItem:TreeWidgetItem = currentTab.ui.dstTree.topLevelItem(srcIdx)
        targetItem:TreeWidgetItem = currentTab.ui.dstTree.topLevelItem(targetIdx)
        tmpSrcIdx:str = srcItem.text(0)
        tmpTargetIdx:str = targetItem.text(0)
        srcItem.setText(0, tmpTargetIdx)
        targetItem.setText(0, tmpSrcIdx)

        tab_idx = self.ui.labelTabWidget.currentIndex()
        tab_label = self.ui.labelTabWidget.tabText(tab_idx)

        config_dict:dict = self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_CONFIG][tab_label][CONFIG_TAG_DST]
        tmpSrcConfig:dict = config_dict[tmpSrcIdx].copy()
        tmpTargetConfig:dict = config_dict[tmpTargetIdx].copy()
        config_dict[tmpSrcIdx] = tmpTargetConfig
        config_dict[tmpTargetIdx] = tmpSrcConfig

        self.__labelSrcDstCombobox_update(tab_label)

    def __labelDstTreeDoubleClicked_callback(self, item:TreeWidgetItem) -> None:
        idx:str = item.text(0)
        tag:str = item.text(1)
        color:str = item.text(2)

        self.labelDialog_targetIdx:str = idx

        self.__labelDialogExec(int(idx), tag, color)
    
    def __labelDialogExec(self, idx:int, tag:str, colorCode:str) -> None:
        self.labelDialog.ui.indexSpinBox.setValue(idx)
        self.labelDialog.ui.tagLineEdit.setText(tag)
        self.labelDialog.ui.colorButton.setStyleSheet(
            'background-color : {0} ; color : {1}; border: 0px;'
            .format(colorCode, self.__decide_textColor(colorCode))
        )
        self.labelDialog.exec_()
    
    def __labelDialogColorButtonClicked_callback(self) -> None:
        init_color = self.labelDialog.ui.colorButton.palette().color(QPalette.Background)
        color = QColorDialog.getColor(init_color)
        if color.isValid() is False: return
        red, green, blue, _ = color.getRgb()
        color_code = '#{0:02X}{1:02X}{2:02X}'.format(red, green, blue)
        self.labelDialog.ui.colorButton.setStyleSheet('background-color : {0} ; color : {1}; border: 0px;'.format(color_code, self.__decide_textColor(color_code)))

    def __labelDialogOkButtonClicked_callback(self) -> None:
        idx:str = str(self.labelDialog.ui.indexSpinBox.value())
        tag:str = self.labelDialog.ui.tagLineEdit.text()
        if tag == '': return
        red, green, blue, _ = self.labelDialog.ui.colorButton.palette().color(QPalette.Background).getRgb()
        color:str = '#{0:02X}{1:02X}{2:02X}'.format(red, green, blue)

        currentTabIdx:int = self.ui.labelTabWidget.currentIndex()
        currentTabLabel:str = self.ui.labelTabWidget.tabText(currentTabIdx)

        if idx in self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_CONFIG][currentTabLabel][CONFIG_TAG_DST].keys():
            if idx != self.labelDialog_targetIdx: return

        if self.labelDialog_targetIdx == '':
            self.__labelDstTree_addItem(currentTabLabel, idx, tag, color)
        else:
            self.__labelDstTree_editItem(currentTabLabel, idx, tag, color)

        self.labelDialog.close()
    
    def __labelDstTree_addItem(self, labelConfigTag:str, idx:str, tag:str, color:str) -> None:
        currentTab:LabelTab = self.ui.labelTabWidget.currentWidget()
        item = TreeWidgetItem([idx, tag, color])
        currentTab.ui.dstTree.addTopLevelItem(item)
        self.__labelTreeItem_setColor(item)
        self.__labelConfigEdit(labelConfigTag, idx, tag, color)
        self.__labelSrcDstCombobox_update(labelConfigTag)

    def __labelDstTree_editItem(self, labelConfigTag:str, idx:str, tag:str, color:str) -> None:
        currentTab:LabelTab = self.ui.labelTabWidget.currentWidget()
        item:TreeWidgetItem = currentTab.ui.dstTree.currentItem()
        item.setText(0, idx)
        item.setText(1, tag)
        item.setText(2, color)
        self.__labelTreeItem_setColor(item)
        self.__labelConfigEdit(labelConfigTag, idx, tag, color)
        self.__labelSrcDstCombobox_update(labelConfigTag)

    def __labelConfigEdit(self, labelConfigTag:str, idx:str, label_tag:str, colorCode:str) -> None:
        self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_CONFIG][labelConfigTag][CONFIG_TAG_DST].pop(self.labelDialog_targetIdx, None)
        config_idx_dict = {}
        config_idx_dict[CONFIG_TAG_TAG] = label_tag
        config_idx_dict[CONFIG_TAG_COLOR] = list(self.__colorCode2bgr(colorCode))
        self.dataloader_config[CONFIG_TAG_LABEL][CONFIG_TAG_CONFIG][labelConfigTag][CONFIG_TAG_DST][idx] = config_idx_dict

    def __labelTreeItem_setColor(self, item:TreeWidgetItem) -> None:
        bg_color:QColor = QColor(item.text(2))
        fg_color:QColor = QColor(self.__decide_textColor(bg_color))

        for i in range(4):
            item.setBackground(i, bg_color)
            item.setForeground(i, fg_color)

    def __sort_byIdx(self, src:dict) -> dict:
        sorted_list = sorted(src.items(), key=lambda x:int(x[0]))
        dst_dict = {key: item for key, item in sorted_list}
        return dst_dict

    def __colorCode2bgr(self, colorCode:str) -> Tuple[int, int, int]:
        """'#RRGGBB'のカラーコードをBGRのタプルに変換

        Args:
            colorCode (str): '#RRGGBB'のカラーコード

        Returns:
            Tuple[int, int, int]: BGRのタプル
        """
        red = int(colorCode[1:3], 16)
        green = int(colorCode[3:5], 16)
        blue = int(colorCode[5:7], 16)
        return blue, green, red

    def __decide_textColor(self, color:Any) -> Union[str, QColor]:
        if isinstance(color, str):
            blue, green, red = self.__colorCode2bgr(color)
            if red * 0.299 + green * 0.587 + blue * 0.114 < 186:
                return '#FFFFFF'
            else:
                return '#000000'
        elif isinstance(color, QColor):
            red, green, blue, _ = color.getRgb()
            if red * 0.299 + green * 0.587 + blue * 0.114 < 186:
                return Qt.white
            else:
                return Qt.black

def byte2str(obj) -> Union[str, None]:
    return obj.decode() if isinstance(obj, bytes) else obj

def main() -> None:
    app = QApplication(sys.argv)
    h5dlc = H5DataLoaderConfig(app)
    h5dlc.show()
    sys.exit(app.exec_())
