#coding:utf8
import gazu
import pprint as pp
from unittest import TestCase


class TestFilter(TestCase):
    def test_setUp(self):
        gazu.client.set_host("http://192.168.3.116/api")
        gazu.log_in("pipeline@rapa.org", "netflixacademy")

        # 테스트용 클래스변수 정의
        self.project = gazu.project.get_project_by_name('Project1')
        self.asset = gazu.asset.get_asset_by_name(self.project, 'room1')
        self.user = gazu.person.get_person_by_full_name('ahyeon jo')
        self.task_status = gazu.task.get_task_status_by_name('Todo')
        self.task_type = gazu.task.get_task_type_by_name('LayoutPizza')
        self.task = gazu.task.get_task_by_entity(self.asset, self.task_type)
        self.comment = 'Unit Test'
        # gazu.task.add_comment(self.task, self.task_status, self.comment)
        self.comment_dict = gazu.task.get_last_comment_for_task(self.task)
        self.software = gazu.files.all_softwares()[1]  # 마야
        self.sa1 = gazu.asset.get_asset_by_name(self.project, 'dog')
        self.sa2 = gazu.asset.get_asset_by_name(self.project, 'chair')
        self.sa3 = gazu.asset.get_asset_by_name(self.project, 'computer')
        self.sa4 = gazu.asset.get_asset_by_name(self.project, 'paper')
        self.sa5 = gazu.asset.get_asset_by_name(self.project, 'human')
        self.sa6 = gazu.asset.get_asset_by_name(self.project, 'assetcasttest')
        self.seq1 = gazu.shot.get_sequence_by_name(self.project, 'seq1')
        self.seq2 = gazu.shot.get_sequence_by_name(self.project, 'seq2')
        self.shot1 = gazu.shot.get_shot_by_name(self.seq1, 'sh1')
        self.shot2 = gazu.shot.get_shot_by_name(self.seq1, 'sh2')
        # mb = gazu.files.new_output_type('MayaBinary', 'mb')
        # ma = gazu.files.new_output_type('MayaAskii', 'ma')
        # gazu.files.new_output_type('UndistortionJpg', 'jpg')
        # gazu.files.new_output_type('PreviewMov', 'mov')
        # JPG, OBJ, FBX, Alembic, MPEG-4 이미 있음
        pp.pprint(gazu.files.all_output_types())
        # w = gazu.files.new_working_file(self.task, software=self.software, comment=self.comment)
        # gazu.files.new_entity_output_file(self.asset, mb, self.task_type, self.comment, w, representation='mb')
        self.output_type_mb = gazu.files.get_output_type_by_name('MayaBinary')
        self.output_type_ma = gazu.files.get_output_type_by_name('MayaAskii')
        self.output_type_ujpg = gazu.files.get_output_type_by_name('UndistortionJpg')
        self.output_type_pmov = gazu.files.get_output_type_by_name('PreviewMov')
        working_file = gazu.files.get_working_files_for_task(self.task)
        self.working_file = working_file[0]
        output_file = gazu.files.get_last_output_files_for_entity(self.asset, self.output_type_mb, self.task_type)
        self.output_file = output_file[0]
        # self.path = '/home/rapa/foldertree_test/a/b/c/d/e/f/g/working/working_file'
        # self.path2 = '/home/rapa/foldertree_test/a/b/c/d/e/f/g/output/output_file'

    # def test__get_information_dict(self):
    #     pass
    #
    # def test__collect_info_task(self):
    #     self.fail()
    #
    # def test__list_append(self):
    #     self.fail()
    #
    # def test__collect_info_casting(self):
    #     self.fail()
    #
    # def test__filter_info(self):
    #     self.fail()
    #
    # def test_select_task(self):
    #     self.fail()
