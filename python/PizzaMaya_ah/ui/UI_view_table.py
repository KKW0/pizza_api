# coding=utf-8

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QTableView, QHeaderView

from PizzaMaya_ah.code.filter import Filter


class HorizontalHeader(QtWidgets.QHeaderView):
    def __init__(self, parent=None):
        super(HorizontalHeader, self).__init__(QtCore.Qt.Horizontal, parent)
        self.setSectionsMovable(False)
        self.combo = None
        self.combo2 = None
        self.sort_dict = None
        self.seq_index = 0
        self.proj_index = 0
        self.proxy_model = None
        self.proxy_model2 = None
        self.sort_button = None  # 정렬 버튼
        self.table = None
        self.model = None
        self.ft = Filter()
        self.setSectionResizeMode(QHeaderView.Fixed)
        self.setStretchLastSection(True)

        self.setSectionsMovable(False)
        self.setSectionsClickable(True)  # add this line

        self.setSortIndicator(-1, Qt.AscendingOrder)
        self.sort_button = QtWidgets.QPushButton(self)
        self.sort_button.setText("Sort")
        self.sort_button.setGeometry(self.sectionViewportPosition(2), 0, self.sectionSize(2) - 0, self.height())
        self.sort_button.clicked.connect(self.sort_clicked)
        self.sort_button.show()

    def sort_clicked(self):
        if self.seq_index != 0:
            self.proxy_model2.sort(self.seq_index, self.sortOrder())
        elif self.proj_index != 0:
            self.proxy_model.sort(self.proj_index, self.sortOrder())
        else:  # proj_index와 seq_index가 모두 0인 경우
            self.model.sort(self.logicalIndexAt(0), self.sortOrder())

    def sortIndicatorChanged(self, logicalIndex, order):
        if logicalIndex == 2:
            self.seq_index = 0
            self.proj_index = 0
            self.combo2.setCurrentIndex(0)
            if self.proxy_model2 is not None:
                self.proxy_model2.invalidate()
            elif self.proxy_model is not None:
                self.proxy_model.invalidate()
        super(HorizontalHeader, self).sortIndicatorChanged(logicalIndex, order)

    def showEvent(self, event):

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        self.setFont(font)

        _, _, proj_set, _, self.sort_dict = self.ft.collect_info_task()

        self.combo = QtWidgets.QComboBox(self)
        if proj_set:
            proj_set.sort()
        self.combo.addItems(['Project'] + proj_set)
        self.combo.currentTextChanged.connect(self.combobox_changed1)
        self.combo.setGeometry(self.sectionViewportPosition(0), 0, self.sectionSize(0) - 0, self.height())
        self.combo.show()

        self.combo2 = QtWidgets.QComboBox(self)
        self.combo2.addItems(['Sequence'])
        self.combo2.currentTextChanged.connect(self.combobox_changed2)
        self.combo2.setGeometry(self.sectionViewportPosition(1), 0, self.sectionSize(1) - 0, self.height())
        self.combo2.setDisabled(True)
        self.combo2.show()

        self.table = self.parent()
        self.model = self.table.model()

        super(HorizontalHeader, self).showEvent(event)

    def combobox_changed1(self, option):
        self.proxy_model = QtCore.QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        if option != 'Project':
            self.proj_index = self.combo.currentIndex()
            self.proxy_model.setFilterRegExp('^{}$'.format(option))
            self.proxy_model.setFilterKeyColumn(0)
            self.table.setModel(self.proxy_model)
            self.combo2.clear()
            if self.sort_dict[option]:
                self.sort_dict[option].sort()
            self.combo2.addItems(['Sequence'] + self.sort_dict[option])
            self.combo2.setDisabled(False)
        else:
            self.seq_index = 0
            self.proj_index = 0
            self.table.setModel(self.model)
            self.combo2.setCurrentIndex(0)
            self.combo2.setDisabled(True)

    def combobox_changed2(self, option2):
        if self.combo.currentIndex != 0:
            if option2 != 'Sequence':
                self.seq_index = self.combo2.currentIndex()
                self.proxy_model2 = QtCore.QSortFilterProxyModel()
                self.proxy_model2.setSourceModel(self.proxy_model)
                self.proxy_model2.setFilterRegExp('^{}$'.format(option2))
                self.proxy_model2.setFilterKeyColumn(1)
                self.table.setModel(self.proxy_model2)
            else:
                self.seq_index = 0
                self.table.setModel(self.proxy_model)


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

        self.horizontal_header = self.horizontalHeader()
        self.vertical_header = self.verticalHeader()
        self.horizontal_header.setDefaultAlignment(Qt.AlignHCenter)
        self.vertical_header.setDefaultAlignment(Qt.AlignVCenter)

        header = self.horizontalHeader()
        header.setDefaultAlignment(QtCore.Qt.AlignCenter)
        header.setFont(font)  # 헤더에 폰트 설정

        self.horizontal_header.setMinimumSectionSize(50)
        self.vertical_header.setMinimumSectionSize(50)
        self.vertical_header.setSectionResizeMode(QHeaderView.Fixed)

        self.setStyleSheet("background-color: #353535; selection-background-color: gray;")
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.horizontal_header.setSortIndicatorShown(True)
        self.horizontal_header.setSectionsClickable(True)
        self.horizontal_header.setStretchLastSection(True)


