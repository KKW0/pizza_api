from unittest import TestCase
import os
import logging
from logger import Pizza_logger
from login import Auth_br


class TestPizza_logger(TestCase):
    def setUp(self):
        self.logger = Pizza_logger()
        self.user_path = './test_logs'
        self.login = Auth_br()
        self.login.connect_host('http://192.168.3.116/api')
        self.login.log_in('pipeline@rapa.org', 'netflixacademy')

    # def test_set_logger(self):
    #     self.dir_path = './test_logs'
    #     self.logger = Pizza_logger(self.dir_path)
    #     self.assertIsNotNone(self.logger.log.handlers)
    #
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
