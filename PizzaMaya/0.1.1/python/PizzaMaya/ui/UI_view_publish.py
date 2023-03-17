# coding=utf-8

import os
import sys
import gazu
import maya.cmds as mc

from PizzaMaya.code.filter import Filter
from PizzaMaya.code.publish import PublishThings

from PySide2 import QtWidgets, QtCore, QtUiTools, QtGui


class Save(QtWidgets.QMainWindow):
    """
    이 클래스는 작업한 내용을 퍼블리시 하기 위한 기능을 실행시키는 UI를 생성하는 뷰이다.
    """
    def __init__(self):
        """
        UI파일을 불러오고 mainWindow를 상속받으며, 현재 UI를 화면 중앙에 띄운다.
        사용할 기능에 대한 instance를 만들고 버튼을 연결해준다.
        """
        super(Save, self).__init__()
        self.my_task = None

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
        self.ui.setGeometry(
            QtWidgets.QStyle.alignedRect(
                QtCore.Qt.LeftToRight,
                QtCore.Qt.AlignCenter,
                self.ui.size(),
                QtGui.QGuiApplication.primaryScreen().availableGeometry(),
            ),
        )

        self.ui.Final_Save_Button.clicked.connect(self.final_save_button)
        self.ui.Back_Button.clicked.connect(self.back_button)

        self.ft = Filter()
        self.pub = PublishThings()

    def final_save_button(self):
        """
        최종 퍼블리시 승인 버튼이다.
        이  버튼을 클릭하면 현재 작업하는 씬에 존재하는 카메라의 목록을 불러와 리스트에 추가하고 그 리스트에서 디폴트
        카메라를 제외한 유저가 작업한 샷의 카메라만 남겨서 pub.save_publish_previews()에 넘겨준다.
        text박스 안에 작성한 문장은 퍼블리시하는 파일들의 comment로 작성된다.
        또한 카메라의 이름으로부터 시퀀스의 정보들을 얻어낸다.
        pub.save_publish_real_data 이 함수를 통해 작업한 파일들을 실제로 폴더안에 저장한다.
        이때 사용하는 my task 변수는 UI컨트롤러에서 정보를 받아온다.
        """
        comment = self.ui.Save_Path_View_2.toPlainText()
        shot_dict_list = []
        startup_cameras = []
        all_cameras = mc.ls(type='camera', l=True)
        for camera in all_cameras:
            if mc.camera(mc.listRelatives(camera, parent=True)[0], startupCamera=True, q=True):
                startup_cameras.append(camera)
        custom_camera = list(set(all_cameras) - set(startup_cameras))

        if custom_camera:
            for cam_name in custom_camera:
                cam_name_parts1 = cam_name.split("|")
                cam_name_parts2 = cam_name_parts1[1].split("_")
                proj_name = (cam_name_parts2[0]).title()
                proj = gazu.project.get_project_by_name(proj_name)
                seq_name = cam_name_parts2[1] + '_' + cam_name_parts2[2]      #### seq_1 형태라..
                seq = gazu.shot.get_sequence_by_name(proj, seq_name)
                shot = gazu.shot.get_shot_by_name(seq, cam_name_parts2[-1])
                shot_dict_list.append(shot)
                
        self.pub.save_publish_real_data(self.my_task, comment)
        self.pub.save_publish_previews(shot_dict_list, custom_camera, comment)
        self.hide()  # 메인 윈도우 숨김
        self.ui.close()

    def back_button(self):
        """
        퍼블리시를 취소하고 뒤로 돌아간다.
        """
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
