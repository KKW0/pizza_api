# coding=utf-8

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QTableView, QComboBox, QStyledItemDelegate


class WrapDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        text = index.data(QtCore.Qt.DisplayRole)
        document = QtGui.QTextDocument()
        document.setHtml(text)
        document.setTextWidth(option.rect.width())
        option.text = ""
        painter.translate(option.rect.x(), option.rect.y())
        document.drawContents(painter)


class Table(QTableView):
    """
    task 선택하는 TableView
    """
    def __init__(self):
        QTableView.__init__(self)

        self.setSortingEnabled(True)

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(10)

        font.setBold(True)

        self.setFont(font)

        self.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter)
        self.verticalHeader().setDefaultAlignment(Qt.AlignVCenter)

        # QTableView Headers
        self.combo_box = QComboBox(self.horizontalHeader())
        self.combo_box.setGeometry(0, 0, 100, 30)
        self.combo_box.addItems(['All', 'Option 1', 'Option 2'])


        self.combo_box2 = QComboBox(self.horizontalHeader())
        self.combo_box2.setGeometry(100, 0, 100, 30)
        self.combo_box2.addItems(['All', 'Option A', 'Option B'])


        # self.horizontal_header = self.horizontalHeader()
        self.vertical_header = self.verticalHeader()

        self.horizontalHeader().setMinimumSectionSize(50)
        self.verticalHeader().setMinimumSectionSize(50)

        self.horizontalHeader().setStretchLastSection(True)

        self.setStyleSheet("background-color: #353535; selection-background-color: gray;")
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        delegate = WrapDelegate(self.combo_box)
        self.horizontalHeader().setItemDelegateForColumn(0, delegate)

        delegate2 = WrapDelegate(self.combo_box2)
        self.horizontalHeader().setItemDelegateForColumn(1, delegate2)


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
