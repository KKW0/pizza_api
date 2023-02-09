#coding:utf8
import os
import sys
from PySide2 import QtWidgets, QtCore, QtUiTools

'''
# save_windows
'''
from save_windows import App2

from load_windows import App3
'''
# load_windows
'''


class App(QtWidgets.QMainWindow, App2, App3):
    def __init__(self):
        super().__init__()
        self.save = None
        self.user_list_start = None
        ui_path = os.path.expanduser('/home/rapa/git/pizza/kangkyoungwook/PJT_test1/Pizza_MaYa.ui')
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.ui.show()

        '''
        # save 클릭시 save_windows ui로 전환
        '''
        self.ui.save_windows.clicked.connect(self.save_windows)
        self.app2 = App2()

        '''
        # load 클릭시 load_windows ui로 전환
        '''
        self.ui.load_windows.clicked.connect(self.load_windows)
        self.app3 = App3()

    # ----------------------------------------------------------------------------------------------

    def save_windows(self):
        self.hide()  # 메인 윈도우 숨김
        # ui_path = os.path.expanduser('/home/rapa/git/pizza/kangkyoungwook/PJT_test1/save_windows.ui')
        # ui_file = QtCore.QFile(ui_path)
        # ui_file.open(QtCore.QFile.ReadOnly)
        # loader = QtUiTools.QUiLoader()
        # self.ui = loader.load(ui_file)
        # ui_file.close()
        # self.ui.show()  # ui 출력
        self.app2.ui.exec()

    def load_windows(self):
        self.hide()  # 메인 윈도우 숨김
        # ui_path = os.path.expanduser('/home/rapa/git/pizza/kangkyoungwook/PJT_test1/load_windows.ui')
        # ui_file = QtCore.QFile(ui_path)
        # ui_file.open(QtCore.QFile.ReadOnly)
        # loader = QtUiTools.QUiLoader()
        # self.ui = loader.load(ui_file)
        # ui_file.close()
        # self.ui.show()  # ui 출력
        self.app3.ui.exec()


# ----------------------------------------------------------------------------------------------
def main():
    app = QtWidgets.QApplication(sys.argv)
    myapp = App()
    myapp.ui.show()
    sys.exit(app.exec_())


# ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
