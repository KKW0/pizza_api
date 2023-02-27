#coding:utf-8

"""

이 코드는 인증 프로세스 중 또는 파일 작업 중에 발생할 수 있는 몇 가지 사용자 지정 예외를 정의합니다.

"""

class Error(Exception):
    """

    이 모듈의 모든 예외에 대한 기본 클래스입니다.

    """
    pass


class AuthFileIOError(Error):
    """

    인증 파일에 액세스하거나 인증 파일을 만드는 동안 오류가 발생하면 발생합니다.

    """
    pass


class UnconnectedHostError(Error):
    """

    연결된 호스트 없이 로그인을 시도할 때 발생합니다.

    """
    pass


class InvalidAuthError(Error):
    """

    로그인하는 동안 잘못된 사용자 ID 또는 암호를 입력하면 발생합니다.

    """
    pass


class DictTypeError(Error):
    """

    사전이 필요하지만 입력이 사전이 아닌 경우 상승.

    """
    pass


class WorkingFileExistsError(Error):
    """

    이미 존재하는 작업 파일을 만들 때 발생합니다.

    """
    pass


