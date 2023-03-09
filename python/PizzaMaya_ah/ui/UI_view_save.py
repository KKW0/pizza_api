# coding=utf-8

import os
import sys
from PySide2 import QtWidgets, QtCore, QtUiTools


class Save(QtWidgets.QMainWindow):
    def __init__(self):
        super(Save, self).__init__()

        self.save = None
        self.user_list_start = None

        # 현재 작업 디렉토리 경로를 가져옴
        cwd = os.path.dirname(os.path.abspath(__file__))
        # ui 파일 경로 생성
        ui_path = os.path.join(cwd, 'UI_design', 'Save.ui')
        # ui 파일이 존재하는지 확인
        if not os.path.exists(ui_path):
            raise Exception("UI file not found at: {0}".format(ui_path))

        self.ui_file = QtCore.QFile(ui_path)
        self.ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(self.ui_file)
        self.ui_file.close()

        self.ui.Final_Save_Button.clicked.connect(self.final_save_button)
        self.ui.Back_Button.clicked.connect(self.back_button)

    def final_save_button(self):
        self.hide()  # 메인 윈도우 숨김
        print("저장했어 그만눌러")

    def back_button(self):
        self.hide()  # 메인 윈도우 숨김
        self.ui.close()

# ----------------------------------------------------------------------------------------------


def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    try:
        app = QtWidgets.QApplication().instance()
    except TypeError:
        app = QtWidgets.QApplication().instance()
    myapp = Save()
    myapp.ui.show()
    sys.exit(app.exec_())


# ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
