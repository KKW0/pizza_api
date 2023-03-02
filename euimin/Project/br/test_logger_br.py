#coding:utf8
import os
from unittest import TestCase
from logger_br import Pizza_logger
from login_br import Auth_br


class TestPizza_logger(TestCase):
    def setUp(self):
        self.logger = Pizza_logger()
        self.user_path = './test_logs'
        self.login = Auth_br()
        self.login.connect_host('http://192.168.3.116/api')
        self.login.log_in('pipeline@rapa.org', 'netflixacademy')

    # def tearDown(self):
        # self.assertTrue(self.login.log_out())

    def test_set_logger(self):
        self.logger.set_logger()
        # self.assertIsNotNone(self.logger.log.handlers)
        # print(self.logger.set_logger(), "AAAA")
        # self.assertTrue(self.logger.set_logger())

    # def test_connect_log(self):
    #     self.logger.connect_log('http://192.168.3.116/api')
    #     self.assertIn('successful connection to http://192.168.3.116/api',
    #                   self.logger.log.handlers[1].stream.getvalue().strip())
    #
    # def test_enter_log(self):
    #     self.logger.enter_log('KKW')
    #     self.assertIn('KKW: log-in succeed', self.logger.log.handlers[1].stream.getvalue().strip())
    #
    # def test_create_working_file_log(self):
    #     self.logger.create_working_file_log('KKW', '/path/to/file')
    #     self.assertIn('"KKW" create maya file in "/path/to/file"',
    #                   self.logger.log.handlers[1].stream.getvalue().strip())
    #
    # def test_load_output_file_log(self):
    #     self.logger.load_output_file_log('KKW', '/path/to/file')
    #     self.assertIn('"KKW" load output file from "/path/to/file"',
    #                   self.logger.log.handlers[1].stream.getvalue().strip())
