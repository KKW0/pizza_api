#coding:utf-8
# import maya
from logging import *
import os
import gazu
import construct_full_path


class Load:
    """
    Gazu 프로젝트 관리 시스템에서 선택한 작업에 대한 Maya 로더를 나타냅니다.

    Attributes:
        selected_task (dict): Gazu 프로젝트 관리 시스템에서 선택한 작업을 나타내는 사전입니다.
        user_name (str): 인증된 사용자의 전체 이름입니다.
        logger (Logger): 작업 파일 로그를 만드는 로거 개체입니다.
        auth (Auth): Gazu API에 액세스하기 위한 인증 개체입니다.

    Methods:
        new_maya_working_file(name='main', comment='') -> dict:
            선택한 작업에 대해 Gazu 프로젝트 관리 시스템에 새 Maya 작업 파일을 생성하고 새 작업 파일을 나타내는 사전을 반환합니다.
    """
    def __init__(self, task):
        self.user_name = self.auth.user.get('full_name')
        self.selected_task = task
        self.logger = Logger()
        self.auth = Auth()
        self.new_maya_working_file()

    def construct_full_path(file):
        path = file.get('path')
        file_type = file.get('type')
        padding = '.'
        if file_type == 'WorkingFile':
            software_id = file.get('software_id')
            ext = gazu.files.get_software(software_id).get('file_extension')
        elif file_type == 'OutputFile':
            output_type = file.get('output_type_id')
            ext = gazu.files.get_output_type(output_type).get('short_name')
            if ext in ['exr', 'dpx', 'jpg', 'jpeg', 'png', 'tga']:
                padding = '.####.'
        else:
            raise ValueError('file must be a WorkingFile or OutputFile dictionary')
        return path + padding + ext

    def new_maya_working_file(self, name='main', comment=''):

        maya = gazu.files.get_software_by_name('maya')
        user = gazu.client.get_current_user()
        working_file = gazu.files.new_working_file(self.selected_task, name=name, comment=comment,
                                                   software=maya, person=user)
        working_file_path = construct_full_path(working_file)

        root_dir = os.path.dirname(working_file_path)
        file_name = os.path.basename(working_file_path)

        if not os.path.exists(root_dir):
            os.mkdir(root_dir)

        for file in os.listdir(root_dir):
            if file == file_name:
                raise FileExistsError("Working file already exists")

        os.system("touch {0}".format(working_file_path))
        self.logger.create_working_file_log(self.user_name, working_file_path)

        return working_file