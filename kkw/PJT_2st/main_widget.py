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

        self.model = CustomTableModel(data)
        self.setModel(self.model)

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(10)

        font.setBold(True)

        self.setFont(font)

        self.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter)
        self.verticalHeader().setDefaultAlignment(Qt.AlignVCenter)

        # QTableView Headers
        self.horizontal_header = self.horizontalHeader()
        self.vertical_header = self.verticalHeader()

        self.horizontalHeader().setMinimumSectionSize(50)
        self.verticalHeader().setMinimumSectionSize(50)

        # self.setColumnWidth(3, 200)

        self.horizontal_header.setStretchLastSection(True)

        self.setStyleSheet("background-color: #353535; selection-background-color: gray;")
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

class Widget2(QTableView):
    def __init__(self, data):
        QTableView.__init__(self)

        # Getting the Model
        self.model_ = CustomTableModel2(data)
        self.setModel(self.model_)

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(10)

        font.setBold(True)

        self.setFont(font)

        # QTableView Headers
        self.horizontal_header = self.horizontalHeader()
        self.vertical_header = self.verticalHeader()

        self.horizontalHeader().setMinimumSectionSize(100)
        self.verticalHeader().setMinimumSectionSize(100)

        # self.setColumnWidth(3, 200)

        self.horizontal_header.setStretchLastSection(True)

        self.setStyleSheet("background-color: #353535; selection-background-color: gray;")
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)