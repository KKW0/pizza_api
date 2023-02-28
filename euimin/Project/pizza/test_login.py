from unittest import TestCase
import os
import json
from login import Pizza_login


class TestPizza_login(TestCase):
    def setUp(self):
        self.valid_url = 'http://192.168.3.116/api'
        self.valid_id = 'pipeline@rapa.org'
        self.valid_pw = 'netflixacademy'
        self.login = Pizza_login()

    def test_host(self):
        self.assertEqual(self.login.host, self.login._host)
    #
    # def test_user(self):
    #     self.fail()
    #
    # def test_check_host(self):
    #     self.fail()
    #
    # def test_check_user(self):
    #     self.fail()
    #
    # def test_setting(self):
    #     self.fail()
    #
    # def test_reset_setting(self):
    #     self.fail()
    #
    # def test_save_setting(self):
    #     self.fail()
    #
    # def test_connect_host(self):
    #     self.fail()
    #
    # def test_log_in(self):
    #     self.fail()
    #
    # def test_log_out(self):
    #     self.fail()
    #
    # def test_load_setting(self):
    #     self.fail()
