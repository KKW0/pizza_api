#coding:utf8
from unittest import TestCase
from PizzaMaya_ah.code.login import LogIn
import os


class TestLogIn(TestCase):
    def setUp(self):
        self.valid_url = 'http://192.168.3.116/api'
        self.valid_id = 'pipeline@rapa.org'
        self.valid_pw = 'netflixacademy'
        self.invalid_url = 'http://192.168.3.116'
        self.invalid_id = 'pipeline@rapa.or'
        self.invalid_pw = 'netflixacadem'
        self.login = LogIn()

    def test_valid_host(self):
        self.assertEqual(self.login.valid_host, self.login._valid_host)

    def test_valid_user(self):
        self.assertEqual(self.login.valid_user, self.login._valid_user)

    def test_host(self):
        self.assertEqual(self.login.host, self.login._host)

    def test_user(self):
        self.assertEqual(self.login.user, self.login._user)

    def test_user_id(self):
        self.assertEqual(self.login.user_id, self.login._user_id)

    def test_user_pw(self):
        self.assertEqual(self.login.user_pw, self.login._user_pw)

    def test_auto_login(self):
        self.assertEqual(self.login.auto_login, self.login._auto_login)

    def test_connect_host(self):
        with self.assertRaises(ValueError):
            self.login.host = self.invalid_url
            self.login.connect_host()
        self.assertFalse(self.login._valid_host)

        self.login.host = self.valid_url
        self.login.connect_host()
        self.assertTrue(self.login.valid_host)
        self.assertTrue(self.login.connect_host())

    def test_log_in(self):
        self.login.host = self.valid_url
        self.login.connect_host()
        self.login.user_id = self.invalid_id
        self.login.user_pw = self.invalid_pw
        with self.assertRaises(ValueError):
            self.login.log_in()
        self.assertFalse(self.login.valid_user)

        self.login.host = self.valid_url
        self.login.connect_host()
        self.login.user_id = self.valid_id
        self.login.user_pw = self.valid_pw
        self.login.log_in()
        self.assertTrue(self.login.valid_user)
        self.assertTrue(self.login.log_in())

    def test_log_out(self):
        self.login.host = self.valid_url
        self.login.connect_host()
        self.login.user_id = self.valid_id
        self.login.user_pw = self.valid_pw
        self.login.log_in()

        self.login.log_out()
        self.assertIsNone(self.login._user)
        self.assertTrue(self.login.log_out())

    def test_access_setting(self):
        self.login.access_setting()
        self.assertTrue(os.path.exists(self.login.dir_path))
        self.assertTrue(os.path.exists(self.login.user_path))

    def test_load_setting(self):
        load = self.login.load_setting()
        self.assertIsInstance(load, dict)

    def test_save_setting(self):
        save = self.login.save_setting()
        self.assertIsInstance(save, dict)

    def test_reset_setting(self):
        self.assertIsNone(self.login.host)
        self.assertIsNone(self.login.user_id)
        self.assertIsNone(self.login.user_pw)
        self.assertFalse(self.login.valid_host)
        self.assertFalse(self.login.valid_user)
        self.assertFalse(self.login.auto_login)