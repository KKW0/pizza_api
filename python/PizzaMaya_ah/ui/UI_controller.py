# coding=utf-8

import os
import sys
import gazu
import pprint as pp

from PizzaMaya_ah.code.login import LogIn
from PizzaMaya_ah.code.filter import Filter
from PizzaMaya_ah.code.usemaya import MayaThings
from PizzaMaya_ah.code.thumbnail import thumbnail_control

from PizzaMaya_ah.ui.UI_view_save import Save
from PizzaMaya_ah.ui.UI_view_table import Table
from PizzaMaya_ah.ui.UI_view_table import Table2
from PizzaMaya_ah.ui.UI_view_table import Table3
from PizzaMaya_ah.ui.UI_view_table import HorizontalHeader
from PizzaMaya_ah.ui.UI_view_login import LoginWindow
from PizzaMaya_ah.ui.UI_model import CustomTableModel
from PizzaMaya_ah.ui.UI_model import CustomTableModel2
from PizzaMaya_ah.ui.UI_model import CustomTableModel3
from PySide2 import QtWidgets, QtCore, QtUiTools
from PySide2.QtWidgets import QMainWindow, QMessageBox
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, values=None, parent=None, size_policy=None):
        super(MainWindow, self).__init__()
        # 현재 작업 디렉토리 경로를 가져옴

        self.task = None
        self.my_task = None
        self.task_num = None
        self.my_shots = None
        self.task_info = None
        # self.row_index_list = []
        self.preview_pixmap = None
        self.undi_info_list = None
        self.camera_info_list = None
        self.casting_info_list = None
        self.task_clicked_index = None
        self.my_shot_index_list = []
        self.selected_index_list = []  # 선택한 에셋들의 인덱스 번호
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
        self.horizontal_header = HorizontalHeader()
        self.table.setHorizontalHeader(self.horizontal_header)

        self.table2 = Table2()
        self.ui.verticalLayout.addWidget(self.table2, 0)

        self.table3 = Table3()
        self.ui.verticalLayout3.addWidget(self.table3, 0)

        # Getting the Model
        self.table1_model = CustomTableModel()
        self.table.setModel(self.table1_model)

        self.table2_model = CustomTableModel2()
        self.table2.setModel(self.table2_model)

        self.table3_model = CustomTableModel3()
        self.table3.setModel(self.table3_model)

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
        self.ma = MayaThings()

        # ----------------------------------------------------------------------------------------------

        # Login 버튼, Logout 버튼 연결
        self.login_window.ui.Login_Button.clicked.connect(self.login_button)
        self.ui.Logout_Button.clicked.connect(self.logout_button)
        # Login 버튼, Logout 버튼 연결
        self.login_window.ui.Login_Button.clicked.connect(self.login_button)
        self.ui.Logout_Button.clicked.connect(self.logout_button)

        # TableView 3개 연결
        self.table.clicked.connect(self.table_clicked)
        self.table2.clicked.connect(self.table_clicked2)
        self.table3.clicked.connect(self.table_clicked3)

        # Save 클릭시 Save ui로 전환, Load 클릭시 로드됨
        self.ui.Save_Button.clicked.connect(self.save_button)
        self.ui.Load_Button.clicked.connect(self.load_button)
        self.save = Save()

        # 에셋 여러개 선택
        self.table2.selectionModel().selectionChanged.connect(self.selection_changed)

    def selection_changed(self, selected, deselected):
        selection_model = self.table2.selectionModel()
        selected_rows = selection_model.selectedRows()
        selected_indexes = selection_model.selectedIndexes()
        row_count = self.table2_model.row_count

        sel_asset_ids = set()
        for sel_idx in selected_indexes:
            sel_asset_ids.add(sel_idx.row())
        self.selected_index_list = sel_asset_ids
        # self.row_index_list.append(selected_indexes[0].row())

        self.ui.Selection_Lable.setText('Selected Files %d / %d' % (len(selected_rows), row_count))
        print(self.ui.Selection_Lable.text())

    # ----------------------------------------------------------------------------------------------
    # save 또는 load 버튼 누르면 save 또는 load 윈도우를 호출

    def save_button(self):
        # self.ui.hide()  ##### 메인 윈도우를 숨길 필요 있는지? 그냥 겹쳐서 띄우면 안되나 exec로
        self.save.ui.show()

    def load_button(self):
        if not self.my_task:
            return
        else:
            # screen_resolution = QtWidgets.QDesktopWidget().screenGeometry()
            # screen_center = screen_resolution.center()

            reply = QMessageBox.question(self, 'Confirmation', '{0}개의 에셋과 {1}개의 샷을 로드하시겠습니까?' \
                                         .format(len(self.selected_index_list), (len(self.my_shot_index_list))),
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            # reply.move(screen_center - reply.rect().center())
            if reply == QMessageBox.Yes:
                my_layout_asset = gazu.asset.get_asset(self.my_task['entity_id'])
                self.ma.import_casting_asset(my_layout_asset, self.selected_index_list)
                for index in self.my_shot_index_list:
                    shot_list = gazu.casting.get_asset_cast_in(self.my_task['entity_id'])
                    self.ma.import_cam_seq(shot_list[index])
                self.ui.close()
                QMessageBox.information(self, 'Completed', '로드되었습니다!', QMessageBox.Ok)
                # QMessageBox.move(screen_center - QMessageBox.rect().center())

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
            self.undi_info_list, self.camera_info_list = self.ft.select_task(self.horizontal_header.proj_index,
                                                                             self.horizontal_header.seq_index,
                                                                             self.task_clicked_index)
        tup, _, _, _ = thumbnail_control(self.my_task, self.task_clicked_index,
                                         self.casting_info_list, self.undi_info_list)
        png = bytes(tup)

        self.preview_pixmap = QPixmap()
        self.preview_pixmap.loadFromData(png)
        label = self.ui.Preview
        label.setPixmap(self.preview_pixmap.scaled(label.size(), Qt.KeepAspectRatio))

        self.ui.InfoTextBox.setPlainText('Project Name: {}'.format(task_info['project_name'] + '\n'))
        self.ui.InfoTextBox.appendPlainText('Description: {0}'.format(task_info['description']))
        self.ui.InfoTextBox.appendPlainText('Due Date: {0}'.format(task_info['due_date']))
        self.ui.InfoTextBox.appendPlainText('Comment: {0}'.format(str(task_info['last_comment']['text'])))

        self.table2_model.load_data2(self.read_data2())
        self.table2_model.layoutChanged.emit()

        self.table3_model.load_data3(self.read_data3())
        self.table3_model.layoutChanged.emit()

    def table_clicked2(self, event):
        clicked_cast = self.casting_info_list[event.row()]

        _, asset_thumbnail_list, _, _ = thumbnail_control(self.my_task, self.task_clicked_index,
                                                          self.casting_info_list, undi_info_list=[])
        png = bytes(asset_thumbnail_list[event.row()])

        self.preview_pixmap = QPixmap()
        self.preview_pixmap.loadFromData(png)
        label = self.ui.Preview
        label.setPixmap(self.preview_pixmap.scaled(label.size(), Qt.KeepAspectRatio))

        self.ui.InfoTextBox.setPlainText('Asset Name: {}'.format(clicked_cast['asset_name']+'\n'))
        self.ui.InfoTextBox.appendPlainText('Description: {0}'.format(clicked_cast['description']))
        self.ui.InfoTextBox.appendPlainText('Asset Type: {0}'.format(clicked_cast['asset_type_name']))
        self.ui.InfoTextBox.appendPlainText('Occurence: {0}'.format(str(clicked_cast['nb_occurences'])))
        self.ui.InfoTextBox.appendPlainText('Output File: {0}'.format(str(len(clicked_cast['output']))))
        self.ui.InfoTextBox.appendPlainText('Newest or Not: Not')   # 모든 아웃풋 파일들이 전부 최신 리비전이면 YES로 표기

    def table_clicked3(self, event):
        clicked_undi = self.undi_info_list[event.row()][0]
        clicked_cam = self.camera_info_list[event.row()][0]
        _, _, undi_thumbnail_list, _ = thumbnail_control(self.my_task, self.task_clicked_index,
                                                         [], self.undi_info_list)
        png = bytes(undi_thumbnail_list[event.row()])

        self.preview_pixmap = QPixmap()
        self.preview_pixmap.loadFromData(png)
        label = self.ui.Preview
        label.setPixmap(self.preview_pixmap.scaled(label.size(), Qt.KeepAspectRatio))

        selection_model = self.table3.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        sel_shot_idexes = set()
        for sel_idx in selected_indexes:
            sel_shot_idexes.add(sel_idx.row())
        self.my_shot_index_list = sel_shot_idexes

        self.ui.InfoTextBox.setPlainText('[Shot Info]')
        self.ui.InfoTextBox.appendPlainText('Shot Name: {}'.format(clicked_undi['shot_name'] + '\n'))
        self.ui.InfoTextBox.appendPlainText('[Undistortion Image Info]')
        self.ui.InfoTextBox.appendPlainText('Frame Range: {}'.format(clicked_undi['frame_range']))
        self.ui.InfoTextBox.appendPlainText('Description: {0}'.format(clicked_undi['description']))
        st = '\n'
        new_str = st.lstrip()
        self.ui.InfoTextBox.appendPlainText(new_str)
        self.ui.InfoTextBox.appendPlainText('[Camera Info]')
        self.ui.InfoTextBox.appendPlainText('Asset Type: {0}'.format(clicked_cam['output_type_name']))
        self.ui.InfoTextBox.appendPlainText('Description: {0}'.format(str(clicked_cam['description'])))

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
            _, asset_thumbnail_list, _, shot_list = \
                thumbnail_control(self.my_task, 0, self.casting_info_list, self.undi_info_list)
            # 캐스팅된 에셋목록 추가
            for index, cast in enumerate(self.casting_info_list):
                if len(cast['output']) == 0:
                    data.append([asset_thumbnail_list[index], cast['asset_name'], 'No Output File to Load'])
                else:
                    data.append([asset_thumbnail_list[index], cast['asset_name'], cast['asset_type_name']])
            return data
        else:
            return data

    def read_data3(self):
        data = []
        if self.my_task is not None:
            _, _, undi_thumbnail_list, shot_list = \
                thumbnail_control(self.my_task, 0, self.casting_info_list, self.undi_info_list)
            # 샷 목록 추가
            for index, info_list in enumerate(self.undi_info_list):
                data.append([undi_thumbnail_list[index], shot_list[index]['shot_name']])
            return data
        else:
            return data


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
