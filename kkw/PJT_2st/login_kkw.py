# coding=utf-8

from logger_kkw import Pizza_logger

import os
import json
import gazu

class Auth_br(object):
    def __init__(self):
        # self._host = None
        # self._user = None
        # self._user_id = None
        # self._user_pw = None
        # self._valid_host = False
        # self._valid_user = False
        # self._auto_login = False
        self.host = None
        self.user = None
        self.user_id = None
        self.user_pw = None
        self.valid_host = False
        self.valid_user = False
        self.auto_login = False

        self.logging = Pizza_logger()
        self.dir_path = os.path.expanduser('~/.config/pizza/')
        self.user_path = os.path.join(self.dir_path, 'user.json')

    # @property
    # def valid_host(self):
    #     """
    #
    #     현재 호스트 연결의 유효성을 반환하는 속성입니다.
    #
    #     """
    #     return self._valid_host
    #
    # @valid_host.setter
    # def valid_host(self, value):
    #     self._valid_host = value
    #
    # @property
    # def valid_user(self):
    #     """
    #
    #     현재 사용자 로그인의 유효성을 반환하는 속성입니다.
    #
    #     """
    #     return self._valid_user
    #
    # @valid_user.setter
    # def valid_user(self, value):
    #     self._valid_user = value
    #
    # @property
    # def host(self):
    #     """
    #
    #     현재 호스트의 URL을 반환하는 속성입니다.
    #
    #     """
    #     return self._host
    #
    # @host.setter
    # def host(self, value):
    #     self._host = value
    #
    # @property
    # def user(self):
    #     """
    #
    #     Returns:
    #         현재 로그인한 사용자의 사용자 사전을 반환합니다.
    #
    #     """
    #     return self._user
    #
    # @user.setter
    # def user(self, value):
    #     self._user = value
    #
    # @property
    # def user_id(self):
    #     return self._user_id
    #
    # @user_id.setter
    # def user_id(self, value):
    #     self._user_id = value
    #
    # @property
    # def user_pw(self):
    #     return self._user_pw
    #
    # @user_pw.setter
    # def user_pw(self, value):
    #     self._user_pw = value
    #
    # @property
    # def auto_login(self):
    #     return self._auto_login
    #
    # @auto_login.setter
    # def auto_login(self, value):
    #     self._auto_login = value

    def connect_host(self, host):
        """

        지정된 호스트 URL에 연결을 시도하고 인증 설정에 저장합니다.

        Args:
            try_host(str) : 연결할 호스트의 URL입니다.
        Returns:
            bool : 연결이 성공하면 True이고, 그렇지 않으면 False입니다.
        Raises:
            ValueError: 호스트 URL이 잘못된 경우.

        """

        # self.ui.text = self.text_edit.toPlainText()
        gazu.set_host(host)
        if not gazu.client.host_is_valid():
            self.logging.failed_log()
            raise ValueError('에러 메시지 : 호스트 URL이 잘못되었습니다.')
        # self._host = gazu.get_host()
        self.valid_host = True
        # self.save_setting()
        self.logging.connect_log(host)
        return True

    def log_in(self, host, user_id, user_pw, auto_login):
        """

        제공된 사용자 ID와 암호로 사용자를 로그인합니다.

        Args:
            try_id(str): 로그인할 사용자 ID입니다.
            try_pw(str): 로그인할 때 사용할 암호입니다.
        Returns:
            bool : 로그인이 성공하면 True이고, 그렇지 않으면 False입니다.
        Raises:
            SystemError: 자격 증명이 올바르지 않은 경우
            ValueError: 호스트가 연결되어 있지 않은 경우

        """

        # self.ui.id = self.text_edit.toPlainText()
        # self.ui.pw = self.text_edit.toPlainText()

        try:
            log_in = gazu.log_in(user_id, user_pw)
        except gazu.AuthFailedException:
            self.logging.failed_log()
            raise ValueError('에러 메시지 : 사용자 ID 또는 암호가 잘못 입력되었습니다.')

        self._user = log_in['user']
        self.save_setting(host, user_id, user_pw, True, True, auto_login)
        # self.logging.enter_log(self.user["full_name"])
        return True

    def log_out(self):
        """

        현재 사용자를 로그아웃합니다.

        Returns:
            None

        """
        if self._valid_user == True:
            gazu.log_out()
            self._user = None
            self.reset_setting()
        else:
            raise ValueError("로그인 부터 실행해")
        # return True

    def access_setting(self):
        """

        인증 디렉터리에 대한 액세스 설정을 확인하고 존재하지 않는 경우 user.json을 생성합니다.

        Returns:
            bool: 액세스 검사가 성공하면 True이고, 그렇지 않으면 False입니다.
        Raises:
            ValueError: OS 오류로 인해 dir_path에서 지정한 디렉토리를 생성할 수 없거나 user.json 파일을 생성할 수 없는 경우.

        """

        if not os.path.exists(self.dir_path):
            try:
                os.makedirs(self.dir_path)
            except OSError:
                raise ValueError("에러 메시지 : 디렉터리를 만들지 못했습니다.")

        try:
            if not os.path.exists(self.user_path):
                self.reset_setting()
        except OSError:
            raise ValueError("에러 메시지 : user.json 파일을 생성하지 못했습니다.")
        return True

    def load_setting(self):
        """

        user.json 파일에서 인증 설정을 load하고 필요한 경우 호스트에 연결합니다.

        Raises:
            ValueError : 호스트 URL 또는 사용자 ID 및 암호가 잘못된 경우
            SystemError : 로그인할 호스트가 연결되어 있지 않은 경우
            OSError : OS 오류로 인해 user.json 파일을 열 수 없는 경우

        """
        user_dict = {}
        with open(self.user_path, 'r') as json_file:
            user_dict = json.load(json_file)
        return user_dict
        # if user_dict['valid_host']:
        #     self.connect_host()
        # else:
        #     self.logging.failed_log()
        #     raise ValueError("에러에용")
        #
        # if user_dict['valid_user']:
        #     self.log_in(user_dict['user_id'], user_dict['user_pw'])
        # else:
        #     self.logging.failed_log()
        #     raise ValueError("Error")

    # 레이즈를 통해서 false 값일 경우 추가


    def save_setting(self, host, user_id, user_pw, valid_host, valid_user, auto_login):
        """

        현재 인증 설정을 user.json 파일에 저장합니다.

        Raises:
            OSError : OS 오류로 인해 user.json 파일을 쓸 수 없는 경우

        """

        user_dict = {
            'host': host,
            'user_id': user_id,
            'user_pw': user_pw,
            'valid_host': valid_host,
            'valid_user': valid_user,
            'auto_login': auto_login
        }
        with open(self.user_path, 'w') as json_file:
            json.dump(user_dict, json_file)

    def reset_setting(self):
        """

        인증 설정을 기본값으로 재설정합니다.

        """

        self._host = ''
        self._user_id = ''
        self._user_pw = ''
        self._valid_host = False
        self._valid_user = False
        self._auto_login = False

        # self.save_setting()


def main():
    test = Auth_br()
    # test.access_setting()
    # test.connect_host("http://192.168.3.116/api")
    # test.log_in("pipeline@rapa.org", "netflixacademy")
    # test.log_out()
    # test.load_setting()
    # test.reset_setting()


if __name__ == "__main__":
    main()