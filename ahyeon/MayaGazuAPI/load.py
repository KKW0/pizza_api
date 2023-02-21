# import maya
from utils import construct_full_path
from logger import *
from auth import Auth
from exceptions import *
import gazu
import os


class Loader:

    def __init__(self, task):
        self.logger = Logger()
        self.auth = Auth()
        self.user_name = self.auth.user.get('full_name')
        self.selected_task = task
        self.new_nuke_working_file()

    def new_maya_working_file(self, name='main', comment='') -> dict:
        """
        새로운 Maya working file 생성
        선택한 task의 working file 생성,
        outputfile 만들 때 쓰일 dictionary 형태 working file을 반환한다.

        Args:
            name(str, optional): working file dict의 이름, 기본값 "main"
            comment(str, optional): working file dict의 설명

        Returns:
            dict: 생성된 working file dict
        """
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
                raise WorkingFileExistsError("Already exists working file")

        os.system(f"touch {working_file_path}")
        self.logger.create_working_file_log(self.user_name, working_file_path)

        return working_file