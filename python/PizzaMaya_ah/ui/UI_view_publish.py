# coding=utf-8

import os
import sys
import gazu
import maya.cmds as mc

from PizzaMaya_ah.code.filter import Filter
from PizzaMaya_ah.code.publish import PublishThings

from PySide2 import QtWidgets, QtCore, QtUiTools


class Save(QtWidgets.QMainWindow):
    def __init__(self):
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

        self.ui.Final_Save_Button.clicked.connect(self.final_save_button)
        self.ui.Back_Button.clicked.connect(self.back_button)

        self.ft = Filter()
        self.pub = PublishThings()

    def final_save_button(self):
        self.hide()  # 메인 윈도우 숨김
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
