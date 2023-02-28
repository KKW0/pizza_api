from unittest import TestCase
from pizza.login import Pizza_login


class TestPizza_login(TestCase):
    def setUp(self):
        self.auth = Pizza_login()
    def test_host(self):
        self.assertTrue(True)

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
