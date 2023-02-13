#coding:utf8
import gazu
import pprint as pp


class SetThings(object):
    def __init__(self):
        self._person = None
        self._project = None

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
        # 또는 세터 없이 그냥 client.get_current_user()

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
        선택한 task에 기반하여 shot을 추출해 저장한다.

        Args:
            num(int): task list의 인덱스 번호
        Returns:
            dict(task): 사용자가 선택한 task의 딕셔너리
            dict(shot): task가 속한 shot의 딕셔너리
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

        task = task_list[num]
        shot = gazu.entity.get_entity(task['entity_id'])

        return task, shot

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
