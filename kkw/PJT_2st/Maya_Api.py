# coding=utf-8

import os
import sys
import gazu

from Save import Save
from Load import Load
from login_kkw import Auth_br
from main_widget import Widget
from main_widget import Widget2
from table_model import CustomTableModel
from table_model import CustomTableModel2
from PySide2 import QtWidgets, QtCore, QtUiTools
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QDialog, QHeaderView, QLineEdit, QTableView, QVBoxLayout, QMainWindow, QAction, \
    QTableWidgetItem, QTableWidget
from Login import MainLogin


from tumbtumb import thumbnail_control


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.save = None
        self.user_list_start = None
        ui_path = os.path.expanduser('/home/rapa/git/pizza/kkw/PJT_2st/Maya_Api.ui')
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)

        self.widget = Widget(self.read_data())
        self.ui.Main_QGrid.addWidget(self.widget, 1, 0)

        self.widget2 = Widget2(self.read_data2())
        self.ui.verticalLayout.addWidget(self.widget2, 0)

        ui_file.close()

        # Login
        self.Login = MainLogin()
        self.login = Auth_br()
        value = self.login.load_setting()
        if value and value['auto_login'] and value['valid_host'] and value['valid_user']:
            self.ui.show()
        else:
            self.Login.ui.show()

        # ----------------------------------------------------------------------------------------------

        # Event
        '''
        # Save 클릭시 Save ui로 전환
        '''
        self.ui.Save_Button.clicked.connect(self.Save_Button)
        self.Save = Save()

        '''
        # Load 클릭시 Load ui로 전환
        '''
        self.ui.Load_Button.clicked.connect(self.Load_Button)
        self.Load = Load()

        self.Login.ui.Login_Button.clicked.connect(self.login_button_clicked)

        self.ui.LogOut_Button.clicked.connect(self.LogOut_Button)

        self.widget.clicked.connect(self.widget_clicked)

        self.widget2.clicked.connect(self.widget_clicked2)

    # ----------------------------------------------------------------------------------------------
    def Save_Button(self):
        self.ui.hide()  # 메인 윈도우 숨김
        self.Save.ui.show()

    def Load_Button(self):
        self.ui.hide()  # 메인 윈도우 숨김
        self.Load.ui.show()

    # ----------------------------------------------------------------------------------------------

    def login_button_clicked(self):
        Host_Box = self.Login.ui.Host_Box
        ID_Box = self.Login.ui.ID_Box
        PW_Box = self.Login.ui.PW_Box

        self.login.host = Host_Box.text()
        self.login.user_id = ID_Box.text()
        self.login.user_pw = PW_Box.text()
        self.login.auto_login = self.Login.ui.Auto_Login_Check.isChecked()

        if self.login.connect_host() and self.login.log_in():
            self.Login.ui.hide()
            self.ui.show()

    def LogOut_Button(self):
        self.login.log_out()
        self.ui.hide()
        self.Login.ui.show()

    # ----------------------------------------------------------------------------------------------

    def widget_clicked(self, event):
        selected_data = self.read_data()[event.row()]
        print(selected_data)

    def widget_clicked2(self, event):
        selected_data = self.read_data2()[event.row()]
        print(selected_data)

    # ----------------------------------------------------------------------------------------------

    @staticmethod
    def read_data():
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

    # ----------------------------------------------------------------------------------------------
    @staticmethod
    def read_data2():
        project = gazu.project.get_project_by_name('jeongtae')
        asset = gazu.asset.get_asset_by_name(project, 'chair')
        task_type = gazu.task.get_task_type_by_name('Layout_asset')
        task_ = gazu.task.get_task_by_entity(asset, task_type)
        png = thumbnail_control([task_])
        # print(png)
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


# ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
