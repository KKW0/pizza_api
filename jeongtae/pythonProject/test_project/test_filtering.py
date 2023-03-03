from unittest import TestCase
from logging_ import PizzaLogger
from filtering import Filter

class TestFilter(TestCase):
    def setUp(self):
        print('hi')
        self.log = PizzaLogger('~/rapa')
        self.fc = Filter()
        self.log.connect_host('http://192.168.3.116/api')
        self.log.log_in('pipeline@rapa.org', 'netflixacademy')

    # def test_select_task(self):
    #     self.assertEqual(type(self.fc.proj_set), 'list')
    #
    # def test_filter_check(self):
    #     self.fail()
    #
    # def test_filter_project(self):
    #     self.fail()
    #
    # def test_filter_seq(self):
    #     self.fail()
