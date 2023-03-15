# coding=utf-8

import os
import sys

from PizzaMaya_ah.code.filter import Filter
from PizzaMaya_ah.code.publish import PublishThings

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

        self.ft = Filter()
        self.task, self.task_info, _, _, _ = self.ft.select_task()
        data = []
        for index in range(len(self.task_info)):
            data.append([self.task_info[index]['project_name'], self.task_info[index]['sequence_name']])

        # init에서 save ui가 동작하면 고정 path값이 바로 보이게 적용
        # ()안에 경로 출력하는 메소드 추가
        # publish에 _publish_file_data의 path값 넣으면 되지 않을까? 하는 생각이랄까요?
        self.ui.Sin_File_Path_2.setText(self.task_info[index]['sequence_name'])
        self.ui.OutPut_File_Path_2.setText(self.task_info[index]['sequence_name'])

        self.pb = PublishThings()

    def final_save_button(self):
        self.hide()  # 메인 윈도우 숨김
        # print("저장했어 그만눌러")
        # 여기도 데이터값만 넣으면 알아서 적용이 되지 않을까 하는 의문이 드네요
        print(self.ui.Save_Path_View_2.toPlainText())

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
