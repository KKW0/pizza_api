#coding:utf-8
from logger import Pizzalogger
from exception_ import *
import os
import json
import gazu


def connect_host(self, try_host):
    """

    지정된 호스트 URL에 연결을 시도하고 인증 설정에 저장합니다.

    Args:
        try_host(str) : 연결할 호스트의 URL입니다.
    Returns:
        bool : 연결이 성공하면 True이고, 그렇지 않으면 False입니다.
    Raises:
        InvalidAuthError: 호스트 URL이 잘못된 경우.

    """

    gazu.set_host(try_host)
    if not gazu.client.host_is_valid():
        raise InvalidAuthError('Error: Invalid host URL.')
    self._host = gazu.get_host()
    self._valid_host = True
    self.save_setting()
    self.pizza.connect_log(self.host)
    return True


def log_in(self, try_id, try_pw):
    """

    제공된 사용자 ID와 암호로 사용자를 로그인합니다.

    Args:
        try_id(str): 로그인할 사용자 ID입니다.
        try_pw(str): 로그인할 때 사용할 암호입니다.
    Returns:
        bool : 로그인이 성공하면 True이고, 그렇지 않으면 False입니다.
    Raises:
        InvalidAuthError: 자격 증명이 올바르지 않은 경우
        UnconnectedHostError: 호스트가 연결되어 있지 않은 경우

    """

    if not self._valid_host:
        raise UnconnectedHostError('Error: Host to login is not connected.')

    try:
        log_in = gazu.log_in(try_id, try_pw)
    except gazu.AuthFailedException:
        raise InvalidAuthError('Error: Invalid user ID or password.')

    self._user = log_in['user']
    self._user_id = try_id
    self._user_pw = try_pw
    self._valid_user = True
    self.save_setting()
    self.pizza.enter_log(self.user.get("full_name"))
    return True


def log_out(self):
    """

    현재 사용자를 로그아웃합니다.

    Returns:
        None

    """

    gazu.log_out()
    self._user = None
    self.reset_setting()


def access_setting(self):
    """

    인증 디렉토리에 대한 액세스 설정을 확인하고 존재하지 않는 경우 user.json을 생성합니다.

    Returns:
        bool: 액세스 검사가 성공하면 True이고, 그렇지 않으면 False입니다.
    Raises:
        AuthFileIOError: OS 오류로 인해 dir_path에서 지정한 디렉토리를 생성할 수 없거나 OS 오류로 인해 user.json 파일을 생성할 수 없는 경우.

    """

    if not os.path.exists(self.dir_path):
        try:
            os.makedirs(self.dir_path)
        except OSError:
            raise AuthFileIOError("Error: Failed to create the directory.")

    try:
        if not os.path.exists(self.user_path):
            self.reset_setting()
    except OSError:
        raise AuthFileIOError("Error: Failed to create user.json file.")
    return True


def load_setting(self):
    """

    user.json 파일에서 인증 설정을 로드하고 필요한 경우 호스트에 연결합니다.

    Raises:
        InvalidAuthError : 호스트 URL 또는 사용자 ID 및 암호가 잘못된 경우
        UnconnectedHostError : 로그인할 호스트가 연결되어 있지 않은 경우
        AuthFileIOError : OS 오류로 인해 user.json 파일을 열 수 없는 경우

    """
    user_dict = {}
    with open(self.user_path, 'r') as json_file:
        user_dict = json.load(json_file)

    if user_dict.get('valid_host'):
        self.connect_host(user_dict.get('host'))
    if user_dict.get('valid_user'):
        self.log_in(user_dict.get('user_id'), user_dict.get('user_pw'))


def save_setting(self):
    """

    현재 인증 설정을 user.json 파일에 저장합니다.

    Raises:
        AuthFIleIOError : OS 오류로 인해 user.json 파일을 쓸 수 없는 경우

    """

    user_dict = {
        'host': self.host,
        'user_id': self._user_id,
        'user_pw': self._user_pw,
        'valid_host': self.valid_host,
        'valid_user': self.valid_user,
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


