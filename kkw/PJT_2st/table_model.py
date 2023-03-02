
from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide2.QtGui import QImage, QPixmap, QPainter, QColor


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        self.load_data(data)

    def load_data(self, data):
        self.input_dates = data[0].values()
        self.input_magnitudes = data[1].values()
        self.input_dates2 = []
        self.input_magnitudes2 = []
        for i in self.input_dates:
            list(i)
            self.input_dates2 = list(i)
        for i in self.input_magnitudes:
            self.input_magnitudes2 = list(i)

        self.column_count = 5
        self.row_count = len(self.input_magnitudes2)

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
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            if column == 0:
                date = self.input_dates2[row]
                return str(date)
            elif column == 1:
                magnitude = self.input_magnitudes2[row]
                return str(magnitude)
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
        # self.input_dates = data[0].values()
        # self.input_magnitudes = data[1].values()
        # self.input_dates2 = []
        # self.input_magnitudes2 = []
        # for i in self.input_dates:
        #     list(i)
        #     self.input_dates2 = list(i)
        # for i in self.input_magnitudes:
        #     self.input_magnitudes2 = list(i)

        self.column_count = 3
        # self.row_count = len(self.input_magnitudes2)

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
            # if column == 1:
            #     date = self.input_dates2[row]
            #     print("AAA", date)
            #     return str(date)
            # elif column == 2:
            #     magnitude = self.input_magnitudes2[row]
            #     return str(magnitude)

            if column == 1:
                return str(self.input_data[row][1])
            elif column == 2:
                return str(self.input_data[row][2])

        elif role == Qt.DecorationRole:
            if column == 0:
                # image_path = '/home/rapa/다운로드/1111.jpeg' # assume image paths are in a separate list
                image_path = self.input_data[row][0]
                pixmap = QPixmap(image_path).scaled(50, 50) # scale image to 50x50 pixels
                return pixmap
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None
