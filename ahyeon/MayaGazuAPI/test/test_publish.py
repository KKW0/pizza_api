#coding:utf8
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
        # gazu.files.new_output_type('Previz_mov', 'mov')
        self.output_type = gazu.files.get_output_type_by_name('Previz_jpg')
        working_file = gazu.files.get_working_files_for_task(self.task)
        self.working_file = working_file[0]
        # gazu.files.new_entity_output_file(self.shot, self.output_type, self.task_type,
        #                                   self.comment, self.working_file)
        output_file = gazu.files.get_last_output_files_for_entity(self.shot, self.output_type, self.task_type)
        self.output_file = output_file[0]
        self.path = '/home/rapa/foldertree_test/a/b/c/d/e/f/g/working/working_file'
        self.path2 = '/home/rapa/foldertree_test/a/b/c/d/e/f/g/output/output_file'

    def test__select_software(self):
        # test = self.pub._select_software(2)
        # pp.pprint(test)
        # self.assertEqual(type(test), dict)
        pass

    def test__select_output_type(self):
        # test = self.pub._select_output_type(self.shot, 2)
        # pp.pprint(test)
        # self.assertEqual(type(test), dict)
        pass

    def test_publish_file_data(self):
        # pp.pprint(self.task_types)
        # pp.pprint(self.task)
        # pp.pprint(self.task['task_type_id'])
        # pp.pprint(self.pub.publish_file_data(self.shot, self.task, self.comment))
        pass

    def test__make_folder_tree(self):
        # path = os.path.dirname(self.path)
        # self.pub._make_folder_tree(path)
        pass

    def test__upload_files(self):
        # self.pub._software = self.software
        # self.pub._upload_files(self.task, self.path, self.comment, self.working_file)
        # gazu.files.download_working_file(self.working_file, self.path+'2'+'.ma')
        # self.pub._upload_files(self.task, self.path2, self.output_file, self.comment_dict)
        # preview = gazu.files.get_all_preview_files_for_task(self.task)
        # gazu.files.download_preview_file(preview[0], self.path2+'_preview2'+'.mov')
        full_path = self.path2 + '_preview.mov'
        gazu.task.add_preview(self.task, self.comment_dict, full_path)
        pass

    def test_save_publish_real_data(self):
        # self.pub.save_publish_real_data(self.shot, self.task, self.comment)
        pass
