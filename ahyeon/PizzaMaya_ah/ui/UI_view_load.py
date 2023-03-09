# coding=utf-8

import os
import sys
from PySide2 import QtWidgets, QtCore, QtUiTools


class Load(QtWidgets.QMainWindow):
    def __init__(self):
        super(Load, self).__init__()

        self.save = None
        self.user_list_start = None
        ui_path = os.path.expanduser('/home/rapa/git/pizza/kkw/PJT_2st/Load.ui')
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.ui.Final_Load_Button.clicked.connect(self.final_load_button)
        self.ui.Back_Button.clicked.connect(self.back_button)

    def final_load_button(self):
        self.hide()  # 메인 윈도우 숨김
        print("불러왔어 그만눌러")
        self.ui.close()

    def back_button(self):
        self.hide()  # 메인 윈도우 숨김
        self.ui.close()

# ----------------------------------------------------------------------------------------------


def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    try:
        app = QtWidgets.QApplication().instance()
    except TypeError:
        app = QtWidgets.QApplication()
    myapp = Load()
    myapp.ui.show()
    sys.exit(app.exec_())


# ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
