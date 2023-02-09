#coding:utf8
import os
import gazu
import pprint as pp
import maya.cmds as mc
from unittest import TestCase
from main import SaveAsKitsuPath
# from maya_test import MayaLayout


class TestSaveAsKitsuPath(TestCase):
    def setUp(self):
        self.origin = SaveAsKitsuPath()
        self.origin.project = "NetflixAcademy"
        self.origin.person = "Youngbin Park"

    # def test_select_task(self, num=0):
    #     pass

    # def test_get_casting(self):
    #     pass
    #
    # def test_get_informations(self):
    #     self._shot = gazu.entity.get_entity(self._task['entity id'])
    #     self._sequence = gazu.shot.get_sequence_from_shot(self._shot['id'])
    #     self.test_get_casting(0)
    #     self._asset = gazu.asset.get_asset(self._casting['asset_id'])
    #     self._asset_type = gazu.asset.get_asset_type_from_asset(self._asset['id'])
    #
    #     print('\n#### shot ####')
    #     pp.pprint(self._shot)
    #     print('\n#### sequence ####')
    #     pp.pprint(self._sequence)
    #     print('\n#### asset ####')
    #     pp.pprint(self._asset)
    #     print('\n#### asset_type ####')
    #     pp.pprint(self._asset_type)
    #
    #     self.assertEqual(type(self._shot), dict)
    #     self.assertEqual(type(self._sequence), dict)
    #
    #     self.assertEqual(type(self._asset), dict)
    #     self.assertEqual(type(self._asset_type), dict)
    #
    # def test_select_software(self, num=0):
    #     pass
    #
    # def test_select_output_type(self, num=0):
    #     pass

    # def test_make_folder_tree(self, path):
    #     pass

    # def test_get_kitsu_path(self, casting=0):
    #     # --------------------------------------------
    #     self.origin.select_task()
    #     self.origin._asset = gazu.asset.get_asset_by_name(self.origin.project, "Hulkbuster")
    #     # --------------------------------------------
    #
    #     pass
    #
    # ################### Maya ###################
    # def test_load_data(self, data_type):
    #     path = ""
    #     file_type = ""
    #     if data_type is 'output':
    #         file_type = self._output_type['file extension']
    #         path = self._output_path + '.' + file_type
    #     elif data_type is 'working':
    #         file_type = self._software['file extension']
    #         path = self._working_path + '.' + file_type
    #
    #     files = mc.getFileList(folder=path, filespec=('.'+file_type))
    #
    #     if len(files) is 0:
    #         raise ValueError("File not found")
    #     else:
    #         for item in files:
    #             mc.file(path, i=1, ignoreVersion=1, options="mo=0", mergeNamespacesOnClash=0,
    #                     importTimeRange="combine", loadReferenceDepth="all", gr=True, gn="imported_GRP")
    #
    #     imported_file = mc.ls("hulk:*", type="transform")
    #     for item in imported_file:
    #         mc.xform(item, t=(0, 0, 0), ro=(-90, 0, 0), ws=1)
    # #
    # # def test_save_working_file(self):
    # #     self.fail()
    # #
    # def test_export_output_file(self):
    #     cam_list = self.connect_image()
    #     output_path = '플레이블라스트 저장할 파일경로'
    #     mc.lookThru(cam_list[0])
    #     mc.playblast(
    #         format='image',
    #         filename='%s' % output_path,
    #         sequenceTime=0,
    #         clearCache=1, viewer=1,
    #         showOrnaments=1,
    #         fp=4, percent=50,
    #         compression="jpg",
    #         quality=100
    #
    # ################### Maya ###################
    #
    def test_publish_file_data(self, comment):
        # 테스크에 대한 워킹 파일 새로 생성
        # person은 user 또는 선택한 person(자신)

        # working file 생성
        # 테스크 하나에 워킹 파일이 여러개일 수는 없음. 리비전만 올라감
        self.origin.select_software(0)
        working_file = gazu.files.new_working_file(self.origin._task['id'],
                                                   software=self.origin._software,
                                                   comment=comment,
                                                   person=self.origin._person)

        # output file 존재 여부 판별 후 이미 있으면 계승하고, 없으면 전부 새로 생성
        output_file_list = gazu.files.get_last_output_files_for_entity(self.origin._shot['id'],
                                                                       task_type=self.origin._task['task_type'])
        if output_file_list is []:
            # output file 없으면 아웃풋 타입 선택해서 새로 생성
            self.origin.select_output_type(0)
            output_file = gazu.files.new_entity_output_file(self.origin._shot['id'],
                                                            self.origin._output_type['id'],
                                                            self.origin._task['task_type'],
                                                            comment=comment,
                                                            working_file=working_file,
                                                            person=self.origin._person,
                                                            representation=self.origin._software['file_extension'])
        else:
            # 이미 있으면 정보 계승함
            old_output = output_file_list[0]
            output_file = gazu.files.new_entity_output_file(self.origin._shot['id'],
                                                            old_output['output_type'],
                                                            self.origin._task['task_type'],
                                                            comment=comment,
                                                            working_file=old_output['working_file'],
                                                            person=self.origin._person,
                                                            revision=old_output['revision']+1,
                                                            representation=old_output['representation'])

        #### ------------------- build -----------------------
        self._working_path = gazu.files.build_working_file_path(self.origin._task['id'],
                                                                software=self.origin._software)
        self._output_path = gazu.files.build_entity_output_file_path(self.origin._shot['id'],
                                                                     self.origin._output_type,
                                                                     self.origin._task['task_type'],
                                                                     representation=output_file['representation'],
                                                                     revision=output_file['revision'] + 1,
                                                                     nb_elements=output_file['nb_elements'])
        path = self.origin.edit_path(self._working_path)
        self.origin.make_folder_tree(path)
        # 폴더 구조 만들기



