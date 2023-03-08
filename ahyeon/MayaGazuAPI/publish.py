#coding:utf8
import os
import gazu
from usemaya import MayaThings

 
class PublishThings:
    """
    작업한 결과물을 실제 폴더에 저장하고, Kitsu에 퍼블리시하는 클래스
    """
    def __init__(self):
        """
        모듈의 인스턴스를 생성하고, 전역변수를 정의한다.
        """
        self.maya = MayaThings()
        self._software = None
        self._task_status = gazu.task.get_task_status_by_name('Todo')
        self._preview_type = None

    def _publish_file_data(self, task, comment):
        """
        Kitsu에 task에 대한 working file, output file 모델을 생성하는 매서드

        Kitsu에 워킹 파일과 아웃풋 파일에 대한 모델을 생성하고,
        작업 결과물을 저장할 폴더 path를 build 한다. 이 path는 return으로 넘겨 실제 폴더 생성까지 이어진다.
        Layout 팀에서는 working file이 하나(.ma), output file도 하나(.mb) 나오기 때문에,
        각 파일은 revision만 올라가며, 여러 모델이 나오지 않는다.

        path와 파일명의 규칙은 아래와 같다.
        path: <Project>/assets/<AssetType>/<Asset>/<TaskType>/output/<OutputType>/v<Revision>
        file: <Project>_<AssetType>_<Asset>_<OutputType>_v<Revision>

        Args:
            task(dict): 선택한 테스크의 딕셔너리
            comment(str): 퍼블리시할 working file, output file에 대한 comment

        Returns:
            str(output_path): output file이 저장될 경로(확장자 제외)
            dict(working_file): Kitsu에 퍼블리시한 working file의 딕셔너리
            str(working_path): working file이 저장될 경로(확장자 제외)
            str(preview_path): preview file이 저장될 경로(확장자 제외)
        """
        casted_list = gazu.casting.get_asset_cast_in(task['entity_id'])
        for cast in casted_list:
            if 'SEQ' in cast['name']:
                seq = cast

        # working file 모델 생성
        working_file_list = gazu.files.get_working_files_for_task(task['id'])
        if working_file_list is []:
            # task가 주어진 에셋에 working file 모델이 없으면 새로 생성
            self._software = gazu.files.get_software_by_name('Maya')
            working_file = gazu.files.new_working_file(task['id'],
                                                       name=seq['name']+'_layout_working',
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

        # output file 모델 생성
        output_type = gazu.files.get_output_type_by_name('Layout_mb')
        output_file_list = gazu.files.get_last_output_files_for_entity(task['entity_id'],
                                                                       output_type=output_type,
                                                                       task_type=task['task_type_id'])
        if output_file_list is []:
            # task가 주어진 에셋에 Layout_mb 타입의 output file이 없으면 새로 생성
            output_file = gazu.files.new_entity_output_file(task['entity_id'],
                                                            output_type['id'],
                                                            task['task_type_id'],
                                                            comment=comment,
                                                            working_file=working_file,
                                                            person=gazu.client.get_current_user(),
                                                            name=seq['name'] + '_layout_output',
                                                            representation='mb')
        else:
            # Layout_mb 타입의 output file이 이미 있으면 정보 계승함
            old_output = output_file_list[0]
            output_type = old_output['output_type_id']
            output_file = gazu.files.new_entity_output_file(task['entity_id'],
                                                            output_type,
                                                            task['task_type_id'],
                                                            comment=comment,
                                                            working_file=working_file,
                                                            person=gazu.client.get_current_user(),
                                                            name=old_output['name'],
                                                            representation=old_output['representation'])

        # 마야에서 작업한 에셋을 저장하기 위한 폴더 패스 build
        working_path = gazu.files.build_working_file_path(task['id'], revision=working_file['revision'])
        output_path = gazu.files.build_entity_output_file_path(task['entity_id'],
                                                               output_type,
                                                               task['task_type_id'],
                                                               representation=output_file['representation'],
                                                               revision=output_file['revision'])
        # main preview용 패스 build
        self._preview_type = gazu.files.get_output_type_by_name('Preview')
        preview_path = gazu.files.build_entity_output_file_path(task['entity_id'],
                                                                self._preview_type,
                                                                task['task_type_id'],
                                                                representation='mov',
                                                                revision=output_file['revision'])

        return output_path, working_file, working_path, preview_path

    def _make_folder_tree(self, path):
        """
        working file, output file을 save/export 하기 위한 실제 폴더를 생성하는 매서드

        폴더가 이미 있으면 생성하지 않는다.

        Args:
            path(str): 파일명을 제외한 폴더 경로
        """

        if os.path.exists(path) is False:
            os.makedirs(path)
        else:
            raise SystemError("폴더가 이미 존재합니다.")

    def _upload_files(self, task, path, file_type=None, comment=None):
        """
        작업한 working file과 task에 대한 preview file을 Kitsu에 업로드하는 매서드

        저장할 파일이 working file인지, preview file인지 먼저 판단한다.
        path에 working 이라는 폴더명이 포함되어 있으면 working file,
        output file을 저장하는 폴더에 메인 프리뷰를 함께 저장하며,
        따라서 path에 output 이라는 폴더명이 포함되어 있으면 preview file을 퍼블리시함을 의미한다.
        preview를 퍼블리시 할 경우, 먼저 task에 대한 preview 모델을 생성한 뒤,
        미리 저장해둔 .mov 형식의 파일(main preview)을 Kitsu에 업로드한다.

        Args:
            task(dict): 선택한 task의 딕셔너리
            path(str): working file 또는 main preview file의 확장자를 제외한 path
            file_type(dict): 업로드할 working file의 딕셔너리. preview를 업로드할 경우 사용하지 않는다.
        """
        if 'working' in path:
            # working file 업로드
            full_path = path + '.' + self._software['file_extension']
            gazu.files.upload_working_file(file_type, full_path)
        elif 'output' in path:
            # main preview file 업로드
            comment = gazu.task.add_comment(task, self._task_status, comment)
            filenames = os.listdir(os.path.dirname(path))
            for filename in filenames:
                if '.mov' in filename:
                    full_path = os.path.dirname(path) + filename
            if gazu.files.get_all_preview_files_for_task(task):
                # preview가 이미 존재하면 add
                preview = gazu.task.add_preview(task, comment, full_path)
            else:
                # preview가 존재하지 않으면 생성 후 upload
                preview = gazu.task.create_preview(task, comment)
                gazu.task.upload_preview_file(preview, full_path)
            gazu.task.set_main_preview(preview)
        else:
            raise ValueError("working 또는 output file의 경로를 입력해주세요.")

    def save_publish_real_data(self, task, comment=None):
        """
        build된 패스(publish_file_data)에 맞추어 실제 폴더를 만든 뒤(make_folder_tree)
        working, output 파일을 저장하고(maya.save_scene_file, maya.export_output_file),
        Kitsu에 working file과 main preview를 업로드하는(upload_files) 매서드

        Args:
            task(dict): 선택한 task의 딕셔너리
            comment(str): working, output file, preview에 대한 comment
        """
        output_path, working_file, working_path, preview_path = \
            self._publish_file_data(task, comment=comment)

        #  build 된 패스(확장자 없는 파일명까지 포함)에서 파일명을 잘라낸 패스를 만들고 폴더 생성
        path_working = os.path.dirname(working_path)
        path_output = os.path.dirname(output_path)
        path_preview = os.path.dirname(preview_path)
        self._make_folder_tree(path_working)
        self._make_folder_tree(path_output)
        self._make_folder_tree(path_preview)

        # 마야에서 각 폴더에 working, output, main preview를 save하고
        # working file과 main preveiw를 kitsu에 업로드
        self.maya.save_scene_file(working_path, self._software['file_extension'])
        self.maya.export_output_n_main_preview_file(output_path, preview_path)
        self._upload_files(task, working_path, working_file)
        self._upload_files(task, preview_path, comment=comment)

    def save_publish_previews(self, shot_list, comment):
        """
        각 샷에 해당하는 레이아웃의 preview file을 업로드하는 매서드

        먼저 프리뷰 파일이 저장된 path를 build하고, shot에는 Layout의 Preview 올리기 용도의 task만 있고
        output이나 working file이 존재하지 않기 때문에 폴더 path의 revision을 직접 업데이트한다.
        그 다음 해당 폴더에 각 샷에 대한 preview를 저장한다.(maya.export_shot_previews)
        마지막으로 저장된 preview file들을 각각의 샷에 맞게 Kitsu에 퍼블리시, 업로드해준다.

        Args:
            shot_list(list): 에셋이 캐스팅된 시퀀스 아래에 있는 모든 샷 딕셔너리들의 집합
            comment(str): 프리뷰를 올릴 때 첨부할 코멘트
        """
        revision = 0
        task_type = gazu.task.get_task_type_by_name('Layout')
        for shot in shot_list:
            path = gazu.files.build_entity_output_file_path(shot, self._preview_type,
                                                            task_type, revision=revision)
            while os.path.exists(path) is True:
                revision += 1
                path = gazu.files.build_entity_output_file_path(shot, self._preview_type,
                                                                task_type, revision=revision)
            self.maya.export_shot_previews(path, shot)

            # Kitsu에 shot의 preview file 업로드
            full_path = path + '.mov'
            task = gazu.task.get_task_by_entity(shot, task_type)
            comment_dict = gazu.task.add_comment(task, self._task_status, comment)
            gazu.task.add_preview(task, comment_dict, full_path)
