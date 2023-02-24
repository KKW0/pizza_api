# import maya
from logging import *
import os
import gazu
import construct_full_path




class Load:

    def __init__(self, task):
        # self.logger = Logger()
        # self.auth = Auth()
        self.user_name = self.auth.user.get('full_name')
        self.selected_task = task
        self.new_maya_working_file()

    def construct_full_path(file: dict):
        """
        output file이나 working file의 딕셔너리를 받아서 확장자까지 연결된 full path를 반환

        Args:
            file(dict):working file 혹은 output file dict

        Returns:
            str: file의 실제 절대경로
                    {dir_name}/{file_name}.{extension}
                확장자가 레스터 이미지 확장자인 경우, padding을 포함
                    {dir_name}/{file_name}.####.{extension}
        """
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
            raise Exception('파일 딕셔너리가 아님')
        return path + padding + ext

    def new_maya_working_file(self, name='main', comment='') -> dict:
        """

        Args:
            name(str, optional): working file dict의 이름, 기본값 "main"
            comment(str, optional): working file dict의 설명

        Returns:
            dict: create working file dict
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