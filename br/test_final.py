from unittest import TestCase
from working_file2 import MyGazu

class TestMyGazu(TestCase):
    def setUp(self) -> None:
        self.gz = MyGazu()

    def test_set_project(self):
        self.gz.set_project("Test_bbr")
        self.assertEqual(self.gz.project['name'], "Test_bbr")

    def test_set_shot(self):
        self.gz.set_shot('shot_01')
        self.assertEqual(self.gz.set_shot, 'shot_01')

    def test_set_seq(self):
        self.gz.set_seq('seq_01')
        self.assertEqual(self.gz.set_seq, 'seq_01')

    def test_set_asset(self):
        self.gz.set_asset('Cow')
        self.assertEqual(self.gz.set_asset, 'Cow')

    # def test_set_task_asset(self):
    #     self.gz.set_task_asset('Cow')
    #     self.assertEqual(self.gz.set_task_asset, 'Cow')

    def test_set_task_shot(self):
        self.gz.set_task_shot('Layout')
        self.assertEqual(self.gz.set_task_shot, 'Layout')

    def test_set_preview(self):
        self.gz.set_preview('New preview file', preview_file)

    def test_new_task(self):
        self.gz.new_task("modeling")

    def test_assign_task(self):
        self.gz.assign_task()

    def test_update_file_tree(self):
        self.gz.update_file_tree()

    def test_create_tree_dir(self):
        self.gz.create_tree_dir()

    def test_update_working(self):
        self.fail()

    def test_update_output(self):
        self.fail()

    def test_working_publish_for_asset(self):
        self.gz.working_publish_for_asset('Cow', 'modeling')

    def test_working_path_for_asset(self):
         self.gz.working_path_for_asset('Cow', 'modeling')

    def test_get_working_publish_for_shot(self):
        self.gz.get_working_publish_for_shot('seq_01', 'shot_01', 'layout')

    def test_get_output_publish_for_shot(self):
        self.gz.get_output_publish_for_shot('seq_01', 'shot_01', 'OBJ', 'layout')

    def test_get_working_path_for_shot(self):
        self.gz.get_working_path_for_shot('seq_01', 'shot_01', 'layout')

    def test_get_frame_padding(self):
        self.fail()

    def test_get_output_path_for_shot(self):
        self.gz.get_output_path_for_shot('seq_01', 'shot_01', 'OBJ', 'layout')

    def test_casting_create(self):
        self.gz.casting_create('Cow', 'seq_01', 'shot_01')
        self.gz.casting_create('Mouse', 'seq_01', 'shot_01')
        self.gz.casting_create('Desk', 'seq_01', 'shot_01')

    def test_get_path_for_casting(self):
        self.test_get_path_for_casting("rocket")
