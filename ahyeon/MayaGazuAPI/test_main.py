#coding:utf8
import os
# from pathlib import Path
import gazu
import pprint as pp
import maya.cmds as mc
from unittest import TestCase
from main import SaveAsKitsuPath
# from maya_test import MayaLayout


class TestSaveAsKitsuPath(TestCase):
    def setUp(self):
        self.origin = SaveAsKitsuPath()
        self.origin.project = "A_project"

    def test_select_task(self, num=0):
        print(self.origin.project)
        task_list_proj = gazu.task.all_tasks_for_project(self.origin.project)
        task_list_user = gazu.user.all_tasks_to_do()
        task_list = []
        for task in task_list_user:
            if task in task_list_proj:
                task_list.append(task)
        pp.pprint(task_list)
        self._task = task_list[num]

        pp.pprint(self._task)
        self.assertEqual(type(self._task), dict)

    # def test_get_casting(self, num=0):
    #     self._casting_dict = gazu.casting.get_shot_casting(self._shot['id'])
    #     self._casting = self._casting_dict[num]
    #
    #     print('\n#### casting ####')
    #     pp.pprint(self._casting)
    #     self.assertEqual(type(self._casting), dict)
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
    #     software_list = gazu.files.all_softwares()
    #     self._software = software_list[num]
    #
    #     print('\n#### software ####')
    #     pp.pprint(self._software)
    #     self.assertEqual(type(self._software), list)
    #
    # def test_select_output_type(self, num=0):
    #     output_type_list = gazu.files.all_output_types_for_entity(self._shot['id'])
    #     self._output_type = output_type_list[num]
    #
    #     print('\n#### output_type_list ####')
    #     pp.pprint(output_type_list)
    #     self.assertEqual(type(output_type_list), list)
    #     self.assertEqual(type(self._output_type), dict)
    #
    # def test_make_folder_tree(self, path):
    #     dir_path_list = path.split('/')[:-1]
    #     dir_path = '/'.join(dir_path_list)
    #     Path(dir_path).mkdir(parents=True, exist_ok=True)
    #
    # def test_get_kitsu_path(self, num=0):
    #     working_file_list = gazu.files.get_working_files_for_task(self._task['id'])
    #     if working_file_list is []:
    #         self.test_select_software(0)
    #         self._working_path = gazu.files.build_working_file_path(self._task['id'],
    #                                                                 software=self._software)
    #         self.test_make_folder_tree(self._working_path)
    #     else:
    #         # 테스크에 워킹 파일이 이미 존재할 경우, 기존 파일의 정보를 계승
    #         working_file = working_file_list[num]
    #         self._software = gazu.files.get_software(working_file['software'])
    #         print('\n#### working_file ####')
    #         pp.pprint(working_file)
    #         self._working_path = gazu.files.build_working_file_path(self._task['id'],
    #                                                                 software=self._software,
    #                                                                 revision=working_file['revision']+1)
    #
    #         print('\n#### software ####')
    #         pp.pprint(self._software)
    #
    #     output_file_list = gazu.files.get_last_output_files_for_entity(self._shot['id'],
    #                                                                    task_type=self._task['task_type'])
    #     if output_file_list is []:
    #         self.test_select_output_type(0)
    #         self._output_path = gazu.files.build_entity_output_file_path(self._shot['id'],
    #                                                                      self._output_type,
    #                                                                      self._task['task_type'])
    #         self.test_make_folder_tree(self._output_path)
    #     else:
    #         output_file = output_file_list[num]
    #         self._output_path = gazu.files.build_entity_output_file_path(self._shot['id'],
    #                                                                      self._output_type,
    #                                                                      self._task['task_type'],
    #                                                                      representation=output_file['representation'],
    #                                                                      revision=output_file['revision']+1,
    #                                                                      nb_elements=output_file['nb_elements'])
    #
    # # ################### Maya ###################
    # # def test_load_data(self, data_type):
    # #     path = ""
    # #     file_type = ""
    # #     if data_type is 'output':
    # #         file_type = self._output_type['file extension']
    # #         path = self._output_path + '.' + file_type
    # #     elif data_type is 'working':
    # #         file_type = self._software['file extension']
    # #         path = self._working_path + '.' + file_type
    # #
    # #     files = mc.getFileList(folder=path, filespec=('.'+file_type))
    # #
    # #     if len(files) is 0:
    # #         raise ValueError("File not found")
    # #     else:
    # #         for item in files:
    # #             mc.file(path, i=1, ignoreVersion=1, options="mo=0", mergeNamespacesOnClash=0,
    # #                     importTimeRange="combine", loadReferenceDepth="all", gr=True, gn="imported_GRP")
    # #
    # #     imported_file = mc.ls("hulk:*", type="transform")
    # #     for item in imported_file:
    # #         mc.xform(item, t=(0, 0, 0), ro=(-90, 0, 0), ws=1)
    # # #
    # # # def test_save_working_file(self):
    # # #     self.fail()
    # # #
    # # def test_export_output_file(self):
    # #     cam_list = self.connect_image()
    # #     output_path = '플레이블라스트 저장할 파일경로'
    # #     mc.lookThru(cam_list[0])
    # #     mc.playblast(
    # #         format='image',
    # #         filename='%s' % output_path,
    # #         sequenceTime=0,
    # #         clearCache=1, viewer=1,
    # #         showOrnaments=1,
    # #         fp=4, percent=50,
    # #         compression="jpg",
    # #         quality=100
    #
    # ################### Maya ###################
    #
    # def test_publish_file_data(self, comment, nb_elements):
    #     working_file = gazu.files.new_working_file(self._task['id'], software=self._software,
    #                                                comment=comment)
    #     output_file = gazu.files.new_entity_output_file(self._shot, self._output_type,
    #                                                     self._task['task_type'],
    #                                                     comment=comment,
    #                                                     working_file=working_file,
    #                                                     nb_elements=nb_elements, representation='')
    #
