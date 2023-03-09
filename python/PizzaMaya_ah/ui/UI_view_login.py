# coding=utf-8

import os
import sys

from PizzaMaya_ah.code.login import LogIn
from PySide2 import QtWidgets, QtCore, QtUiTools


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()

        self.user_list_start = None

        # 현재 작업 디렉토리 경로를 가져옴
        cwd = os.path.dirname(os.path.abspath(__file__))
        # ui 파일 경로 생성
        ui_path = os.path.join(cwd, 'UI_design', 'Login.ui')
        # ui 파일이 존재하는지 확인
        if not os.path.exists(ui_path):
            raise Exception("UI file not found at: {0}".format(ui_path))

        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)

        ui_file.close()

        self.login = LogIn()
    # ----------------------------------------------------------------------------------------------

        self.host_box = self.ui.findChild(QtWidgets.QLineEdit, "Host_Box")
        self.id_box = self.ui.findChild(QtWidgets.QLineEdit, "ID_Box")
        self.pw_box = self.ui.findChild(QtWidgets.QLineEdit, "PW_Box")

    # ----------------------------------------------------------------------------------------------


def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    try:
        app = QtWidgets.QApplication().instance()
    except TypeError:
        app = QtWidgets.QApplication(sys.argv)
    myapp = LoginWindow()
    myapp.ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()