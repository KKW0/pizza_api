
import sys
from PySide2.QtWidgets import (QGridLayout, QHeaderView, QSizePolicy,
                               QTableView, QWidget, QApplication)

from table_model import CustomTableModel
from table_model import CustomTableModel2

class Widget(QTableView):
    def __init__(self, data):
        QTableView.__init__(self)

        self.model = CustomTableModel(data)

        self.setModel(self.model)

        # QTableView Headers
        self.horizontal_header = self.horizontalHeader()
        self.vertical_header = self.verticalHeader()

        self.setColumnWidth(3, 200)
        # self.horizontal_header.setSectionResizeMode(
        #     QHeaderView.ResizeToContents
        # )
        # self.vertical_header.setSectionResizeMode(
        #     QHeaderView.ResizeToContents
        # )
        self.horizontal_header.setStretchLastSection(True)
        #
        # size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #
        # size.setHorizontalStretch(1)
        # self.setSizePolicy(size)

class Widget2(QWidget):
    def __init__(self, data):
        QWidget.__init__(self)

        # Getting the Model
        self.model = CustomTableModel2(data)

        # Creating a QTableView
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        # QTableView Headers
        self.horizontal_header = self.table_view.horizontalHeader()
        self.vertical_header = self.table_view.verticalHeader()
        self.horizontal_header.setSectionResizeMode(
                               QHeaderView.ResizeToContents
                               )
        self.vertical_header.setSectionResizeMode(
                             QHeaderView.ResizeToContents
                             )
        self.horizontal_header.setStretchLastSection(True)

        # QWidget Layout
        self.main_layout = QGridLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        ## Left layout
        size.setHorizontalStretch(1)
        self.table_view.setSizePolicy(size)
        self.main_layout.addWidget(self.table_view)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)

