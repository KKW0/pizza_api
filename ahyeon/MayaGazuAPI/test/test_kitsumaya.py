#coding:utf8
from unittest import TestCase


class TestSetThings(TestCase):
    def test_run_program(self):
        self.fail()


"""
import gazu
import pprint as pp
from unittest import TestCase
from publish import PublishThings


class TestPublishThings(TestCase):
    def setUp(self):
        gazu.client.set_host("http://192.168.3.116/api")
        gazu.log_in("pipeline@rapa.org", "netflixacademy")
        self.pub = PublishThings()

        # 테스트용 클래스변수 정의
        self.project = gazu.project.get_project_by_name('jeongtae')
        self.seq = gazu.shot.get_sequence_by_name(self.project, 'seq1')
        self.shot = gazu.shot.get_shot_by_name(self.seq, 'shot02')
        task_type = gazu.task.all_task_types_for_shot(self.shot)
        self.task_type = task_type[0]  # 레이아웃, 1은 매치무브
        self.user = []
        self.user.append(gazu.client.get_current_user())
        self.task_status = gazu.task.get_task_status_by_name('Todo')
        # gazu.task.new_task(self.shot, self.task_type, task_status=self.task_status, assignees=self.user)
        self.task = gazu.task.get_task_by_entity(self.shot, self.task_type)
        self.comment = 'Unit Test'
        # gazu.task.add_comment(self.task, self.task_status, self.comment)
        self.comment_dict = gazu.task.get_last_comment_for_task(self.task)
        software = gazu.files.all_softwares()
        self.software = software[2]    # 마야
        # gazu.files.new_working_file(self.task, software=self.software, comment=self.comment)
        gazu.files.new_output_type('Layout_mb', 'mb')
        self.output_type = gazu.files.get_output_type_by_name('Layout_mb')
        working_file = gazu.files.get_working_files_for_task(self.task)
        self.working_file = working_file[0]
        # gazu.files.new_entity_output_file(self.shot, self.output_type, self.task_type,
        #                                   self.comment, self.working_file)
        output_file = gazu.files.get_last_output_files_for_entity(self.shot, self.output_type, self.task_type)
        self.output_file = output_file[0]
        self.path = '/home/rapa/foldertree_test/a/b/c/d/e/f/g/working/working_file'
        self.path2 = '/home/rapa/foldertree_test/a/b/c/d/e/f/g/output/output_file'
"""