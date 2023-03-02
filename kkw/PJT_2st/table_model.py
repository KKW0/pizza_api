
from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide2.QtGui import QImage, QPixmap, QPainter, QColor

class CustomTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        self.load_data(data)

    def load_data(self, data):
        self.column_count = 5

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
            return ("Project", "Seq", "DueDate", "Comment", "Description")[section]
        else:
            return str(section)

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()

        if role == Qt.DisplayRole:
            for column in range(len(self.input_data[row])):
                if column == index.column():
                    return str(self.input_data[row][column])

            return None

        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None





class CustomTableModel2(QAbstractTableModel):
    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
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
                image_path = self.input_data[row][0]
                pixmap = QPixmap(image_path).scaled(50, 50) # scale image to 50x50 pixels
                return pixmap
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None
