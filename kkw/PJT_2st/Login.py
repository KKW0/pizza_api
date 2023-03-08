# coding=utf-8

import os
import sys

from login_kkw import Auth_br
from PySide2 import QtWidgets, QtCore, QtUiTools


class MainLogin(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainLogin, self).__init__()

        self.Login = None
        self.user_list_start = None
        ui_path = os.path.expanduser('/home/rapa/git/pizza/kkw/PJT_2st/Login.ui')
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)

        ui_file.close()

        self.login = Auth_br()
    # ----------------------------------------------------------------------------------------------

        self.Host_Box = self.ui.findChild(QtWidgets.QLineEdit, "Host_Box")

        self.ID_Box = self.ui.findChild(QtWidgets.QLineEdit, "ID_Box")
        self.PW_Box = self.ui.findChild(QtWidgets.QLineEdit, "PW_Box")

    # ----------------------------------------------------------------------------------------------

def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    try:
        app = QtWidgets.QApplication().instance()
    except TypeError:
        app = QtWidgets.QApplication(sys.argv)
    myapp = MainLogin()
    myapp.ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
