# coding=utf-8

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QTableView, QComboBox, QStyledItemDelegate, QHeaderView



class HorizontalHeader(QtWidgets.QHeaderView):
    def __init__(self, parent=None):
        super(HorizontalHeader, self).__init__(QtCore.Qt.Horizontal, parent)
        self.setSectionsMovable(True)
        self.comboboxes = []
        self.sort_button = None  # 정렬 버튼
        self.sectionResized.connect(self.handleSectionResized)
        self.sectionMoved.connect(self.handleSectionMoved)

    def showEvent(self, event):
        for i in range(self.count()):
            if i < len(self.comboboxes):
                combo = self.comboboxes[i]
                combo.clear()
                combo.addItems(['All', 'Option 1', 'Option 2'])
            else:
                combo = QtWidgets.QComboBox(self)
                combo.addItems(['All', 'Option 1', 'Option 2'])
                self.comboboxes.append(combo)

            combo.setGeometry(self.sectionViewportPosition(i), 0, self.sectionSize(i) - 4, self.height())
            combo.show()

        # 마지막 헤더일 경우 정렬 버튼 생성
        if self.sort_button is None and i == self.count() - 1:
            self.sort_button = QtWidgets.QPushButton(self)
            self.sort_button.setText("Due Date")
            self.sort_button.setGeometry(self.sectionViewportPosition(i), 0, self.sectionSize(i) - 4, self.height())
            self.sort_button.show()
            self.sort_button.clicked.connect(self.handleSortButtonClicked)

        # comboboxes 리스트 크기가 count() 보다 큰 경우 삭제
        if len(self.comboboxes) > self.count():
            for i in range(self.count(), len(self.comboboxes)):
                self.comboboxes[i].deleteLater()

        super(HorizontalHeader, self).showEvent(event)

    def handleSortButtonClicked(self):
        # 마지막 헤더 클릭 시 정렬
        self.parent().sortByColumn(self.count() - 1, Qt.AscendingOrder)

    def handleSectionResized(self, i):
        for i in range(self.count()):
            j = self.visualIndex(i)
            logical = self.logicalIndex(j)
            if i < len(self.comboboxes):
                self.comboboxes[i].setGeometry(self.sectionViewportPosition(logical), 0, self.sectionSize(logical) - 4, self.height())

        # 정렬 버튼 위치 조정
        if self.sort_button:
            self.sort_button.setGeometry(self.sectionViewportPosition(self.count() - 1), 0, self.sectionSize(self.count() - 1) - 4, self.height())

    def handleSectionMoved(self, i, oldVisualIndex, newVisualIndex):
        for i in range(min(oldVisualIndex, newVisualIndex), self.count()):
            logical = self.logicalIndex(i)
            if i < len(self.comboboxes):
                self.comboboxes[i].setGeometry(self.sectionViewportPosition(logical), 0, self.sectionSize(logical) - 5,
                                               self.height())

        # 마지막 헤더인 경우
        if newVisualIndex == self.count() - 1:
            self.setSortIndicator(self.count() - 2, Qt.AscendingOrder)
            self.sortByColumn(self.count() - 2, Qt.AscendingOrder)
        elif oldVisualIndex == self.count() - 1:
            self.setSortIndicator(self.count() - 2, Qt.AscendingOrder)
            self.sortByColumn(self.count() - 2, Qt.AscendingOrder)

    def set_header_labels(self, labels):
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(labels)
        self.setModel(model)
        self.comboboxes = []  # comboboxes 리스트 초기화
        self.fixComboPositions()

    def fixComboPositions(self):
        for i in range(self.count()):
            if i < len(self.comboboxes):
                combo = self.comboboxes[i]
            else:
                combo = QtWidgets.QComboBox(self)
                combo.addItems(['All', 'Option 1', 'Option 2'])
                self.comboboxes.append(combo)

            combo.setGeometry(self.sectionViewportPosition(i), 0, self.sectionSize(i) - 4, self.height())
            combo.show()

        if len(self.comboboxes) > self.count():
            for i in range(self.count(), len(self.comboboxes)):
                self.comboboxes[i].deleteLater()
            self.comboboxes = self.comboboxes[:self.count()]



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



