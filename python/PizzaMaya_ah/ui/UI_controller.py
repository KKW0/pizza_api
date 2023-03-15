# coding=utf-8

import os
import sys
import pprint as pp

from PizzaMaya_ah.code.login import LogIn
from PizzaMaya_ah.code.filter import Filter
from PizzaMaya_ah.code.thumbnail import thumbnail_control

from PizzaMaya_ah.ui.UI_view_save import Save
from PizzaMaya_ah.ui.UI_view_load import Load
from PizzaMaya_ah.ui.UI_view_table import Table
from PizzaMaya_ah.ui.UI_view_table import Table2
from PizzaMaya_ah.ui.UI_view_table import HorizontalHeader
from PizzaMaya_ah.ui.UI_view_login import LoginWindow
from PizzaMaya_ah.ui.UI_model import CustomTableModel
from PizzaMaya_ah.ui.UI_model import CustomTableModel2

from PySide2 import QtWidgets, QtCore, QtUiTools
from PySide2.QtWidgets import QMainWindow
from PySide2.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self, values=None, parent=None):
        super(MainWindow, self).__init__()
        # 현재 작업 디렉토리 경로를 가져옴

        self.task = None
        self.my_task = None
        self.task_num = None
        self.my_shots = None
        self.task_info = None
        self.row_index_list = []
        self.preview_pixmap = None
        self.undi_info_list = None
        self.camera_info_list = None
        self.casting_info_list = None
        self.task_clicked_index = None
        cwd = os.path.dirname(os.path.abspath(__file__))
        # ui 파일 경로 생성
        ui_path = os.path.join(cwd, 'UI_design', 'Main.ui')
        # ui 파일이 존재하는지 확인
        if not os.path.exists(ui_path):
            raise Exception("UI file not found at: {0}".format(ui_path))

        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        # 메인 윈도우의 레이아웃에 TableView 2개 추가
        self.table = Table()
        self.ui.verticalLayout2.addWidget(self.table, 0)
        self.horizontalHeader = HorizontalHeader()
        self.table.setHorizontalHeader(self.horizontalHeader)

        # self.table.horizontalHeader().sectionClicked.connect(self.filter_list)
        # self.horizontalHeader.combo.currentTextChanged.connect(self.combobox_changed1)
        # self.horizontalHeader.combo2.currentTextChanged.connect(self.combobox_changed2)

        self.table2 = Table2()
        self.ui.verticalLayout.addWidget(self.table2, 0)


        # Getting the Model
        self.table1_model = CustomTableModel()
        self.table.setModel(self.table1_model)

        self.table2_model = CustomTableModel2()
        self.table2.setModel(self.table2_model)

        # 프로그램 시작 시 auto login이 체크되어 있는지 확인하며, 체크되어 있으면 바로 main window 띄움
        self.login_window = LoginWindow()
        self.login = LogIn()

        value = self.login.load_setting()
        if value and value['auto_login'] and value['valid_host'] and value['valid_user'] is True:

            self.login.host = value['host']
            self.login.user_id = value['user_id']
            self.login.user_pw = value['user_pw']
            self.login.auto_login = value['auto_login']
            self.login.connect_host()
            self.login.log_in()
            self.ui.show()

            # Set table1 data
            self.table1_model.load_data(self.read_data())
            self.table1_model.layoutChanged.emit()
        else:
            self.login_window.ui.show()

        self.ft = Filter()

        # ----------------------------------------------------------------------------------------------

        # Login 버튼, Logout 버튼 연결
        self.login_window.ui.Login_Button.clicked.connect(self.login_button)
        self.ui.Logout_Button.clicked.connect(self.logout_button)
        # Login 버튼, Logout 버튼 연결
        self.login_window.ui.Login_Button.clicked.connect(self.login_button)
        self.ui.Logout_Button.clicked.connect(self.logout_button)

        # TableView 2개 연결
        self.table.clicked.connect(self.table_clicked)
        self.table2.clicked.connect(self.table_clicked2)


        # Save 클릭시 Save ui로 전환
        self.ui.Save_Button.clicked.connect(self.save_button)
        self.save = Save()

        # Load 클릭시 Load ui로 전환
        self.ui.Load_Button.clicked.connect(self.load_button)
        self.load = Load()

        self.table2.selectionModel().selectionChanged.connect(self.selection_changed)

    def selection_changed(self, selected, deselected):
        selection_model = self.table2.selectionModel()
        selected_rows = selection_model.selectedRows()
        selected_indexes = selection_model.selectedIndexes()
        row_count = self.table2_model.row_count

        print(selected_indexes[0].row())
        self.row_index_list.append(selected_indexes[0].row())

        self.ui.Selection_Lable.setText('Selected Files %d / %d' % (len(selected_rows), row_count))
        print(self.ui.Selection_Lable.text())

    # def combobox_changed1(self, event):
    #     print(event)
    #
    # def combobox_changed2(self, event):
    #     print(event)


    # ----------------------------------------------------------------------------------------------
    # save 또는 load 버튼 누르면 save 또는 load 윈도우를 호출

    def save_button(self):
        # self.ui.hide()  ##### 메인 윈도우를 숨길 필요 있는지? 그냥 겹쳐서 띄우면 안되나 exec로
        self.save.ui.show()

    def load_button(self):
        # self.ui.hide()  # 메인 윈도우 숨김
        self.load.my_task = self.my_task
        self.load.my_shots = self.my_shots
        self.load.selected_index_list = list(set(self.row_index_list))
        self.load.ui.show()

    # ----------------------------------------------------------------------------------------------
    # 정보 입력 후 로그인 버튼을 클릭하면 Kitsu에 로그인을 하고, 오토로그인이 체크되어있는지 판별
    # 로그아웃 버튼 클릭 시 Kitsu에서 로그아웃을 하고, 메인 윈도우 hide한 뒤 로그인 윈도우 띄움

    def login_button(self):
        host_box = self.login_window.ui.Host_Box
        id_box = self.login_window.ui.ID_Box
        pw_box = self.login_window.ui.PW_Box

        self.login.host = host_box.text()
        self.login.user_id = id_box.text()
        self.login.user_pw = pw_box.text()
        self.login.auto_login = self.login_window.ui.Auto_Login_Check.isChecked()

        if self.login.connect_host() and self.login.log_in():
            self.login_window.ui.hide()     ###### close가 아니라 hide 해야 하는지?
            self.ui.show()

            # Set table1 data
            self.table1_model.load_data(self.read_data())
            self.table1_model.layoutChanged.emit()

    def logout_button(self):
        self.login.log_out()
        self.ui.hide()
        self.login_window.ui.show()

    # ----------------------------------------------------------------------------------------------
    # TableView의 항목을 클릭하면 항목의 정보를 프린트 해줌

    def table_clicked(self, event):
        self.task_clicked_index = event.row()
        self.my_task, task_info, self.casting_info_list,\
            self.undi_info_list, self.camera_info_list = self.ft.select_task(task_num=self.task_clicked_index)
        tup, _, _, _ = thumbnail_control(self.my_task, self.task_clicked_index,
                                         self.casting_info_list, self.undi_info_list)
        png = bytes(tup)
        self.preview_pixmap = QPixmap()

        self.preview_pixmap.loadFromData(png)
        self.preview_pixmap = self.preview_pixmap.scaled(360, 300)
        label = self.ui.Preview
        label.setPixmap(self.preview_pixmap)

        self.ui.InfoTextBox.setPlainText('Project Name: {}'.format(task_info['project_name'] + '\n'))
        self.ui.InfoTextBox.appendPlainText('Description: {0}'.format(task_info['description']))
        self.ui.InfoTextBox.appendPlainText('Due Date: {0}'.format(task_info['due_date']))
        self.ui.InfoTextBox.appendPlainText('Comment: {0}'.format(str(task_info['last_comment'])))

        self.table2_model.load_data2(self.read_data2())
        self.table2_model.layoutChanged.emit()

    def table_clicked2(self, event):
        clicked_cast = self.casting_info_list[event.row()]

        _, asset_thumbnail_list, _, _ = thumbnail_control(self.my_task, self.task_clicked_index,
                                                          self.casting_info_list, undi_info_list=[])
        png = bytes(asset_thumbnail_list[event.row()])

        self.preview_pixmap = QPixmap()
        self.preview_pixmap.loadFromData(png)
        self.preview_pixmap = self.preview_pixmap.scaled(360, 300)
        label = self.ui.Preview
        label.setPixmap(self.preview_pixmap)

        self.ui.InfoTextBox.setPlainText('Asset Name: {}'.format(clicked_cast['asset_name']+'\n'))
        self.ui.InfoTextBox.appendPlainText('Description: {0}'.format(clicked_cast['description']))
        self.ui.InfoTextBox.appendPlainText('Asset Type: {0}'.format(clicked_cast['asset_type_name']))
        self.ui.InfoTextBox.appendPlainText('Occurence: {0}'.format(str(clicked_cast['nb_occurences'])))
        self.ui.InfoTextBox.appendPlainText('Output File: {0}'.format(str(len(clicked_cast['output']))))
        self.ui.InfoTextBox.appendPlainText('Newest or Not: Not')   # 모든 아웃풋 파일들이 전부 최신 리비전이면 YES로 표기

    # ----------------------------------------------------------------------------------------------
    # TableView 두개에 띄울 각각의 정보를 넣어둠

    def read_data(self):
        """
        task 선택하는 TableView의 데이터

        filter의 선택에 따라 정보가 바뀐다.

        Returns:

        """
        ft = Filter()
        self.task, task_info, _, _, _ = ft.select_task()
        data = []
        for index in range(len(task_info)):
            data.append([task_info[index]['project_name'], task_info[index]['sequence_name'],
                         task_info[index]['due_date']])

        return data

    def read_data2(self):
        """
        asset, camera, undi_img 선택하는 TableView의 데이터

        task 선택 후 data가 생성된다.

        Returns:

        """
        # 썸네일을 얻기 위해 받아와야 하는 정보
        data = []
        if self.my_task is not None:
            _, asset_thumbnail_list, undi_thumbnail_list, shot_list = \
                thumbnail_control(self.my_task, 0, self.casting_info_list, self.undi_info_list)
            # 캐스팅된 에셋목록 추가
            for index, cast in enumerate(self.casting_info_list):
                data.append([asset_thumbnail_list[index], cast['asset_name'], cast['asset_type_name']])
            # 샷 목록 추가
            for index, info_list in enumerate(self.undi_info_list):
                data.append([undi_thumbnail_list[index], shot_list[index]['shot_name'], 'Shot'])
            return data
        else:
            return data

    # ----------------------------------------------------------------------------------------------
    # 테이블 모델 필터링
    # def filter_list(self, index):
    #     option = self.table.combo_box.currentText()
    #     option2 = self.table.combo_box2.currentText()
    #
    #     proxy_model = QtCore.QSortFilterProxyModel()
    #     proxy_model.setSourceModel(self.table1_model)
    #
    #     if option != 'All':
    #         proxy_model.setFilterRegExp('^{}$'.format(option))
    #         proxy_model.setFilterKeyColumn(0)
    #         self.table.combo_box2.setDisabled(False)
    #     else:
    #         self.table.combo_box2.setCurrentIndex(0)
    #         option2 = 'All'
    #         self.table.combo_box2.setDisabled(True)
    #
    #     if option2 != 'All':
    #         proxy_model2 = QtCore.QSortFilterProxyModel()
    #         proxy_model2.setSourceModel(proxy_model)
    #         proxy_model2.setFilterRegExp('^{}$'.format(option2))
    #         proxy_model2.setFilterKeyColumn(1)
    #         self.setModel(proxy_model2)
    #     else:
    #         self.setModel(proxy_model)


    # ----------------------------------------------------------------------------------------------


def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    try:
        app = QtWidgets.QApplication().instance()
    except TypeError:
        app = QtWidgets.QApplication()
    myapp = MainWindow()
    myapp.ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
