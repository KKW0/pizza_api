#coding:utf8
import os
import gazu
from usemaya import MayaThings


class PublishThings:
    def __init__(self):
        self.maya = MayaThings()
        self._software = None

    def publish_file_data(self, task, comment):
        """
        Kitsu에 task에 대한 working file, output file 모델을 생성하는 매서드
        Kitsu에 워킹 파일과 아웃풋 파일에 대한 정보를 먼저 기록한 뒤,
        폴더를 생성하기 위한 path를 build 한다.
        Layout 팀에서는 working file이 하나, output file도 하나 나오기 때문에,
        파일은 revision만 올라가고 여러개가 나오지 않는다.

        Args:
            task(dict): 선택한 테스크의 딕셔너리
            comment(str): working file, output file에 대한 comment

        Returns:
            dict(output_file): Kitsu에 퍼블리싱한 output file의 딕셔너리
            str(output_path): output file이 저장된 경로(확장자 제외)
            dict(working_file): Kitsu에 퍼블리싱한 working file의 딕셔너리
            str(working_path): working file이 저장된 경로(확장자 제외)
        """
        # working file 생성
        working_file_list = gazu.files.get_working_files_for_task(task['id'])
        if working_file_list is []:
            # working file 없으면 새로 생성
            self._software = gazu.files.get_software_by_name('Maya')
            working_file = gazu.files.new_working_file(task['id'],
                                                       software=self._software['id'],
                                                       comment=comment,
                                                       person=gazu.client.get_current_user())
        else:
            # 이미 있으면 기존 정보 계승, 리비전은 이름이 같으면 자동으로 올라감
            old_working = working_file_list[0]
            self._software = old_working['software_id']
            working_file = gazu.files.new_working_file(task['id'],
                                                       name=old_working['name'],
                                                       software=self._software,
                                                       comment=comment,
                                                       person=gazu.client.get_current_user())

        # output file 생성
        output_type = gazu.files.get_output_type_by_name('Layout_mb')
        output_file_list = gazu.files.get_last_output_files_for_entity(task['entity_id'],
                                                                       output_type=output_type,
                                                                       task_type=task['task_type_id'])
        if output_file_list is []:
            # 샷에 Layout_mb 타입의 output file이 없으면 새로 생성
            output_file = gazu.files.new_entity_output_file(task['entity_id'],
                                                            output_type['id'],
                                                            task['task_type_id'],
                                                            comment=comment,
                                                            working_file=working_file,
                                                            person=gazu.client.get_current_user(),
                                                            representation='mb')
        else:
            # 샷에 Layout_mb 타입의 output file이 이미 있으면 정보 계승함
            old_output = output_file_list[0]
            output_type = old_output['output_type_id']
            output_file = gazu.files.new_entity_output_file(task['entity_id'],
                                                            output_type,
                                                            task['task_type_id'],
                                                            comment=comment,
                                                            working_file=working_file,
                                                            person=gazu.client.get_current_user(),
                                                            representation=old_output['representation'])

        # 마야에서 작업한 시퀀스를 저장하기 위해 폴더 패스 build
        working_path = gazu.files.build_working_file_path(task['id'], revision=working_file['revision'])
        output_path = gazu.files.build_entity_output_file_path(task['entity_id'],
                                                               output_type,
                                                               task['task_type_id'],
                                                               representation=output_file['representation'],
                                                               revision=output_file['revision'])

        return output_file, output_path, working_file, working_path

    def _make_folder_tree(self, path):
        """
        working file, output file을 save/export 하기 위한 실제 폴더를
        생성하는 매서드
        폴더가 이미 있으면 생성하지 않는다.

        Args:
            path(str): 파일명을 제외한 폴더 경로
        """

        if not os.path.exists(path):
            os.makedirs(path)
        else:
            raise SystemError("폴더가 이미 존재합니다.")

    def _upload_files(self, task, path, file_type, comment=None):
        """
        작업한 working file과 task에 대한 preview file을 Kitsu에 업로드하는 매서드
        output 파일에 대한 preview 모델을 생성한 뒤, 저장해둔 .mov 형식의 preview 파일을 업로드한다.

        Args:
            task(dict): 선택한 task의 딕셔너리
            path(str): working file 또는 output file의 확장자를 제외한 path
            comment(dict): preview file에 대한 comment dict(task의 comment와 같음)
            file_type(dict): working file 또는 preview file을 만들 output file의 딕셔너리
        """
        if 'working' in path:
            full_path = path + '.' + self._software['file_extension']
            gazu.files.upload_working_file(file_type, full_path)
        elif 'output' in path:
            full_path = path + '_preview' + '\d' + '.mov'
            if not gazu.files.get_all_preview_files_for_task(task):
                preview = gazu.task.create_preview(task, comment)
                gazu.task.upload_preview_file(preview, full_path)
                gazu.task.set_main_preview(preview)
            else:
                gazu.task.add_preview(task, comment, full_path)
        else:
            raise ValueError("working 또는 output file의 경로를 입력해주세요.")

    def save_publish_real_data(self, task, comment=None):
        """
        build된 패스에 맞추어 폴더 트리를 생성하고(make_floder_tree), 파일을 저장하는 매서드
        저장 후에는 Kitsu에 working file과 preview file을 업로드한다(upload_files)

        Args:
            task(dict): 선택한 task
            comment(str): working, output file, preview에 대한 comment
        """
        output_file, output_path, working_file, working_path = \
            self.publish_file_data(task, comment=comment)

        #  build 된 패스(확장자 없는 파일명까지 포함)에서 파일명을 잘라낸 패스를 만들고 폴더 생성
        path_working = os.path.dirname(working_path)
        path_output = os.path.dirname(output_path)
        self._make_folder_tree(path_working)
        self._make_folder_tree(path_output)

        # 마야에서 각 폴더에 working, output, preview file을 save
        self.maya.save_working_file(working_path, self._software['file_extension'])
        self.maya.export_output_file(output_path)

        # Kitsu에 preview, working file 업로드
        comment_dict = gazu.task.get_last_comment_for_task(task)
        self._upload_files(task, working_path, working_file)
        self._upload_files(task, output_path, output_file, comment_dict)
