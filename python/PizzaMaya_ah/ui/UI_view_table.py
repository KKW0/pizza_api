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
        self.seq_set = None
        self.sort_dict = None
        self.proxy_model = None
        self.sort_button = None  # 정렬 버튼
        # self.sectionResized.connect(self.handleSectionResized)
        # self.sectionMoved.connect(self.handleSectionMoved)
        self.ft = Filter()
        self.table = None
        self.model = None
        self.setSectionResizeMode(QHeaderView.Fixed)



    def showEvent(self, event):
        _, _, proj_set, self.seq_set, self.sort_dict = self.ft._collect_info_task()
        self.combo = QtWidgets.QComboBox(self)
        self.combo.addItems(['Project'] + proj_set)
        self.combo.currentTextChanged.connect(self.combobox_changed1)
        self.combo.setGeometry(self.sectionViewportPosition(0), 0, self.sectionSize(0) - 0, self.height())
        self.combo.show()

        self.combo2 = QtWidgets.QComboBox(self)
        self.combo2.addItems(['Sequence'] + self.seq_set)
        self.combo2.currentTextChanged.connect(self.combobox_changed2)
        self.combo2.setGeometry(self.sectionViewportPosition(1), 0, self.sectionSize(1) - 0, self.height())
        self.combo2.show()

        self.table = self.parent()
        self.model = self.table.model()
        super(HorizontalHeader, self).showEvent(event)

    def combobox_changed1(self, option):
        self.proxy_model = QtCore.QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.combo2.setDisabled(True)
        if option != 'Project':
            self.proxy_model.setFilterRegExp('^{}$'.format(option))
            self.proxy_model.setFilterKeyColumn(0)
            self.table.setModel(self.proxy_model)
            self.combo2.clear()
            # seq_set =
            # self.combo2.addItems(['Sequence'] + seq_set)
            self.combo2.setDisabled(False)
        else:
            self.table.setModel(self.model)
            self.combo2.setCurrentIndex(0)
            option2 = 'Sequence'
            self.combo2.setDisabled(True)

    def combobox_changed2(self, option2):
        if option2 != 'Sequence':
            proxy_model2 = QtCore.QSortFilterProxyModel()
            proxy_model2.setSourceModel(self.proxy_model)
            proxy_model2.setFilterRegExp('^{}$'.format(option2))
            proxy_model2.setFilterKeyColumn(1)
            self.table.setModel(proxy_model2)
        else:
            self.table.setModel(self.proxy_model)

    # def handleSortButtonClicked(self):
    #     # 마지막 헤더 클릭 시 정렬
    #     self.parent().sortByColumn(self.count() - 1, Qt.AscendingOrder)

    # def handleSectionResized(self, i):
    #     for i in range(self.count()):
    #         j = self.visualIndex(i)
    #         logical = self.logicalIndex(j)
    #         if i < len(self.comboboxes):
    #             self.comboboxes[i].setGeometry(self.sectionViewportPosition(logical), 0,
    #                                            self.sectionSize(logical) - 4, self.height())
    #
    #     # 정렬 버튼 위치 조정
    #     if self.sort_button:
    #         self.sort_button.setGeometry(self.sectionViewportPosition(self.count() - 1), 0,
    #                                      self.sectionSize(self.count() - 1) - 4, self.height())

    # def handleSectionMoved(self, i, oldVisualIndex, newVisualIndex):
    #     for i in range(min(oldVisualIndex, newVisualIndex), self.count()):
    #         logical = self.logicalIndex(i)
    #         if i < len(self.comboboxes):
    #             self.comboboxes[i].setGeometry(self.sectionViewportPosition(logical), 0, self.sectionSize(logical) - 5,
    #                                            self.height())
    #
    #     # 마지막 헤더인 경우
    #     if newVisualIndex == self.count() - 1:
    #         self.setSortIndicator(self.count() - 2, Qt.AscendingOrder)
    #         self.sortByColumn(self.count() - 2, Qt.AscendingOrder)
    #     elif oldVisualIndex == self.count() - 1:
    #         self.setSortIndicator(self.count() - 2, Qt.AscendingOrder)
    #         self.sortByColumn(self.count() - 2, Qt.AscendingOrder)

    # def set_header_labels(self, labels):
    #     model = QtGui.QStandardItemModel()
    #     model.setHorizontalHeaderLabels(labels)
    #     self.setModel(model)
    #     self.comboboxes = []  # comboboxes 리스트 초기화
    #     self.fixComboPositions()
    #
    # def fixComboPositions(self):
    #     for i in range(self.count()):
    #         if i < len(self.comboboxes):
    #             combo = self.comboboxes[i]
    #         else:
    #             combo = QtWidgets.QComboBox(self)
    #             combo.addItems(['All', 'Option 1', 'Option 2'])
    #             self.comboboxes.append(combo)
    #
    #         combo.setGeometry(self.sectionViewportPosition(i), 0, self.sectionSize(i) - 4, self.height())
    #         combo.show()
    #
    #     if len(self.comboboxes) > self.count():
    #         for i in range(self.count(), len(self.comboboxes)):
    #             self.comboboxes[i].deleteLater()
    #         self.comboboxes = self.comboboxes[:self.count()]


class Table(QTableView):
    """
    task 선택하는 TableView
    """
    def __init__(self):
        QTableView.__init__(self)

        # self.setSortingEnabled(True)

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        self.setFont(font)

        self.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter)
        self.verticalHeader().setDefaultAlignment(Qt.AlignVCenter)

        self.vertical_header = self.verticalHeader()

        self.horizontalHeader().setMinimumSectionSize(50)
        self.verticalHeader().setMinimumSectionSize(50)

        self.horizontalHeader().setStretchLastSection(True)

        self.setStyleSheet("background-color: #353535; selection-background-color: gray;")
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSortIndicatorShown(True)
        self.horizontalHeader().setSectionsClickable(True)




class Table2(QtWidgets.QTableView):
    """
    asset 선택하는 TableView
    """
    def __init__(self, data=None):
        super(Table2, self).__init__()

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

        # # 고정된 행과 열 모드 설정
        # self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # self.setCornerButtonEnabled(False)

        self.horizontal_header.setMinimumSectionSize(100)
        self.vertical_header.setMinimumSectionSize(100)

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
        model.setHorizontalHeaderLabels(['Asset', 'Camera', 'Undistorted Image'])

        for row in data:
            items = [QtGui.QStandardItem(str(item)) for item in row]
            model.appendRow(items)

        self.setModel(model)
        self.resizeColumnsToContents()
        self.horizontal_header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)



