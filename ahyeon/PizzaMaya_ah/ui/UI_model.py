# coding=utf-8

from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex


class CustomTableModel(QAbstractTableModel):
    """
    task 선택하는 TableView의 모델
    """
    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        self.row_count = None
        self.input_data = None
        self.column_count = None
        self.load_data(data)

    def load_data(self, data):
        self.column_count = 3

        self.input_data = data
        self.row_count = len(data)

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ("Project", "Seq", "DueDate")[section]
        else:
            return str(section)

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()

        if role == Qt.DisplayRole:
            for column in range(len(self.input_data[row])):
                if column == index.column():
                    return str(self.input_data[row][column])

            return None

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None


class CustomTableModel2(QAbstractTableModel):
    """
    asset, camera, undi_img 선택하는 TableView의 모델
    """
    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        self.row_count = None
        self.input_data = None
        self.column_count = None
        self.load_data2(data)

    def load_data2(self, data):
        self.column_count = 3

        self.input_data = data
        self.row_count = len(data)

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ("Project", "Seq", "DueDate")[section]
        else:
            return str(section)

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            if column == 1:
                return str(self.input_data[row][1])
            elif column == 2:
                return str(self.input_data[row][2])

        elif role == Qt.DecorationRole:
            if column == 0:
                pixmap = QPixmap()
                pixmap.loadFromData(self.input_data[0][0])
                pixmap = pixmap.scaled(100, 100)
                return pixmap

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None