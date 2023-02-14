#coding:utf8
import os
import gazu
import pprint as pp
from usemaya import MayaThings


class PublishThings:
    def __init__(self):
        self.maya = MayaThings()
        self._software = None
        self._output_type = None

    def _select_software(self, num=0):
        """
        테스크에 working file을 생성하기 위해, 작업에 사용한 소프트웨어를 선택하는 매서드

        Args:
            num(int): 소프트웨어 목록의 인덱스 번호
        Returns:
            dict: 선택한 소프트웨어의 딕셔너리
        """
        software_list = gazu.files.all_softwares()

        print('\n#### software list ####')
        pp.pprint(software_list)

        return software_list[num]

    def _select_output_type(self, shot, num=0):
        """
        테스크에 output file을 처음 생성할 경우, 필요한 output type을 선택하는 매서드

        Args:
            shot(dict): 선택한 task가 속한 shot의 딕셔너리
            num(int): output type 목록의 인덱스 번호
        Returns:
            dict: 선택한 output type의 딕셔너리
        """
        output_type_list = gazu.files.all_output_types_for_entity(shot['id'])

        print('\n#### output type list ####')
        pp.pprint(output_type_list)

        return output_type_list[num]

    def publish_file_data(self, shot, task, comment):
        """
        working file, output file 데이터를 생성하고 Kitsu에 publish하는 매서드
        Kitsu에 워킹 파일과 아웃풋 파일에 대한 정보를 먼저 기록한 뒤,
        폴더를 생성하기 위한 path를 build 한다.

        Args:
            shot(dict): 선택한 테스크가 속한 shot의 딕셔너리
            task(dict): 선택한 테스크의 딕셔너리
            comment(str): working file, output file에 대한 comment

        Returns:
            dict(output_file): Kitsu에 퍼블리싱한 output file의 딕셔너리
            str(output_path): output file이 저장된 경로(확장자 제외)
            dict(working_file): Kitsu에 퍼블리싱한 working file의 딕셔너리
            str(working_path): working file이 저장된 경로(확장자 제외)
        """
        # 테스크에 대한 워킹/아웃풋 파일 새로 생성
        # Layout 팀에서는 working file이 여러개 안 나옴. output file도 여러개 안 나옴(리비전만 올라감)

        # working file 생성
        # 테스크 하나에 워킹 파일이 여러개일 수는 없음. 리비전만 올라감(이름이 같으면 자동으로..)
        working_file_list = gazu.files.get_working_files_for_task(task['id'])
        if working_file_list is []:
            # working file 없으면 소프트웨어 선택해서 새로 생성
            self._software = self._select_software(0)
            working_file = gazu.files.new_working_file(task['id'],
                                                       software=self._software['id'],
                                                       comment=comment,
                                                       person=gazu.client.get_current_user())
        else:
            # 이미 있으면 기존 정보 계승하고 리비전만 올림
            old_working = working_file_list[0]
            self._software = old_working['software_id']
            working_file = gazu.files.new_working_file(task['id'],
                                                       software=self._software,
                                                       comment=comment,
                                                       person=gazu.client.get_current_user())

        # output file 생성
        # 워킹 파일 하나에 아웃풋은 여러개 나올 수 있지만 레이아웃은 아님
        output_file_list = gazu.files.get_last_output_files_for_entity(shot['id'],
                                                                       output_type='Previz',
                                                                       task_type=task['task_type'])
        if output_file_list is []:
            # 샷에 선택한 아웃풋 타입의 output file이 없으면 타입 선택해서 새로 생성
            output_type = self._select_output_type(shot, 0)
            output_file = gazu.files.new_entity_output_file(shot['id'],
                                                            output_type['id'],
                                                            task['task_type'],
                                                            comment=comment,
                                                            working_file=working_file,
                                                            person=gazu.client.get_current_user(),
                                                            representation=self._software['file_extension'])
                                                            # 'jpg'라고 써도 됨
        else:
            # 샷에 선택한 아웃풋 타입의 output file이 이미 있으면 정보 계승함
            old_output = output_file_list[0]
            output_type = old_output['output_type_id']
            output_file = gazu.files.new_entity_output_file(shot['id'],
                                                            output_type,
                                                            task['task_type'],
                                                            comment=comment,
                                                            working_file=working_file,
                                                            person=gazu.client.get_current_user(),
                                                            revision=old_output['revision']+1,
                                                            # +1 안써도 리비전 올라감
                                                            representation=old_output['representation'])

        # 마야에서 작업한 파일을 저장하기 위해 폴더 패스 build
        working_path = gazu.files.build_working_file_path(task['id'],
                                                          software=self._software,
                                                          revision=working_file['revision'])
        output_path = gazu.files.build_entity_output_file_path(shot['id'],
                                                               self._output_type,
                                                               task['task_type'],
                                                               representation=output_file['representation'],
                                                               revision=output_file['revision'],
                                                               nb_elements=output_file['nb_elements'])

        return output_file, output_path, working_file, working_path

    def _make_folder_tree(self, path):
        """
        working file, output file을 save/export 하기 위한 실제 폴더를
        생성하는 매서드

        Args:
            path(str): 파일명을 제외한 폴더 경로
        """
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            parent = os.path.dirname(path)
            if parent != "/":
                self._make_folder_tree(parent)
        # 테스트 해봐야 함

    def _upload_files(self, task, path, comment, file_type):
        """
        작업한 working file과 task에 대한 preview file을 Kitsu에 업로드하는 매서드

        Args:
            task(dict): 선택한 task의 딕셔너리
            path(str): working file 또는 output file의 확장자를 제외한 path
            comment(str): working file, preview file에 대한 comment
            file_type(dict): working file 또는 preview file을 만들 output file의 딕셔너리
        """
        if 'working' in path:
            full_path = path + '.' + self._software['file_extension']
            gazu.files.upload_working_file(file_type, full_path)
        elif 'output' in path:
            full_path = path + '_preview.mov'
            preview = gazu.task.create_preview(task, comment=comment)
            gazu.task.upload_preview_file(preview, full_path)

    def save_publish_real_data(self, shot, task, comment):
        """
        build된 패스에 맞추어 폴더 트리를 생성하고(make_floder_tree), 파일을 저장하는 매서드
        저장 후에는 Kitsu에 working file과 preview file을 업로드한다(upload_files)

        Args:
            shot(dict): 선택한 task가 속한 shot
            task(dict): 선택한 task
            comment(str): working, output file, preview에 대한 comment
        """
        output_file, output_path, working_file, working_path = \
            self.publish_file_data(shot, task, comment=comment)
        #  build 된 패스(확장자 없는 파일명까지 포함)에서 파일명을 잘라낸 패스를 만들고 폴더 생성
        path_working = os.path.dirname(working_path)
        path_output = os.path.dirname(output_path)
        self._make_folder_tree(path_working)
        self._make_folder_tree(path_output)

        # 마야에서 각 폴더에 working, output, preview file을 save
        self.maya.save_working_file(working_path, self._software['file_extension'])
        self.maya.export_output_file(output_path)

        # Kitsu에 preview, working file 업로드
        self._upload_files(task, working_path, working_file['comment'], working_file)
        self._upload_files(task, output_path, output_file['comment'], output_file)
