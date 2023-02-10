#coding:utf8
import os
import gazu
import pprint as pp
import maya.cmds as mc


class SaveAsKitsuPath(object):
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

    # @property
    # def sequence(self):
    #     return self._sequence
    #
    # @sequence.setter
    # def sequence(self, value):
    #     self._sequence = gazu.shot.get_sequence_by_name(self.project, value)
    # @property
    # def shot(self):
    #     return self._shot
    #
    # @shot.setter
    # def shot(self, value):
    #     self._shot = gazu.shot.get_shot_by_name(self.sequence, value)

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
        캐스팅된 에셋의 최신 output file들의 패스 리스트를 추출하는 매서드

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
        casting: 캐스팅된 에셋의 asset_id와 nb_elements가 기록된 dict
        """
        file_dict_list = []
        self._shot = gazu.entity.get_entity(self._task['entity_id'])
        casting_list = gazu.casting.get_shot_casting(self._shot)
        for casting in casting_list:
            file_dict_list = self.get_kitsu_path(casting)
            for file_dict in file_dict_list:
                self.load_output(file_dict['path'])

    def get_undistort_img(self):
        """
        _shot에 소속된 task type이 Matchmove고,
        ouput type이 Undistortion_img인 output file을 찾는 매서드

        Returns:
        """
        return

    def get_camera(self):
        """
        shot에 소속된 task type이 Matchmove고,
        ouput type이 Camera인 output file을 찾는 매서드
        """
        pass

    def connect_image(self, path, camera):
        """
        import한 언디스토션 이미지(아웃풋 파일) 시퀀스와 camera를 연결시켜주는 매서드
        카메라가 바라보는 방향에 언디스토션 이미지가 뜨고,
        카메라의 움직임에 따라 감
        카메라에 이미지 연결 후 시퀀스 옵션을 True로 해서 이미지가 영상처럼 넘어가게 함

        Args:
            path(str): 확장자까지 포함된 언디스토션 이미지 파일경로
            camera(str): 카메라 파일의 경로
        """
        image_plane = mc.imagePlane(c=camera)
        mc.setAttr('%s.imageName' % image_plane[0], path, type='string')
        mc.setAttr("%s.useFrameExtension" % image_plane[0], True)

    def import_cam_seq(self):
        """
        샷에 소속된 언디스토션 시퀀스를 찾고(get_undistort_img)
        샷에 소속된 카메라 output file도 찾아서(get_camera)
        모두 import한 뒤, 언디스토션 시퀀스를 카메라와 연결시키는(connect_image) 매서드
        """

    def save_working_file(self):
        """
        포맷을 받아서 원하는 형식으로 저장하는 매서드
        Args:
            path: 저장할 경로 + 이름
            format: "mayaAscii","mayaBinary" 둘중하나

        Returns:

        """
        # if format == "mayaAscii":다
        #     mc.file(rename = "%s"%path + ".ma")
        # elif format == "mayaBinary":
        #     mc.file(rename = "%s"%path + ".mb")
        # mc.file(save = True, type = format)

    def export_output_file(self):
        pass

    # ----------------------------- publish -----------------------------

    def get_informations(self):
        """
        working file, output file을 생성할 때
        필요한 데이터들을 추출하는 매서드
        """
        pass

    def select_software(self, num=0):
        """
        테스크에 working file을 생성하기 위해, 작업에 사용한 소프트웨어를 선택하는 매서드

        Args:
            num: 소프트웨어 목록의 인덱스 번호
        """
        software_list = gazu.files.all_softwares()

        print('\n#### software list ####')
        pp.pprint(software_list)

        self._software = software_list[num]

    def select_output_type(self, num=0):
        """
        테스크에 output file을 처음 생성할 경우, 필요한 output type을 선택하는 매서드

        Args:
            num: output type 목록의 인덱스 번호
        """
        output_type_list = gazu.files.all_output_types_for_entity(self._shot['id'])

        print('\n#### output type list ####')
        pp.pprint(output_type_list)

        self._output_type = output_type_list[num]

    def edit_path(self, path):
        """
        build 된 패스에서 파일명을 잘라낸 패스를 만들어내는 매서드

        Args:
            path: extension을 제외한 파일명이 포함된 패스

        Returns:
            str: 파일명 부분이 잘린 패스
        """
        dir_path_list = path.split('/')[:-1]
        dir_path = '/'.join(dir_path_list)

        return dir_path

    def make_folder_tree(self, path):
        """
        working file, output file을 save/export 하기 위한 실제 폴더를
        생성하는 매서드

        Args:
            path: 파일명을 제외한 폴더 경로
        """
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            parent = os.path.dirname(path)
            if parent != "/":
                self.make_folder_tree(parent)

    def make_publish_file_data(self, comment):
        """
        working file, output file 데이터를 생성하고 Kitsu에 publish하는 매서드

        Args:
            comment: working file, output file에 대한 설명
        """
        pass


def main():
    save = SaveAsKitsuPath()
    save.project = "NetfilxAcademy"
    save.person = "Youngbin Park"
    # save_path.sequence = "My Dog"
    # save_path.shot = "tail"
    save.select_task(0)


if __name__ == "__main__":
    main()
