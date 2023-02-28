#coding:utf8
import os
import json
import gazu


class Pizza_login:
    """
    The above class helps you log in and out to use pizza,
    and provides automatic login function through json.
    """
    def __init__(self):
        self._host = None
        self._user = None
        self._user_id = None
        self._user_pw = None
        self._check_host = False
        self._check_user = False

        self.path = os.path.expanduser('~/.config/pizza/')
        self.user_path = os.path.join(self.path + 'pizza.json')

    @property
    def host(self):
        return self._host

    @property
    def user(self):
        return self._user

    @property
    def check_host(self):
        return self._check_host

    @property
    def check_user(self):
        return self._check_user

    def setting(self):
        """
        Specifies the path of the json file and the path of the folder.
        """
        if not os.path.exists(self.path):
            try:
                os.makedirs(self.path)
            except OSError:
                pass
                # raise Exception("Error")

        try:
            if not os.path.exists(self.user_path):
                self.reset_setting()
        except OSError:
            pass
            # raise Exception("Error")

    def reset_setting(self):
        """
        Initialize the information that goes into the josn file and link it to save setting.
        """
        self._host = ''
        self._user_id = ''
        self._user_pw = ''
        self._check_host = False
        self._check_user = False

        self.save_setting()

    def save_setting(self):
        """
        Save the json file to the specified path as follows
        """
        user = {
            'host': self._host,
            'user_id': self._user_id,
            'user_pw': self._user_pw,
            'check_host': self._check_host,
            'check_user': self._check_user
        }

        with open(self.user_path, 'w') as json_file:
            json.dump(user, json_file)

    def connect_host(self, try_host):
        """
        Check the host path of pizza and add it to the json file if true.
        """
        gazu.set_host(try_host)
        if not gazu.client.host_is_valid():
            pass
            # raise Exception('Error')
        self._host = gazu.get_host()
        self._check_host = True
        self.save_setting()
        # self.logger.connect_log(self.host)
        return True

    def log_in(self, try_id, try_pw):
        """
        If the path of the host is correct,
        try to log in to pizza, and if successful,
        save the login information value as a json file.
        """
        if not self._check_host:
            pass
            # raise Exception('Error')
        try:
            log_in = gazu.log_in(try_id, try_pw)
        except gazu.AuthFailedException:
            pass
            # raise Exception('Error')

        self._user = log_in['user']
        self._user_id = try_id
        self._user_pw = try_pw
        self._check_user = True
        self.save_setting()
        # self.logger.enter_log(self.user.get("full_name"))
        return True

    def log_out(self):
        """
        If you log out of pizza,
        change the user's information to None and call reset setting.
        """
        gazu.log_out()
        self._user = None
        self.reset_setting()

    def load_setting(self):
        """
        If the value determined in the stored json file is True,
        the host and log_in functions are called.
        """
        user = {}
        with open(self.user_path, 'r') as json_file:
            user = json.load(json_file)

        if user.get('check_host'):
            self.connect_host(user.get('host'))
        if user.get('check_user'):
            self.log_in(user.get('user_id'), user.get('user_pw'))


# def main():
#     test = login()
#     # test.setting()
#     # test.host("http://192.168.3.116/api")
#     # test.log_in("pipeline@rapa.org", "netflixacademy")
#     test.load_setting()
#     # test.reset_setting()
#
#
# if __name__ == "__main__":
#     main()
