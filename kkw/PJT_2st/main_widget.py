# coding=utf-8

import sys

from PySide2.QtCore import Qt
from PySide2.QtCore import QModelIndex
from table_model import CustomTableModel
from table_model import CustomTableModel2
from PySide2 import QtWidgets, QtCore, QtUiTools
from PySide2.QtGui import QFont, QColor, QBrush, QPen
from PySide2.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem
from PySide2.QtWidgets import (QGridLayout, QHeaderView, QSizePolicy,
                               QTableView, QWidget, QApplication, QStyle)

class Widget(QTableView):
    def __init__(self, data):
        QTableView.__init__(self)

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        self.setFont(font)

        color = QColor(255, 255, 255)
        # myapp.ui.setStyleSheet("color: {}".format(color.name()))

        font.setBold(True)

        self.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter)
        self.verticalHeader().setDefaultAlignment(Qt.AlignVCenter)

        self.model = CustomTableModel(data)
        self.setModel(self.model)

        self.setFixedSize(400, 400)

        # QTableView Headers
        self.horizontal_header = self.horizontalHeader()
        self.vertical_header = self.verticalHeader()

        self.horizontalHeader().setMinimumSectionSize(50)
        self.verticalHeader().setMinimumSectionSize(35)

        # self.setColumnWidth(3, 200)

        self.horizontal_header.setStretchLastSection(True)

        self.setGeometry(QtCore.QRect(0, 0, 400, 400))  # Set the position and size of the Widget
        self.setStyleSheet("background-color: #353535; selection-background-color: gray;")

class Widget2(QTableView):
    def __init__(self, data):
        QTableView.__init__(self)

        # Getting the Model
        self.model = CustomTableModel2(data)
        self.setModel(self.model)

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        self.setFont(font)

        self.setFixedSize(600, 300)

        # QTableView Headers
        self.horizontal_header = self.horizontalHeader()
        self.vertical_header = self.verticalHeader()

        self.horizontal_header.setStretchLastSection(True)

        self.setGeometry(QtCore.QRect(0, 0, 600, 300))  # Set the position and size of the Widget2
        self.setStyleSheet("background-color: #353535; selection-background-color: gray;")

