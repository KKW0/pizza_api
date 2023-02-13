#coding:utf8
import os
import gazu
import pprint as pp
import maya.mc as mc


class ImportThings(object):
    """
    프로젝트에서 사용자에게 주어진 테스크 중 하나를 선택하고,
    테스크가 소속된 샷에 캐스팅되어 있는 에셋 데이터를 가져오고,
    각 에셋의 working file과 output file을 추출하여,
    씬에 import 해서 레이아웃 작업을 한 뒤에,
    작업한 working file과 output file을 실제 폴더 트리에 저장하고,
    그것들을 Kitsu에 퍼블리싱하고, working file을 업로드도 해주는 클래스
    Layout 팀을 위한 api
    """
    def __init__(self):
        gazu.client.set_host("http://192.168.3.116/api")
        gazu.log_in("pipeline@rapa.org", "netflixacademy")

        self._working_file = None
        self._output_file = None
        self._working_path = None
        self._output_path = None
        # publish할 때 사용

        self._person = None
        # user 쓸거면 안써도 되려나 싶음...
        self._project = None
        self._task = None
        self._shot = None
        self._software = None
        self._output_type = None

    @property
    def person(self):
        return self._person

    @person.setter
    def person(self, value):
        """
        task 목록을 보고 싶은 유저의 정보를 저장해주는 세터
        user에게 할당된 테스크가 많다면 필요 없을 듯...
        영빈님한테만 테스크가 할당되어 있어서 테스트 용으로 만듦....

        Args:
            value(str): 영빈 td님 성함...
        """
        self._person = gazu.person.get_person_by_full_name(value)

    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, value):
        """
        테스크가 있는 프로젝트를 선택하는 세터

        Args:
            value(str): 프로젝트 이름
        """
        self._project = gazu.project.get_project_by_name(value)

    # ----------------------------- kitsu/gazu -----------------------------

    def update_filetree(self, mountpoint, root):
        """
        필요할 시 파일 트리를 업데이트하는 매서드

        Args:
            mountpoint(str/path): 폴더 트리를 생성할 위치의 전체 경로
            root(str/folder name): 폴더 트리를 생성할 mountpoint의 자식 폴더 이름
        """
        tree = {
            "working": {
                "mountpoint": mountpoint,
                "root": root,
                "folder_path": {
                    "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>/working/v<Revision>",
                    "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>/working/v<Revision>",
                    "style": "lowercase"
                },
                "file_name": {
                    "shot": "<Project>_<Sequence>_<Shot>_<TaskType>_<Revision>",
                    "asset": "<Project>_<AssetType>_<Asset>_<TaskType>_<Revision>",
                    "style": "lowercase"
                }
            },
            "output": {
                "mountpoint": mountpoint,
                "root": root,
                "folder_path": {
                    "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>/output/<OutputType>/v<Revision>",
                    "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>/output/<OutputType>/v<Revision>",
                    "style": "lowercase"
                },
                "file_name": {
                    "shot": "<Project>_<Sequence>_<Shot>_<OutputType>_v<Revision>",
                    "asset": "<Project>_<AssetType>_<Asset>_<OutputType>_v<Revision>",
                    "style": "lowercase"
                }
            }
        }
        gazu.files.update_project_file_tree(self._project, tree)

    def select_task(self, num=0):
        """
        수행할 task를 선택하는 매서드
        task는 선택한 person 또는 user에 assign되어 있어야 하고, 상태가 Todo여야 한다.

        Args:
            num(int): task list의 인덱스 번호
        """
        task_list = []
        task_list_user = gazu.task.all_tasks_for_person(self.person)
        # user에게 테스크가 충분히 할당되어 있다면 gazu.user.all_tasks_to_do() 로 대체
        for task in task_list_user:
            if task['project_id'] == self.project['id'] \
                    and task['task_status_name'] == 'Todo':
                task_list.append(task)

        print('\n#### task list ####')
        pp.pprint(task_list)

        self._task = task_list[num]

    def get_kitsu_path(self, casting):
        """
        샷에 캐스팅된 에셋의 최신 output file들의 패스 리스트를 추출하는 매서드

        Args:
            casting(dict): 샷에 캐스팅된 에셋의 간략한 정보가 담긴 dict

        Returns:
            list: 아웃풋 파일들의 패스(확장자 포함), 개수, 확장자가 담긴 dict를 수집한 리스트
        """
        file_list = []
        file_dict = {
            'path': "",
            'nb_elements': 0,
        }
        asset = gazu.asset.get_asset(casting['asset_id'])
        output_file_list = gazu.files.get_last_output_files_for_entity(asset)
        for out_file in output_file_list:
            # 각 output file의 패스를 생성하고, 리스트에 append
            out_path = gazu.files.build_entity_output_file_path(asset,
                                                                out_file['output_type'],
                                                                out_file['task_type'],
                                                                revision=out_file['revision'])
            path = out_path + '.' + out_file['representation']
            file_dict['path'] = path
            file_dict['nb_elements'] = out_file['nb_elements']
            file_list.append(file_dict)

        return file_list

    # ----------------------------- maya -----------------------------

    def load_working(self):
        """
        마야에서 선택한 테스크에 working file이 이미 있을 경우,
        해당 파일을 import 하는 매서드

        """

    def load_output(self, path):
        """
        마야에서 샷에 캐스팅된 에셋의 output file들을 import하는 매서드

        Args:
            path(str): 파일명까지 포함된 에셋의 아웃풋 파일의 패스
        """
        mc.file(
            path, i=True, ignoreVersion=True,
            mergeNamespacesOnClash=False, importTimeRange="combine",
            loadReferenceDepth="all",
            returnNewNodes=True
        )

    def import_casting_asset(self):
        """
        수행중인 테스크(샷)에 캐스팅된 에셋의 저장위치를 모두 추출하여 마야에 import 하는 매서드
        output file의 각각의 확장자 포함된 패스를 추출하고(get_kitsu_path),
        추출한 패스를 기반으로 마야에 import 한다.(load_output)

        file_dict_list: 에셋에 있는 각 output file들(최신버전)의
                        path, nb_elements가 기록된 dict를 모은 리스트
        casting_list: 캐스팅된 에셋의 asset_id와 nb_elements가 기록된 dict가 모인 리스트
        """
        file_dict_list = []
        self._shot = gazu.entity.get_entity(self._task['entity_id'])
        casting_list = gazu.casting.get_shot_casting(self._shot)
        for casting in casting_list:
            file_dict_list = self.get_kitsu_path(casting)
            for file_dict in file_dict_list:
                self.load_output(file_dict['path'])

    def get_undistortion_img(self):
        """
        _shot에 소속된 task type이 Matchmove고,
        ouput type이 Undistortion_img인 output file을 찾는 매서드

        Returns:
            str: 마지막 언디스토션 이미지가 저장된 path. padding을 여기서 추출해야 하려나 싶다.
        """
        undi_path = gazu.files.build_entity_output_file_path(self._shot, 'Undistortion_img', 'Matchmove')
        full_path = undi_path + '.jpg'

        return full_path

    def get_camera(self):
        """
        _shot에 소속된 task type이 Matchmove고,
        ouput type이 Camera인 output file을 찾는 매서드

        Returns:
            str: 카메라(fbx) 아웃풋 파일이 저장된 path
        """
        camera_files = gazu.files.get_last_output_files_for_entity(self._shot, 'Camera', 'Matchmove')
        camera_path = gazu.files.build_entity_output_file_path(self._shot, 'Camera', 'Matchmove')
        full_path = camera_path + '.' + camera_files[0]['representation']

        return full_path

    def connect_image(self, undi_path, camera):
        """
        import한 언디스토션 이미지(아웃풋 파일) 시퀀스와 camera를 연결시켜주는 매서드
        카메라가 바라보는 방향에 언디스토션 이미지가 뜨고,
        카메라의 움직임에 따라 감
        카메라에 이미지 연결 후 시퀀스 옵션을 True로 해서 이미지가 영상처럼 넘어가게 함

        Args:
            undi_path(str): 확장자까지 포함된 마지막 언디스토션 이미지의 파일경로
            camera(str): 카메라 파일의 경로
        """
        image_plane = mc.imagePlane(c=camera)
        mc.setAttr(image_plane[0]+'.imageName', undi_path, type='string')
        mc.setAttr(image_plane[0]+'.useFrameExtension', True)

    def import_cam_seq(self):
        """
        샷에 소속된 언디스토션 시퀀스를 찾고(get_undistort_img)
        샷에 소속된 카메라 output file도 찾아서(get_camera)
        모두 import한 뒤, 언디스토션 시퀀스를 카메라와 연결시키는(connect_image) 매서드
        """
        undi_seq_path = self.get_undistortion_img()
        camera_path = self.get_camera()
        self.connect_image(undi_seq_path, camera_path)

    def save_working_file(self, path, representation):
        """
        마야 내에서 저장 경로와 저장 형식을 선택해 작업한 씬 파일을 저장하는 매서드

        Args:
            path(str): 저장할 경로 + 이름
            representation(str): "ma"또는 "mb"

        Returns:

        """
        if representation == "ma":
            mc.file(rename=path + ".ma")
        elif representation == "mb":
            mc.file(rename=path + ".mb")
        mc.file(save=True, type=representation)

    def export_preview(self, path, comment):
        """
        output file의 용량을 줄여서 preview file을 저장하는 매서드

        Args:
            path(str): _preview와 확장자를 붙인 전체 경로
            comment(str): 프리뷰 파일에 대한 comment
        """
        # preview = gazu.task.create_preview(self._task, comment=comment)
        # gazu.task.upload_preview_file(preview, path)

    def export_output_file(self, path):
        """
        작업한 파일을 플레이블라스트 시퀀스로 저장하는 매서드

        Args:
            path(str): output file 시퀀스를 저장할 경로 + 이름
        """
        # 디폴트 카메라 필터링
        startup_cameras = []
        all_cameras = mc.ls(type='camera', l=True)
        for camera in all_cameras:
            if mc.camera(mc.listRelatives(camera, parent=True)[0], startupCamera=True, q=True):
                startup_cameras.append(camera)
        custom_camera = list(set(all_cameras) - set(startup_cameras))

        # 카메라가 바라보는 플레이블라스트 저장 (패딩이 자동으로 붙는지 확인 필요)
        mc.lookThru(custom_camera[0])
        mc.playblast(
            format='image',
            filename=path,
            sequenceTime=False,
            clearCache=True, viewer=True,
            showOrnaments=True,
            fp=4, percent=50,
            compression="jpg",
            quality=100
        )

    # ----------------------------- publish -----------------------------

    def select_software(self, num=0):
        """
        테스크에 working file을 생성하기 위해, 작업에 사용한 소프트웨어를 선택하는 매서드

        Args:
            num(int): 소프트웨어 목록의 인덱스 번호
        """
        software_list = gazu.files.all_softwares()

        print('\n#### software list ####')
        pp.pprint(software_list)

        self._software = software_list[num]

    def select_output_type(self, num=0):
        """
        테스크에 output file을 처음 생성할 경우, 필요한 output type을 선택하는 매서드

        Args:
            num(int): output type 목록의 인덱스 번호
        """
        output_type_list = gazu.files.all_output_types_for_entity(self._shot['id'])

        print('\n#### output type list ####')
        pp.pprint(output_type_list)

        self._output_type = output_type_list[num]

    def publish_file_data(self, comment):
        """
        working file, output file 데이터를 생성하고 Kitsu에 publish하는 매서드
        Kitsu에 워킹 파일과 아웃풋 파일에 대한 정보를 먼저 기록한 뒤,
        폴더를 생성하기 위한 path를 build 한다.

        Args:
            comment(str): working file, output file에 대한 설명
        """
        # 테스크에 대한 워킹/아웃풋 파일 새로 생성
        # person은 user 또는 선택한 person(자신)
        # Layout 팀에서는 working file이 여러개 안 나옴. output file도 여러개 안 나옴(리비전만 올라감)

        # working file 생성
        # 테스크 하나에 워킹 파일이 여러개일 수는 없음. 리비전만 올라감(이름이 같으면 자동으로..)
        working_file_list = gazu.files.get_working_files_for_task(self._task['id'])
        if working_file_list is []:
            # working file 없으면 소프트웨어 선택해서 새로 생성
            self.select_software(0)
            self._working_file = gazu.files.new_working_file(self._task['id'],
                                                             software=self._software['id'],
                                                             comment=comment,
                                                             person=self._person)
        else:
            # 이미 있으면 기존 정보 계승하고 리비전만 올림
            old_working = working_file_list[0]
            self._software = old_working['software_id']
            self._working_file = gazu.files.new_working_file(self._task['id'],
                                                             software=self._software,
                                                             comment=comment,
                                                             person=self._person)

        # output file 생성
        # 워킹 파일 하나에 아웃풋은 여러개 나올 수 있지만 레이아웃은 아님
        output_file_list = gazu.files.get_last_output_files_for_entity(self._shot['id'],
                                                                       task_type=self._task['task_type'])
        if output_file_list is []:
            # 샷에 선택한 아웃풋 타입의 output file이 없으면 타입 선택해서 새로 생성
            self.select_output_type(0)
            self._output_file = gazu.files.new_entity_output_file(self._shot['id'],
                                                                  self._output_type['id'],
                                                                  self._task['task_type'],
                                                                  comment=comment,
                                                                  working_file=self._working_file,
                                                                  person=self._person,
                                                                  representation=self._software[
                                                                      'file_extension'])
        else:
            # 샷에 선택한 아웃풋 타입의 output file이 이미 있으면 정보 계승함
            old_output = output_file_list[0]
            self._output_type = old_output['output_type_id']
            self._output_file = gazu.files.new_entity_output_file(self._shot['id'],
                                                                  self._output_type,
                                                                  self._task['task_type'],
                                                                  comment=comment,
                                                                  working_file=self._working_file,
                                                                  person=self._person,
                                                                  revision=old_output['revision'],
                                                                  representation=old_output['representation'])

        # 마야에서 작업한 파일을 저장하기 위해 폴더 패스 build
        self._working_path = gazu.files.build_working_file_path(self._task['id'],
                                                                software=self._software,
                                                                revision=self._working_file['revision'])
        self._output_path = gazu.files.build_entity_output_file_path(self._shot['id'],
                                                                     self._output_type,
                                                                     self._task['task_type'],
                                                                     representation=self._output_file['representation'],
                                                                     revision=self._output_file['revision'] + 1,
                                                                     nb_elements=self._output_file['nb_elements'])

    def make_folder_tree(self, path):
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
                self.make_folder_tree(parent)

    def upload_files(self, path, comment, file_type):
        """
        작업한 working file과 task에 대한 preview file을 Kitsu에 업로드하는 매서드

        Args:
            path(str): working file 또는 output file의 확장자를 제외한 path
            comment(str): working file, preview file에 대한 comment
            file_type(dict): working file 또는 preview file과 동일한 output file의 딕셔너리
        """
        if file_type == self._working_file:
            full_path = path + '.' + self._software['file_extension']
            gazu.files.upload_working_file(file_type, full_path)
        elif file_type == self._output_file:
            full_path = path + '_preview.' + file_type['representation']
            self.export_preview(full_path, comment)

    def save_real_data(self):
        """
        build된 패스에 맞추어 폴더 트리를 생성하고(make_floder_tree), 파일을 저장하는 매서드
        저장 후에는 Kitsu에 working file과 preview file을 업로드한다(upload_files)
        """
        #  build 된 패스(확장자 없는 파일명까지 포함)에서 파일명을 잘라낸 패스를 만들고 폴더 생성
        path_work = os.path.dirname(self._working_path)
        path_out = os.path.dirname(self._output_path)
        self.make_folder_tree(path_work)
        self.make_folder_tree(path_out)

        # 마야에서 각 폴더에 save
        self.save_working_file(self._working_path, self._software['file_extension'])
        self.export_preview(self._output_path, self._output_file['comment'])
        self.export_output_file(self._output_path)

        # Kitsu에 preview, working file 업로드
        self.upload_files(self._working_path, self._working_file['comment'], self._working_file)
        self.upload_files(self._output_path, self._output_file['comment'], self._output_file)


def main():
    save = ImportThings()
    save.project = "NetfilxAcademy"
    save.person = "Youngbin Park"
    save.select_task(0)


if __name__ == "__main__":
    main()
