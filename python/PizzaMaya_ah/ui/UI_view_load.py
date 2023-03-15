# coding=utf-8

import os
import sys

import gazu

from PizzaMaya_ah.code.usemaya import MayaThings

from PySide2 import QtWidgets, QtCore, QtUiTools


class Load(QtWidgets.QMainWindow):
    def __init__(self):
        super(Load, self).__init__()

        self.my_task = None
        self.shot_list = None
        self.shot_num = None

        # 현재 작업 디렉토리 경로를 가져옴
        cwd = os.path.dirname(os.path.abspath(__file__))
        # ui 파일 경로 생성
        ui_path = os.path.join(cwd, 'UI_design', 'Load.ui')
        # ui 파일이 존재하는지 확인
        if not os.path.exists(ui_path):
            raise Exception("UI file not found at: {0}".format(ui_path))

        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.ui.Final_Load_Button.clicked.connect(self.final_load_button)
        self.ui.Back_Button.clicked.connect(self.back_button)

        self.ma = MayaThings()

    def final_load_button(self):
        self.hide()  # 메인 윈도우 숨김    # self.close() ???
        my_shot = self.ft.select_shot(shot_list, shot_num)
        asset_index_list = []
        try:
            self.ma.import_cam_seq(my_shot)
        except Exception as exc:
            raise ValueError("Error")
        QtWidgets.QMessageBox.information(self,
                                          "camera, undistortion img",
                                          "로드가 완료되었습니다.")

        my_layout_asset = gazu.asset.get_asset(self.my_task['entity_id'])
        try:
            self.ma.import_casting_asset(my_layout_asset, asset_index_list)
        except Exception as exc:
            raise ValueError("Error")
        QtWidgets.QMessageBox.information(self,
                                          "asset {0}개의".format(checked_num),
                                          "로드가 완료되었습니다.")

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
