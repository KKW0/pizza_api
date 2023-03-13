#coding:utf8
import gazu
import pprint as pp
from unittest import TestCase


class TestFilter(TestCase):
    def test_setUp(self):
        gazu.client.set_host("http://192.168.3.116/api")
        gazu.log_in("pipeline@rapa.org", "netflixacademy")

        # 테스트용 클래스변수 정의
        self.project = gazu.project.get_project_by_name('jeongtae')
        self.asset = gazu.asset.get_asset_by_name(self.project, 'chair')
        self.seq = gazu.shot.get_sequence_by_name(self.project, 'seq1')
        self.shot = gazu.shot.get_shot_by_name(self.seq, 'shot02')
        task_type = gazu.task.all_task_types_for_shot(self.shot)
        # self.task_type = task_type[0]  # 레이아웃, 1은 매치무브
        self.user = gazu.person.get_person_by_full_name('ahyeon jo')
        # self.user.append(gazu.client.get_current_user())
        self.task_status = gazu.task.get_task_status_by_name('Todo')
        # gazu.task.new_task_type('Layout_asset')           ####task type 이름 바꿔야 함
        self.task_type = gazu.task.get_task_type_by_name('Layout_asset')            ####task type 이름 바꿔야 함
        # gazu.task.new_task(self.asset, self.task_type, task_status=self.task_status)
        self.task = gazu.task.get_task_by_entity(self.asset, self.task_type)
        self.assignee = gazu.task.assign_task(self.task['id'], self.user['id'])
        self.comment = 'Unit Test'
        # gazu.task.add_comment(self.task, self.task_status, self.comment)
        self.comment_dict = gazu.task.get_last_comment_for_task(self.task)
        software = gazu.files.all_softwares()
        self.software = software[2]  # 마야
        # gazu.files.new_working_file(self.task, software=self.software, comment=self.comment)
        # gazu.files.new_output_type('Layout_mb', 'mb')         ####output type 이름 바꿔야 함
        self.output_type = gazu.files.get_output_type_by_name('Layout_mb')          ####output type 이름 바꿔야 함
        working_file = gazu.files.get_working_files_for_task(self.task)
        self.working_file = working_file[0]
        # gazu.files.new_entity_output_file(self.asset, self.output_type, self.task_type,
        #                                   self.comment, self.working_file)
        output_file = gazu.files.get_last_output_files_for_entity(self.asset, self.output_type, self.task_type)
        self.output_file = output_file[0]
        self.path = '/home/rapa/foldertree_test/a/b/c/d/e/f/g/working/working_file'
        self.path2 = '/home/rapa/foldertree_test/a/b/c/d/e/f/g/output/output_file'
        new_asset = gazu.asset.get_asset_by_name(self.project, 'thomas')
        new = {"asset_id": new_asset['id'], "nb_occurences": 55}
        new1 = {"asset_id": self.asset['id'], "nb_occurences": 55}
        new2 = {"shot_id": self.shot['id'], "nb_occurences": None}
        # gazu.casting.update_sequence_casting(self.project, self.seq, new)
        # gazu.casting.update_asset_casting(self.project, self.asset, new)
        # gazu.casting.update_asset_casting(self.project, self.asset, new2)

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
