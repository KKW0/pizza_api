#coding:utf-8
import logging
import os
import json
import gazu


class Logger:
    """

    다른 부서에서 작업한 아웃풋 파일을 load할 때 생성되는 마야 작업 파일 기록
    사용자의 kistu 계정 정보를 관리하기 위한 class
    local 환경에 저장된 계정 정보를 관리하고, gazu client에 login, logout
    객체 생성시 json file을 찾아 host 연결과 로그인을 시도

    """
    def __init__(self):
        self._host = None
        self._user = None
        self._user_id = None
        self._user_pw = None
        self._valid_host = False
        self._valid_user = False
        self.log = None

        self.set_logger()

        self.dir_path = os.path.expanduser('~/.config/Pizza')
        if not os.path.exists(self.dir_path):
            try:
                os.makedirs(self.dir_path)
            except OSError:
                raise AuthFileIOError("Error: Failed to create the directory.")

        self.user_path = os.path.join(self.dir_path, 'user.json')

        if self.access_setting():
            self.load_setting()


@property
def valid_host(self):
    """
    bool: host 연결에 성공했다면 True, 아니면 False
    """
    return self._valid_host


@property
def valid_user(self):
    """
    bool: 로그인에 성공했다면 True, 아니면 False
    """
    return self._valid_user


@property
def host(self):
    """
    str: 연결된 host URL
    """
    return self._host


@property
def user(self):
    """
    dict: 로그인한 계정의 user dict
    """
    return self._user


def connect_host(self, try_host):
    """
    try_host를 사용해 host에 접속 시도

    Returns:
        bool: 접속에 성공하면 True, 아니면 False 반환
    """
    gazu.set_host(try_host)
    if not gazu.client.host_is_valid():
        raise InvalidAuthError('Error: Invalid host URL.')
    self._host = gazu.get_host()
    self._valid_host = True
    self.save_setting()
    self.logger.connect_log(self.host)
    return True


def log_in(self, try_id, try_pw):
    """
    try_id, try_pw를 사용해 로그인 시도

    Returns:
        bool: 접속에 성공하면 True, 아니면 False 반환
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
    self.logger.enter_log(self.user.get("full_name"))
    return True


def log_out(self):
    """
    log out한 후 저장되어있던 json 정보 삭제
    """
    gazu.log_out()
    self._user = None
    self.reset_setting()


def access_setting(self):
    """
    디렉토리와 각 json 파일이 존재하는지 확인하고 없으면 초기화

    Returns:
        bool: self.user_path에 해당하는 json 파일이 존재하거나 생성되면 True, 아니면 False
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
    json file에서 정보를 읽어오기

    json에 기록된 host나 user의 valid 값이 True이면 자동 login
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
    json file에 정보를 저장
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
    json file에 저장된 정보 삭제
    """
    self._host = ''
    self._user_id = ''
    self._user_pw = ''
    self._valid_host = False
    self._valid_user = False

    self.save_setting()


class Error(Exception):
    """
    에러 예외 사항
    """
    pass


class AuthFileIOError(Exception):
    """
    로그인 관련 파일 생성 및 입출력에 실패한 경우
    """
    pass


class UnconnectedHostError(Exception):
    """
    host에 연결되어 있지 않은 상태에서 login을 시도한 경우
    """
    pass


class InvalidAuthError(Exception):
    """
    유효하지 않은 host, id, pw 값으로 연결을 시도한 경우
    """
    pass


class DictTypeError(Exception):
    """
    입력으로 들어온 dict의 type이 부적절한 경우
    """
    pass


class WorkingFileExistsError(Exception):
    """
    생성하고자 하는 working file 경로에 파일이 이미 존재하는 경우
    """
    pass

    def set_logger(self):
        """

        Returns:
            (.log) file: {user, time, path, output file path log} data
        """
        # 로그 생성
        self.log = logging.getLogger('pizza')

        if len(self.log.handlers) == 0:
            # log 출력 형식
            formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
            # 로그의 출력 기준 설정
            self.log.setLevel(logging.DEBUG)

            # log 출력
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            stream_handler.setLevel(logging.INFO)
            self.log.addHandler(stream_handler)

            # log를 파일에 출력
            file_handler = logging.FileHandler(os.path.join(self.dir_path, 'pizza_test.log'))
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)
            self.log.addHandler(file_handler)

        for i in range(10):
            self.log('{}번째 방문입니다.'.format(i))

    def connect_log(self, host_url):
        if host_url:
            self.log.debug("successful connection to {}".format(host_url))

    def enter_log(self, user_name):
        if user_name:
            self.log.debug("{}: log-in succeed".format(user_name))

    def create_working_file_log(self, user_name, working_file):
        """
        working file(.mb)이 정확한 위치에 생성 됐는지 확인
        """
        if os.path.exists(working_file):
            self.log.debug(f"\"{user_name}\" create maya file in \"{working_file}\"")
        else:
            self.log.warning(f"\"{user_name}\" failed to create Maya file")

    def load_output_file_log(self, user_name, output_file_path):
        return self.log.debug(f"\"{user_name}\" load output file from \"{output_file_path}\"")