class Table2(QtWidgets.QTableView):
    """
    asset 선택하는 TableView
    """
    def __init__(self, data=None):
        super(Table2, self).__init__()
        self.pizza = None
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        self.setFont(font)

        # QTableView Headers
        self.horizontal_header = self.horizontalHeader()
        self.vertical_header = self.verticalHeader()

        # 고정된 헤더 모드 설정
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        header = self.horizontalHeader()
        header.setDefaultAlignment(QtCore.Qt.AlignCenter)
        header.setFont(font)  # 헤더에 폰트 설정

        self.horizontal_header.setMinimumSectionSize(100)
        self.vertical_header.setMinimumSectionSize(100)

        self.horizontal_header.setStretchLastSection(True)

        self.setStyleSheet(
            "background-color: #353535; selection-background-color: gray;};")

        corner_button = self.findChild(QtWidgets.QAbstractButton)
        corner_button.setStyleSheet("background-color: #ABABAB; color: black;")

        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        if data is not None:
            self.set_data(data)

    def set_data(self, data):
        """
        테이블 데이터를 설정합니다.
        """
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['A', 'B', 'C'])
        for row in data:
            items = [QtGui.QStandardItem(str(item)) for item in row]
            model.appendRow(items)

        self.setModel(model)
        self.resizeColumnsToContents()
        self.horizontal_header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)


class Table3(QtWidgets.QTableView):
    """
    asset 선택하는 TableView
    """
    def __init__(self, data=None):
        super(Table3, self).__init__()

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        self.setFont(font)

        # QTableView Headers
        self.horizontal_header = self.horizontalHeader()
        self.vertical_header = self.verticalHeader()


        # 고정된 헤더 모드 설정
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        header = self.horizontalHeader()
        header.setDefaultAlignment(QtCore.Qt.AlignCenter)
        header.setFont(font)  # 헤더에 폰트 설정

        self.horizontal_header.setMinimumSectionSize(110)
        self.vertical_header.setMinimumSectionSize(95)

        self.horizontal_header.setStretchLastSection(True)

        self.setStyleSheet("background-color: #353535; selection-background-color: gray;")
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        if data is not None:
            self.set_data(data)

    def set_data(self, data):
        """
        테이블 데이터를 설정합니다.
        """
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['A'])

        for row in data:
            items = [QtGui.QStandardItem(str(item)) for item in row]
            model.appendRow(items)

        self.setModel(model)
        self.resizeColumnsToContents()
        self.horizontal_header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)


