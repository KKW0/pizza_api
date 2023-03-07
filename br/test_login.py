#coding:utf8
import os
import json
from unittest import TestCase
from login import PizzaLogin


class Testlogin(TestCase):
    def setUp(self):
        self.valid_url = 'http://192.168.3.116/api'
        self.valid_id = 'pipeline@rapa.org'
        self.valid_pw = 'netflixacademy'
        self.invalid_url = 'http://192.168.3.116'
        self.invalid_id = 'pipeline@rapa.or'
        self.invalid_pw = 'netflixacadem'
        self.login = PizzaLogin()

    def test_valid_host(self):
        self.assertEqual(self.login.valid_host, self.login._valid_host)

    def test_valid_user(self):
        self.assertEqual(self.login.valid_user, self.login._valid_user)

    def test_host(self):
        self.assertEqual(self.login.host, self.login._host)

    def test_user(self):
        self.assertEqual(self.login.user, self.login._user)

    def test_connect_host(self):
        with self.assertRaises(ValueError):
            self.login.connect_host(self.invalid_url)
        self.assertFalse(self.login._valid_host)

        self.assertTrue(self.login.connect_host(self.valid_url))
        self.assertTrue(self.login._valid_host)

    def test_log_in(self):
        # self.assertFalse(self.login.connect_host(self.invalid_url))
        self.assertTrue(self.login.connect_host(self.valid_url))
        with self.assertRaises(ValueError):
            self.login.log_in(self.invalid_id, self.invalid_pw)
        self.assertFalse(self.login.valid_user)

        self.assertTrue(self.login.log_in(self.valid_id, self.valid_pw))
        self.assertTrue(self.login._valid_user)
        
    def test_log_out(self):
        self.login.connect_host(self.valid_url)
        self.login.log_in(self.valid_id, self.valid_pw)
        self.login.log_out()
        self.assertIsNone(self.login._user)

    def test_access_setting(self):
        self.login.access_setting()
        self.assertTrue(os.path.exists(self.login.dir_path))
        self.assertFalse(os.path.exists(self.login.user_path))

    def test_load_setting(self):
        invalid_dict = {
            'host': self.invalid_url,
            'user_id': self.invalid_id,
            'user_pw': self.invalid_pw,
            'valid_host': False,
            'valid_user': False,
        }
        with open(self.login.user_path, 'w') as json_file:
            json.dump(invalid_dict, json_file)

        self.login.load_setting()
        self.assertFalse(self.login.valid_host)
        self.assertFalse(self.login.valid_user)

        valid_dict = {
            'host': self.valid_url,
            'user_id': self.valid_id,
            'user_pw': self.valid_pw,
            'valid_host': True,
            'valid_user': True,
        }
        with open(self.login.user_path, 'w') as json_file:
            json.dump(valid_dict, json_file)

        self.login.load_setting()
        self.assertTrue(self.login.valid_host)
        self.assertTrue(self.login.valid_user)

    def test_save_setting(self):
        user_dict = {
            'host': self.login.host,
            'user_id': self.login._user_id,
            'user_pw': self.login._user_pw,
            'valid_host': self.login.valid_host,
            'valid_user': self.login.valid_user,
        }

        with open(self.login.user_path, 'r') as json_file:
            user_dict = json.load(json_file)

        self.login.save_setting()

    def test_reset_setting(self):
        self.assertIsNone(self.login._host)
        self.assertIsNone(self.login._user_id)
        self.assertIsNone(self.login._user_pw)
        self.assertFalse(self.login._valid_host)
        self.assertFalse(self.login._valid_user)
