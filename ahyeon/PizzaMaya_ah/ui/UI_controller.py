# coding=utf-8

import os
import sys
import gazu

from PizzaMaya_ah.code import filter
from PizzaMaya_ah.code import thumbnail
from PizzaMaya_ah.code import login
from UI_view_save import Save
from UI_view_load import Load
from UI_view_table import Table
from UI_view_table import Table2
from UI_view_login import LoginWindow
from PySide2 import QtWidgets, QtCore, QtUiTools
from PySide2.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        # Load main window UI
        QMainWindow.__init__(self)
        ui_path = os.path.expanduser('/home/rapa/git/pizza/kkw/PJT_2st/Maya_Api.ui')
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        # 메인 윈도우의 레이아웃에 TableView 2개 추가
        self.table = Table(self.read_data())
        self.ui.verticalLayout2.addWidget(self.table, 0)

        self.table2 = Table2(self.read_data2())
        self.ui.verticalLayout.addWidget(self.table2, 0)

        # 프로그램 시작 시 auto login이 체크되어 있는지 확인하며, 체크되어 있으면 바로 main window 띄움
        self.login_window = LoginWindow()
        self.login = login.LogIn()
        value = self.login.load_setting()
        if value and value['auto_login'] and value['valid_host'] and value['valid_user'] is True:
            self.ui.show()
        else:
            self.login_window.ui.show()

        # ----------------------------------------------------------------------------------------------

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
        self.ui.Load_Button.clicked.connect(self.Load_Button)
        self.load = Load()

    # ----------------------------------------------------------------------------------------------
    # save 또는 load 버튼 누르면 save 또는 load 윈도우를 호출

    def save_button(self):
        self.ui.hide()  ##### 메인 윈도우를 숨길 필요 있는지? 그냥 겹쳐서 띄우면 안되나 exec로
        self.save.ui.show()

    def load_button(self):
        self.ui.hide()  # 메인 윈도우 숨김
        self.load.ui.show()

    # ----------------------------------------------------------------------------------------------
    # 정보 입력 후 로그인 버튼을 클릭하면 Kitsu에 로그인을 하고, 오토로그인이 체크되어있는지 판별
    # 로그아웃 버튼 클릭 시 Kitsu에서 로그아웃을 하고, 메인 윈도우 hide한 뒤 로그인 윈도우 띄움

    def login_button(self):
        host_box = self.Login.ui.Host_box
        id_box = self.Login.ui.ID_box
        pw_box = self.Login.ui.PW_box

        self.login.host = host_box.text()
        self.login.user_id = id_box.text()
        self.login.user_pw = pw_box.text()
        self.login.auto_login = self.Login.ui.Auto_Login_Check.isChecked()

        if self.login.connect_host() and self.login.log_in():
            self.login_window.ui.hide()     ###### close가 아니라 hide 해야 하는지?
            self.ui.show()

    def logout_button(self):
        self.login.log_out()
        self.ui.hide()
        self.login_window.ui.show()

    # ----------------------------------------------------------------------------------------------
    # TableView의 항목을 클릭하면 항목의 정보를 프린트 해줌

    def table_clicked(self, event):
        selected_data = self.read_data()[event.row()]
        print(selected_data)

    def table_clicked2(self, event):
        selected_data = self.read_data2()[event.row()]
        print(selected_data)

    # ----------------------------------------------------------------------------------------------
    # TableView 두개에 띄울 각각의 정보를 넣어둠

    @staticmethod
    def read_data():
        """
        task 선택하는 TableView의 데이터

        filter의 선택에 따라 정보가 바뀐다.

        Returns:

        """
        ft = filter.Filter()
        data = [
            ['Avata', '1', '2023-03-02', '123', 'abcd'],
            ['TopGun', '2', '2023-03-03', '456', 'efgh'],
            ['DontLookUp', '3', '2023-03-04', '789', 'ijkl'],
            ['Flash', '4', '2023-03-05', '456', 'mnop'],
            ['DDong', '5', '2023-03-06', '123', 'qrstu'],
            ['DDong', '6', '2023-03-06', '123', 'qrstu'],
            ['DDong', '7', '2023-03-06', '123', 'qrstu'],
            ['DDong', '8', '2023-03-06', '123', 'qrstu'],
            ['DDong', '9', '2023-03-06', '123', 'qrstu'],
            ['DDong', '10', '2023-03-06', '123', 'qrstu'],
            ['DDong', '11', '2023-03-06', '123', 'qrstu'],
            ['DDong', '12', '2023-03-06', '123', 'qrstu'],
            ['DDong', '13', '2023-03-06', '123', 'qrstu'],
            ['DDong', '14', '2023-03-06', '123', 'qrstu'],
            ['DDong', '15', '2023-03-06', '123', 'qrstu'],
            ['DDong', '16', '2023-03-06', '123', 'qrstu'],
            ['DDong', '17', '2023-03-06', '123', 'qrstu'],
            ['DDong', '18', '2023-03-06', '123', 'qrstu'],
            ['DDong', '19', '2023-03-06', '123', 'qrstu'],
            ['DDong', '20', '2023-03-06', '123', 'qrstu']
        ]
        return data

    @staticmethod
    def read_data2():
        """
        asset, camera, undi_img 선택하는 TableView의 데이터

        task 선택 후 data가 생성된다.

        Returns:

        """
        # 썸네일을 얻기 위해 받아와야 하는 정보
        project = gazu.project.get_project_by_name('jeongtae')
        asset = gazu.asset.get_asset_by_name(project, 'chair')
        task_type = gazu.task.get_task_type_by_name('Layout_asset')
        task = gazu.task.get_task_by_entity(asset, task_type)

        png = thumbnail.thumbnail_control([task])
        data = [
            [png, 'Avata', '2023-03-02']
        ]
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
    