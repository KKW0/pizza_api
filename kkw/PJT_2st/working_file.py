import gazu
import os
import pprint as pp
from publish import PublishThings

class Maya_Option(object):
    gazu.client.set_host("http://192.168.3.116/api")
    gazu.log_in("pipeline@rapa.org", "netflixacademy")
# self.maya = MayaThings()
    self.pub = PublishThings()
    self._project = None
    self._shot = None
    self._task = None

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
        open_proj = gazu.project.all_open_projects()
        name_list = []
        for proj in open_proj:
            name_list.append(proj['name'])
        if value not in name_list:
            raise ValueError("오픈 상태인 프로젝트명을 입력해주세요.")
        else:
            self._project = gazu.project.get_project_by_name(value)

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
        gazu.files.update_project_file_tree(self.project, tree)

    def select_task(self, num=0):
        """
        수행할 task를 선택하는 매서드
        task는 선택한 person 또는 user에 assign되어 있어야 하고, 상태가 Todo여야 한다.
        선택한 task에 기반하여 shot을 추출해 저장한다.

        Args:
            num(int): task list의 인덱스 번호
        """
        task_list = []
        task_list_user = gazu.user.all_tasks_to_do()
        for task in task_list_user:
            if task['project_id'] == self.project['id'] \
                    and task['task_status_name'] == 'Todo':
                task_list.append(task)

        print('\n#### task list ####')
        pp.pprint(task_list)

        self._task = task_list[num]
        self._shot = gazu.entity.get_entity(self._task['entity_id'])

    def _get_kitsu_path(self, casting):
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
        asset = gazu.asset.get_asset(casting['id'])
        output_file_list = gazu.files.get_last_output_files_for_entity(asset)
        for out_file in output_file_list:
            # 각 output file의 패스를 생성하고, 리스트에 append
            out_path = gazu.files.build_entity_output_file_path(asset,
                                                                out_file['output_type_id'],
                                                                out_file['task_type_id'],
                                                                revision=out_file['revision'])
            path = out_path + '.' + out_file['representation']
            file_dict['path'] = path
            file_dict['nb_elements'] = out_file['nb_elements']
            file_list.append(file_dict)

        return file_list

    # def import_casting_asset(self):
    #     """
    #     수행중인 테스크(샷)에 캐스팅된 에셋의 저장위치를 모두 추출하여 마야에 import 하는 매서드
    #     output file의 각각의 확장자 포함된 패스를 추출하고(get_kitsu_path),
    #     추출한 패스를 기반으로 마야에 import 한다.(load_output)
    #
    #     file_dict_list: 에셋에 있는 각 output file들(최신버전)의
    #                     path, nb_elements가 기록된 dict를 모은 리스트
    #     casting_list: 캐스팅된 에셋의 asset_id와 nb_elements가 기록된 dict가 모인 리스트
    #     """
    #     file_dict_list = []
    #     casting_list = gazu.casting.get_shot_casting(self._shot)
    #     for casting in casting_list:
    #         file_dict_list = self._get_kitsu_path(casting)
    #         for file_dict in file_dict_list:
    #             self.maya.load_output(file_dict['path'])

    def run_program(self, comment):
        """
        프로그램을 구동하는 매서드

        Args:
            comment(str): working/output/preview file에 대한 커밋 내용
        """
        self.select_task()
        # 유저에게 할당되고, 프로젝트에 속한 테스크 선택(0번째), 테스크가 속한 샷 추출
        # self.import_casting_asset()
        # # 샷에 캐스팅된 에셋을 마야에 모두 import
        # self.maya.import_cam_seq(self._shot)
        # # 샷의 카메라와 언디스토션 이미지를 마야에 import하고 둘을 연결
        self.pub.publish_file_data(self._shot, self._task, comment=comment)
        # Kitsu에 저장한 working, output file 데이터 퍼블리싱
        self.pub.save_publish_real_data(self._shot, self._task, comment=comment)
        # 폴더 트리에 working, output, preview 파일 저장하고 Kitsu에 업로드


# def main():
#     mm = SetThings()
#     mm.project = "jeongtae"
#     mm.run_program("This is like commit")
#
#
# main()