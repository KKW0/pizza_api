#coding:utf-8
from logging import *
import os
import json
import gazu

"""

이 모듈은 인증 및 로깅 작업을 처리하는 Logger 클래스를 제공합니다.

Logger 클래스를 사용하면 서버 호스트에 연결하고 사용자 ID와 암호로 로그인할 수 있습니다.
그리고 이러한 설정을 로컬 디렉토리의 user.json 파일에 저장합니다.
또한 작업 파일 생성 및 출력 파일 로드와 같은 응용 프로그램의 다양한 이벤트를 기록합니다.

gazu 라이브러리를 사용하여 인증 및 원격 서버와의 통신을 처리합니다. 
로깅 모듈을 사용하여 로그 메시지를 생성하고 파일에 기록합니다.

"""


class PizzaLogger:
    """

    위 클래스는 피자 응용 프로그램에 대한 로깅을 처리합니다.

    Attributes:
    - dir_path (str): 로그 파일이 저장될 디렉터리의 경로입니다.
    - user_path (str): 사용자의 인증 정보가 저장된 JSON 파일의 경로입니다.
    - logger (Logger): 인증 이벤트를 기록하는 Logger 클래스의 인스턴스.
    - _host (str): 사용자가 연결된 호스트의 URL입니다.
    - _user (dict): 로그인한 사용자에 대한 정보가 들어 있는 사전입니다.
    - _user_id (str): 로그인한 사용자의 ID입니다.
    - _user_pw (str): 로그인한 사용자의 암호입니다.
    - _valid_host (bool): 호스트에 대한 연결이 유효한지 여부를 나타내는 플래그입니다.
    - _valid_user (bool): 로그인 자격 증명이 유효한지 여부를 나타내는 플래그입니다.
    - log (logging.Logger): 메시지를 로깅하는 데 사용되는 로거 개체입니다.



    Methods:
    - __init__(): Logger 개체를 초기화합니다.
    - valid_host(): _valid_host 특성의 값을 반환합니다.
    - valid_user(): _valid_user 특성의 값을 반환합니다.
    - host(): _host 특성의 값을 반환합니다.
    - user(): _user 특성의 값을 반환합니다.
    - connect_host(try_host): 지정한 호스트에 연결하고 그에 따라 _host 및 _valid_host 특성을 설정합니다.
    - log_in(try_id, try_pw): 지정된 사용자 ID와 암호를 사용하여 현재 연결된 호스트에 로그인하고 그에 따라 _user, _user_id, _user_pw 및 _valid_user 특성을 설정합니다.
    - log_out(): 현재 로그인한 사용자를 로그아웃합니다.
    - access_setting(): 사용자 구성 디렉터리 및 user.json 파일이 있는지 확인하고 없으면 생성합니다.
    - load_setting(): user.json 파일에서 사용자 설정을 로드하고 그에 따라 _host, _user, _user_id 및 _user_pw 특성을 설정합니다.
    - save_setting(): 현재 사용자 설정을 user.json 파일에 저장합니다.
    - reset_setting(): 현재 사용자 설정을 기본값으로 재설정합니다.
    - set_logger(): 로거 개체를 설정하고 여기에 핸들러를 추가합니다.
    - connect_log(host_url): 지정한 호스트에 대한 연결이 성공했음을 나타내는 메시지를 기록합니다.
    - enter_log(user_name): 지정한 이름의 사용자가 성공적으로 로그인했음을 나타내는 메시지를 기록합니다.
    - create_working_file_log(user_name, working_file): 지정한 이름을 가진 사용자가 지정한 위치에 Maya 파일을 생성했음을 나타내는 메시지를 기록합니다.
    - load_output_file_log(user_name, output_file_path): 지정한 이름을 가진 사용자가 지정한 위치에서 출력 파일을 로드했음을 나타내는 메시지를 기록합니다.
    """

    def __init__(self, dir_path):
        """
        Logger 개체를 초기화합니다.

        :argument:
            dir_path (str): The path to the directory where user information will be stored.

        :raises:
            AuthFileIOError: If the directory creation fails.
        """
        self._host = None
        self._user = None
        self._user_id = None
        self._user_pw = None
        self._valid_host = False
        self._valid_user = False
        self.log = None

        self.set_logger(dir_path)

        self.dir_path = dir_path
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
        현재 호스트 연결의 유효성을 반환하는 속성입니다.
        """
        return self._valid_host

    @property
    def valid_user(self):
        """
        현재 사용자 로그인의 유효성을 반환하는 속성입니다.
        """
        return self._valid_user

    @property
    def host(self):
        """
        현재 호스트의 URL을 반환하는 속성입니다.
        """
        return self._host

    @property
    def user(self):
        """
        현재 로그인한 사용자의 사용자 사전을 반환합니다.

        :return:
        dict: 현재 로그인한 사용자의 사용자 사전입니다.
        """
        return self._user

    def connect_host(self, try_host):
        """
        지정된 호스트 URL에 연결을 시도하고 인증 설정에 저장합니다.
        :argument:
            try_host(str) : 연결할 호스트의 URL입니다.
        :return:
            bool : 연결이 성공하면 True이고, 그렇지 않으면 False입니다.
        :raises:
            InvalidAuthError: 호스트 URL이 잘못된 경우.
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
        제공된 사용자 ID와 암호로 사용자를 로그인합니다.

        :argument:
            try_id(str): 로그인할 사용자 ID입니다.
            try_pw(str): 로그인할 때 사용할 암호입니다.
        :return:
            bool : 로그인이 성공하면 True이고, 그렇지 않으면 False입니다.
        :raises:
            InvalidAuthError: 자격 증명이 올바르지 않은 경우.
            UnconnectedHostError: 호스트가 연결되어 있지 않은 경우.
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
        현재 사용자를 로그아웃합니다.

        :return:
            None
        """

        gazu.log_out()
        self._user = None
        self.reset_setting()

    def access_setting(self):
        """
        인증 디렉토리에 대한 액세스 설정을 확인하고 존재하지 않는 경우 user.json을 생성합니다.

        :return:
            bool: 액세스 검사가 성공하면 True이고, 그렇지 않으면 False입니다.
        :raises:
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

        :raises:
            InvalidAuthError : 호스트 URL 또는 사용자 ID 및 암호가 잘못된 경우.
            UnconnectedHostError : 로그인할 호스트가 연결되어 있지 않은 경우.
            AuthFileIOError : OS 오류로 인해 user.json 파일을 열 수 없는 경우.
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

        :raises:
            AuthFIleIOError: OS 오류로 인해 user.json 파일을 쓸 수 없는 경우.
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

    def set_logger(self):
        """
        로거 인스턴스에 스트림 핸들러 및 파일 핸들러를 추가하여 피자 응용 프로그램에 대한 로깅 구성을 설정합니다.
        INFO 수준에서 10개의 테스트 메시지를 기록합니다.
        """
        self.log = logging.getLogger('pizza')

        if len(self.log.handlers) == 0:
            formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
            self.log.setLevel(logging.DEBUG)

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            stream_handler.setLevel(logging.INFO)
            self.log.addHandler(stream_handler)

            file_handler = logging.FileHandler(os.path.join(self.dir_path, 'pizza_test.log'))
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)
            self.log.addHandler(file_handler)

        for i in range(10):
            self.log.info('{}번째 방문입니다.'.format(i))

    def connect_log(self, host_url):
        """
        DEBUG 수준에서 지정된 'host_url'에 대한 성공적인 연결을 기록합니다.
        """
        if host_url:
            self.log.debug("successful connection to {}".format(host_url))

    def enter_log(self, user_name):
        """
        DEBUG 수준에서 지정된 'user_name'을 사용하여 사용자의 성공적인 로그인을 기록합니다.
        """
        if user_name:
            self.log.debug("{}: log-in succeed".format(user_name))

    def create_working_file_log(self, user_name, working_file):
        """
        파일을 만든 사용자의 이름 및 파일 경로와 함께 DEBUG 수준에서 Maya 파일을 생성한 것을 기록합니다.
        파일이 없으면 경고 메시지를 기록합니다.
        """
        if os.path.exists(working_file):
            self.log.debug("\"%s\" create maya file in \"%s\"" % (user_name, working_file))
        else:
            self.log.warning("\"%s\" failed to create Maya file" % user_name)

    def load_output_file_log(self, user_name, output_file_path):
        """
        파일을 로드한 사용자의 이름과 파일 경로와 함께 DEBUG 수준의 출력 파일 로드를 기록합니다.
        """
        return self.log.debug("\"%s\" load output file from \"%s\"" % (user_name, output_file_path))

