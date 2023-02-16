#coding:utf8
import gazu
import pprint as pp
from unittest import TestCase
from publish import PublishThings
from kitsumaya import SetThings

class TestSetThings(TestCase):
    def setUp(self):
        gazu.client.set_host("http://192.168.3.116/api")
        gazu.log_in("pipeline@rapa.org", "netflixacademy")
        self.sett = SetThings()
        self.pub = PublishThings()

        self.sett.project = 'jeongtae'
        self.comment = 'Unit Test'

    def test_update_filetree(self):
        pass

    def test_select_task(self):
        # self.sett.select_task()
        # pp.pprint(self.sett._task)
        # pp.pprint(self.sett._shot)
        pass

    def test__get_kitsu_path(self):
        # asset = gazu.asset.get_asset_by_name(self.sett.project, 'Gromit')
        # print(self.sett._get_kitsu_path(asset))
        pass

    def test_run_program(self):
        # self.sett.run_program(self.comment)
        pass
