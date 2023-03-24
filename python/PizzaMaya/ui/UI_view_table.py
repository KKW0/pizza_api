# coding=utf-8

from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtWidgets import QTableView, QHeaderView

from PizzaMaya.code.filter import Filter


class HorizontalHeader(QtWidgets.QHeaderView):
    """
    헤더에 콤보박스를 추가하는 클래스이다.
    """
    def __init__(self, parent=None):
        """
        변수들을 정의하고 모듈의 인스턴스를 생성하고 sort버튼의 값을 생성한다.
        """
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

        # 헤더 셀렉션 옵션 설정
        self.setSectionResizeMode(QHeaderView.Fixed)
        self.setStretchLastSection(True)
        self.setSectionsMovable(False)
        self.setSectionsClickable(True)

        # 헤더의 sort 버튼 설정
        self.setSortIndicator(-1, Qt.AscendingOrder)
        self.sort_button = QtWidgets.QPushButton(self)
        self.sort_button.setText("Sort")
        self.sort_button.setGeometry(self.sectionViewportPosition(2), 0, self.sectionSize(2) - 0, self.height())
        self.sort_button.clicked.connect(self.sort_clicked)
        self.sort_button.show()

    def sort_clicked(self):
        """
        sort버튼을 클릭하면 proxy model을 오름차순 또는 내림차순으로 정렬한다.
        """
        if self.seq_index != 0:
            self.proxy_model2.sort(self.seq_index, self.sortOrder())
        elif self.proj_index != 0:
            self.proxy_model.sort(self.proj_index, self.sortOrder())
        else:  # proj_index와 seq_index가 모두 0인 경우        # 수정필요
            self.model.sort(self.logicalIndexAt(0), self.sortOrder())

    def sortIndicatorChanged(self, logical_index, order):
        """
        헤더인덱스의 변경사항에 따라 테이블의 정보를 변경하는 메서드
        이 메서드는 헤더뷰의 서브클래스이다.
        """
        if logical_index == 2:
            self.seq_index = 0
            self.proj_index = 0
            self.combo2.setCurrentIndex(0)
            if self.proxy_model2 is not None:
                self.proxy_model2.invalidate()
            elif self.proxy_model is not None:
                self.proxy_model.invalidate()
        super(HorizontalHeader, self).sortIndicatorChanged(logical_index, order)

    def showEvent(self, event):
        """
        생성한 콤보박스를 보여주는 메서드
        ft.collect_info_task 이 함수를 통해 콤보박스의 요소를 불러온다.
        """
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
        """
            콤보박스1의 선택사항이 달려졌음을 알려주는 메서드
            그에따라 프록시모델로 테이블뷰1의 내용을 변경한다.
        """
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
        """
        콤보박스2의 선택사항이 달려졌음을 알려주는 메서드
        그에따라 프록시모델2로 테이블뷰1의 내용을 변경한다.
        """
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
    프로젝트와 시퀀스 분류에 따라 task를 선택하는 TableView
    """
    def __init__(self):
        """
        헤더와 스타일을 설정한다.
        """
        QTableView.__init__(self)

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        self.setFont(font)

        self.setSortingEnabled(True)
        self.vertical_header = self.verticalHeader()
        self.horizontal_header = self.horizontalHeader()
        self.vertical_header.setDefaultAlignment(Qt.AlignVCenter)
        self.horizontal_header.setDefaultAlignment(Qt.AlignHCenter)

        self.vertical_header.setMinimumSectionSize(50)
        self.horizontal_header.setMinimumSectionSize(50)
        self.vertical_header.setSectionResizeMode(QHeaderView.Fixed)
        self.horizontal_header.setFont(font)  # 헤더에 폰트 설정
        self.horizontal_header.setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.setStyleSheet("background-color: #353535; selection-background-color: gray;")
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.horizontal_header.setSectionsClickable(True)
        self.horizontal_header.setSortIndicatorShown(True)
        self.horizontal_header.setStretchLastSection(True)


class Table2(QtWidgets.QTableView):
    """
    테스크가 주어진 레이아웃어셋에 캐스팅된 asset 중 작업파일에 임포트 할 asset을 선택하는 TableView
    """
    def __init__(self, corner=False):
        """
        헤더와 스타일을 설정한다.
        데이터를 설정해준다.
        """
        super(Table2, self).__init__()

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        self.setFont(font)
        self.corner = corner

        # QTableView Headers
        self.vertical_header = self.verticalHeader()
        self.horizontal_header = self.horizontalHeader()

        # 고정된 헤더 모드 설정
        self.vertical_header.setSectionResizeMode(QHeaderView.Fixed)
        self.horizontal_header.setSectionResizeMode(QHeaderView.Fixed)

        self.horizontal_header.setFont(font)  # 헤더에 폰트 설정
        self.horizontal_header.setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.vertical_header.setMinimumSectionSize(100)
        self.horizontal_header.setMinimumSectionSize(100)
        self.horizontal_header.setStretchLastSection(True)

        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        if self.corner:
            self.setStyleSheet(
                "background-color: #353535; selection-background-color: gray;};")
            corner_button = self.findChild(QtWidgets.QAbstractButton)
            corner_button.setStyleSheet("background-color: #ABABAB; color: black;")
