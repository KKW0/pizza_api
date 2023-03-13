# coding=utf-8

from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QTableView


class Table(QTableView):
    """
    task 선택하는 TableView
    """
    def __init__(self):
        QTableView.__init__(self)

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

        self.horizontal_header.setStretchLastSection(True)

        self.setStyleSheet("background-color: #353535; selection-background-color: gray;")
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)


class Table2(QTableView):
    """
    asset, camera, undi_img 선택하는 TableView
    """
    def __init__(self):
        QTableView.__init__(self)

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

        self.horizontal_header.setStretchLastSection(True)

        self.setStyleSheet("background-color: #353535; selection-background-color: gray;")
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
