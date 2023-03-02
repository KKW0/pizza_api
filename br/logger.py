#coding:utf-8
import os
import json
import gazu

"""

이 api는 인증 및 로깅 작업을 처리하는 Logger 클래스를 제공합니다.

Logger 클래스를 사용하면 서버 호스트에 연결하고 사용자 ID와 암호로 로그인할 수 있습니다.
이러한 설정을 로컬 디렉터리의 user.json 파일에 저장합니다.
또한 작업 파일 생성 및 출력 파일 로드와 같은 응용 프로그램의 다양한 이벤트를 기록합니다.

gazu 라이브러리를 사용하여 인증 및 원격 서버와의 통신을 처리합니다. 
로깅 모듈을 사용하여 로그 메시지를 생성하고 파일에 기록합니다.

"""


<<<<<<< Updated upstream:br/logger.py


=======
>>>>>>> Stashed changes:euimin/Project/br/logger_br.py
class Pizza_logger:
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

        Args:
            dir_path (str): 사용자 정보가 저장될 디렉터리의 경로

        Raises:
            ValueError: 디렉터리 생성이 실패할 경우

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
                raise ValueError("에러 메시지 : 디렉터리를 만들지 못했습니다.")

        self.user_path = os.path.join(self.dir_path, 'user.json')

        if self.access_setting():
            self.load_setting()



    def set_logger(self):
        """

        logger instance에 stream handler 및 file handler를 추가하여 피자 응용 프로그램에 대한 로깅 구성을 설정합니다.
        INFO level에서 10개의 테스트 메시지를 기록합니다.

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

        DEBUG level에서 지정된 'host_url'에 대한 성공적인 연결을 기록합니다.

        """
        if host_url:
            self.log.debug("successful connection to {}".format(host_url))

    def enter_log(self, user_name):
        """

        DEBUG level에서 지정된 'user_name'을 사용하여 사용자의 성공적인 로그인을 기록합니다.

        """
        if user_name:
            self.log.debug("{}: log-in succeed".format(user_name))

    def create_working_file_log(self, user_name, working_file):
        """

        파일을 만든 사용자의 이름 및 파일 경로와 함께 DEBUG level에서 Maya 파일을 생성한 것을 기록합니다.
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
