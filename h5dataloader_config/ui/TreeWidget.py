from PySide2.QtWidgets import QTreeWidgetItem

class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None) -> None:
        super(TreeWidgetItem, self).__init__(parent)
    
    def __lt__(self, otherItem:QTreeWidgetItem):
        column = self.treeWidget().sortColumn()
        try:
            return float(otherItem.text(column)) < float(self.text(column))
        except ValueError:
            return otherItem.text(column) < self.text(column)
