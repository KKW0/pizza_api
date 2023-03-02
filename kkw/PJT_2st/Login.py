
import os
import sys
from PySide2 import QtWidgets, QtCore, QtUiTools

from Maya_Api import MainWindow

class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # 2.7 버전 슈퍼 사용방법 super(Login, self).__init__()
        self.main_window = MainWindow()
        self.Login = None
        self.user_list_start = None
        ui_path = os.path.expanduser('/home/rapa/git/pizza/kkw/PJT_2st/Login.ui')
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.ui.Login_Button.clicked.connect(self.login_button_clicked)

# ----------------------------------------------------------------------------------------------

    def login_button_clicked(self):
        self.ui.hide()
        self.main_window.ui.show()

# ----------------------------------------------------------------------------------------------
def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    try:
        app = QtWidgets.QApplication().instance()
    except TypeError:
        app = QtWidgets.QApplication(sys.argv)
    myapp = Login()
    myapp.ui.show()
    sys.exit(app.exec_())


# ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
