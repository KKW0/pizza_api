
import sys
from PySide2.QtCore import QModelIndex
from PySide2 import QtWidgets, QtCore, QtUiTools
from PySide2.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem
from PySide2.QtWidgets import (QGridLayout, QHeaderView, QSizePolicy,
                               QTableView, QWidget, QApplication, QStyle)


from table_model import CustomTableModel
from table_model import CustomTableModel2

class Widget(QTableView):
    def __init__(self, data):
        QTableView.__init__(self)

        self.model = CustomTableModel(data)
        self.setModel(self.model)

        self.setFixedSize(700, 615)

        # QTableView Headers
        self.horizontal_header = self.horizontalHeader()
        self.vertical_header = self.verticalHeader()

        self.horizontalHeader().setMinimumSectionSize(100)
        self.verticalHeader().setMinimumSectionSize(35)

        self.setColumnWidth(3, 200)

        self.horizontal_header.setStretchLastSection(True)

        self.setGeometry(QtCore.QRect(0, 0, 700, 615))  # Set the position and size of the Widget
        self.setStyleSheet("background-color: #353535; selection-background-color: gray;")



class Widget2(QTableView):
    def __init__(self, data):
        QTableView.__init__(self)

        # Getting the Model
        self.model = CustomTableModel2(data)
        self.setModel(self.model)

        # Creating a QTableView
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        self.setFixedSize(320, 300)

        # QTableView Headers
        self.horizontal_header = self.horizontalHeader()
        self.vertical_header = self.verticalHeader()

        self.horizontal_header.setStretchLastSection(True)

        self.setGeometry(QtCore.QRect(0, 0, 320, 300))  # Set the position and size of the Widget2
        self.setStyleSheet("background-color: #353535; selection-background-color: gray;")

