#coding:utf8
import os
import gazu
import pprint as pp
import maya.cmds as mc


class SaveAsKitsuPath(object):
    """
    선택한 테스크타입에 있는 테스크 중 하나를 선택하고,
    선택한 테스크가 있는 샷에 캐스팅된 에셋 데이터를 가져오고,
    각 에셋의 워킹 파일과 아웃풋 파일 패스를 가져오고,
    작업한 워킹파일과 아웃풋 파일을 폴더 트리에 저장하고,
    Kitsu에 퍼블리싱하고, 워킹 파일을 업로드하는 클래스
    Layout 팀을 위한 api
    """
    def __init__(self):
        gazu.client.set_host("http://192.168.3.116/api")
        gazu.set_event_host("http://192.168.3.116")
        gazu.log_in("pipeline@rapa.org", "netflixacademy")

        self._working_path = None
        self._output_path = None

        # output, working file 만들기 위한 파라미터
        self._project = None
        self._task = None
        self._shot = None
        self._sequence = None
        self._asset = None
        self._asset_type = None
        # self._entity = None
        # # output file의 entity(asset / shot)
        self._software = None
        self._output_type = None
        self._casting_dict = None
        self._casting = None
        # casting된 정보들을 저장하기 위한 딕셔너리

    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, value):
        self._project = gazu.project.get_project_by_name(value)
    #
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

        Args:
            num: task list의 인덱스 번호
        """
        pass

    def get_informations(self):
        """
        working file, output file, casting을 생성할 때
        필요한 데이터들을 추출하는 매서드
        """
        pass

    def get_casting(self):
        """
        수행중인 테스크(샷)에 캐스팅된 에셋의 패스들을 모두 추출하는 매서드
        추출한 패스를 기반으로 마야에 import 한다(self.load_data())
        """
        pass

    def get_kitsu_path(self, num=0):
        pass

    def make_folder_tree(self, path):
        """
        working file, output file을 save/export 하기 위한 실제 폴더를
        생성하는 매서드
        Args:
            path:

        Returns:

        """
        pass

    def load_data(self, file_type):
        """
        마야에서 샷에 캐스팅된 에셋들을 import하는 매서드
        Args:
            file_type:

        Returns:

        """
        pass

    def save_working_file(self):
        pass

    def export_output_file(self):
        pass

    def make_publish_file_data(self):
        pass


def main():
    save_path = SaveAsKitsuPath()
    save_path.project = "A_project"
    print(save_path.project)
    # save_path.sequence = "My Dog"
    # save_path.shot = "tail"
    # save_path.select_task(0)


if __name__ == "__main__":
    main()
