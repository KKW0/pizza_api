from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide2.QtGui import QColor

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

