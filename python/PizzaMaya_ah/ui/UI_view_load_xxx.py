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
        self.my_shot_index_list = []
        self.selected_index_list = []  # 선택한 에셋들의 인덱스 번호

        self.ui.Final_Load_Button.clicked.connect(self.final_load_button)
        self.ui.Back_Button.clicked.connect(self.back_button)

        self.ma = MayaThings()

    def final_load_button(self):
        self.hide()  # 메인 윈도우 숨김    # self.close() ???
        my_layout_asset = gazu.asset.get_asset(self.my_task['entity_id'])
        self.ma.import_casting_asset(my_layout_asset, self.selected_index_list)
        for shot in self.my_shot_index_list:
            self.ma.import_cam_seq(shot)
        QtWidgets.QMessageBox.information(self, 'Completed!', '{0}개의 에셋이 로드되었습니다.'\
                                          .format(len(self.selected_index_list)))