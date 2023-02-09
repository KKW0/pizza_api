#coding:utf8
import os
import gazu
import pprint as pp
import maya.cmds as mc
from maya_test2 import MayaLayout


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
        gazu.set_event_host("http://192.168.3.116")
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
            value:

        Returns:

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
            value:

        Returns:

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
        파일 트리를 업데이트하는 매서드

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
            num: task list의 인덱스 번호
        """
        task_list_user = gazu.task.all_tasks_for_person(self.person)
        # user에게 테스크가 충분히 할당되어 있다면 gazu.user.all_tasks_to_do() 로 대체
        task_list = []
        for task in task_list_user:
            if task['project_id'] == self.project['id'] \
                    and task['task_status_name'] == 'Todo':
                task_list.append(task)
        self._task = task_list[num]

    def get_kitsu_path(self, casting):
        """
        캐스팅된 에셋의 최신 아웃풋 파일들의 패스 리스트를 추출하는 매서드

        Args:
            casting(dict): 샷에 캐스팅된 에셋의 간략한 정보가 담긴 dict

        Returns:
            list: 아웃풋 파일들의 패스(확장자 포함), 개수가 담긴 dict를 수집한 리스트
        """
        file_list = []
        file_dict = {
            'path': "",
            'nb_elements': 0,
            'representation': ''
        }
        asset = gazu.asset.get_asset(casting['asset_id'])
        output_file_list = gazu.files.get_last_output_files_for_entity(asset)
        for out_file in output_file_list:
            # 각 output file의 패스를 생성하고, 리스트에 append
            out_path = gazu.files.build_entity_output_file_path(asset, out_file['output_type'],
                                                                out_file['task_type'])
            path = out_path + '.' + out_file['representation']
            file_dict['path'] = path
            file_dict['nb_elements'] = out_file['nb_elements']
            file_dict['representation'] = out_file['representation']
            file_list.append(file_dict)

        return file_list

    # ----------------------------- maya -----------------------------

    def load_data(self, path):
        """
        마야에서 샷에 캐스팅된 에셋들을 import하는 매서드

        Args:
            path: 파일명까지 포함된 에셋의 아웃풋 파일의 패스

        Returns:
            list: import한 파일이 가지고 있는 요소(트랜스폼, 쉐입 등등)들의 리스트

        """
        imported_file_list = mc.file(
            path, i=1, ignoreVersion=1,
            mergeNamespacesOnClash=0, importTimeRange="combine",
            loadReferenceDepth="all",
            returnNewNodes=True
        )

        return imported_file_list

    def filter_elements(self, element_list):
        """
        아웃풋 파일에 포함된 요소들 중 트랜스폼과 매쉬만 걸러내어,
        각각의 이름을 담은 리스트를 반환하는 매서드

        Args:
            element_list(list): 아웃풋 파일에 포함된 모든 요소들

        Returns:
            list(cam_list): 아웃풋 파일에 포함된 카메라(트랜스폼) 이름. 하나임
            list(mesh_list): 아웃풋 파일에 포함된 매쉬 이름들

        """
        cam_list = []
        mesh_list = []
        for element in element_list:
            if mc.objectType(element) == "camera":
                cam = mc.listRelatives(element, p=1)
                cam_list.append(cam)
            elif mc.objectType(element) == "mesh":
                mesh = mc.listRelatives(element, p=1)
                mesh_list.append(mesh)

        return cam_list, mesh_list

    def get_casting(self):
        """
        수행중인 테스크(샷)에 캐스팅된 에셋의 패스들을 모두 추출하는 매서드
        get_kitsu_path로 각각의 패스를 추출하고,
        추출한 패스를 기반으로 마야에 import 한다.(self.load_data)
        그리고 에셋의 element를 필터링하여 리턴한다.(filter_element)
        """
        path_list = []
        element_list = []
        self._shot = gazu.entity.get_entity(self._task['entity_id'])
        casting_dict = gazu.casting.get_shot_casting(self._shot)
        for casting in casting_dict:
            path_list = self.get_kitsu_path(casting)
            for path in path_list:
                element_list = (self.load_data(path['path']))
                cam_list, mesh_list = self.filter_elements(element_list)
                if path['representation'] == 'jpg':
                    # 아웃풋 파일이 시퀀스 이미지면 캠과 연결시켜준다.
                    self.connect_image(path, cam_list[0])

    def connect_image(self, path, camera):
        """
        언디스토션 이미지(아웃풋 파일) 시퀀스를 cam에 연결시켜주는 매서드
        카메라가 바라보는 방향에 언디스토션 이미지가 뜨고,
        카메라의 움직임에 따라 감
        카메라에 이미지 연결 후 시퀀스 옵션을 True로 해서 이미지가 영상처럼 넘어가게 함

        Args:
            path(str): 확장자까지 포함된 언디스토션 이미지 파일경로
            camera(str): 캐스팅에 있는 카메라의 이름
        """
        image_plane = mc.imagePlane(c=camera)
        mc.setAttr('%s.imageName' % image_plane[0], path, type='string')
        mc.setAttr("%s.useFrameExtension" % image_plane[0], True)

    def save_working_file(self):
        pass

    def export_output_file(self):
        pass

    # ----------------------------- publish -----------------------------

    def get_informations(self):
        """
        working file, output file, casting을 생성할 때
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
        dir_path_list = self._working_path.split('/')[:-1]
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
