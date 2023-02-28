#coding:utf8
from unittest import TestCase
from login_br import Auth_br


class Testlogin_br(TestCase):
    def setUp(self):
        self.valid_url = 'http://192.168.3.116/api'
        self.valid_id = 'pipeline@rapa.org'
        self.valid_pw = 'netflixacademy'
        self.invalid_url = 'http://192.168.3.116'
        self.invalid_id = 'pipeline@rapa.or'
        self.invalid_pw = 'netflixacadem'
        self.login = Auth_br()

    # def test_valid_host(self):
    #     self.assertEqual(self.login.valid_host, self.login._valid_host)

    # def test_valid_user(self):
    #     self.fail()
    #
    # def test_host(self):
    #       self.fail()
    #
    # def test_user(self):
    #     self.fail()
    #
    def test_connect_host(self):
        self.assertEqual(self.valid_url, self.login._valid_host)
    #
    # def test_log_in(self):
    #     self.fail()
    #
    # def test_log_out(self):
    #     self.fail()
    #
    # def test_access_setting(self):
    #     self.fail()
    #
    # def test_load_setting(self):
    #     self.fail()
    #
    # def test_save_setting(self):
    #     self.fail()
    #
    # def test_reset_setting(self):
    #     self.fail()
