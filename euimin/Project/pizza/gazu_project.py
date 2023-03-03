import gazu
import pprint as pp


class MakeKitsuFiles:
    """
    Kitsu에 트리 구조를 가진 프로젝트를 생성하고 그에 맞춘 폴더 트리를 만드는 클래스
    워킹 파일, 아웃풋 파일, 프리뷰 파일의 업로드와 다운로드 가능
    """

    def __init__(self):
        """
        클래스에서 쓰일 프라이빗 변수를 정의하는 매서드
        """

        self._project = None
        self._sequence = None
        self._shot = None
        self._asset = None

    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, value):
        """
        self._project에 지정된 이름의 프로젝트 딕셔너리를 할당하는 세터

        Args:
            value(str): 정보를 얻길 원하는 프로젝트 이름
        """
        self._project = gazu.project.get_project_by_name(value)

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, value):
        """
        self._sequence에 지정된 이름의 시퀀스 딕셔너리를 할당하는 세터

        Args:
            value(str): 정보를 얻길 원하는 시퀀스 이름
        """
        self._sequence = gazu.shot.get_sequence_by_name(self.project, value)

    @property
    def shot(self):
        return self._shot

    @shot.setter
    def shot(self, value):
        """
        self._shot에 지정된 이름의 샷 딕셔너리를 할당하는 세터

        Args:
            value(str): 정보를 얻길 원하는 샷 이름
        """
        self._shot = gazu.shot.get_shot_by_name(self.sequence, value)

    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, value):
        """
        self._shot에 지정된 이름의 에셋 딕셔너리를 할당하는 세터

        Args:
            value(self): 정보를 얻길 원하는 에셋 이름
        """
        self._asset = gazu.asset.get_asset_by_name(self.project, value)

    def update_file_tree(self):
        gazu.files.update_project_file_tree(self.project, {
            "working": {
                "mountpoint": "/mnt/personal",
                "root": "euiminLee",
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
                "mountpoint": "/mnt/personal",
                "root": "euiminLee",
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
        })

    def print_info(self):
        print("\n### project info ###")
        pp.pprint(self.project)

        sequences = gazu.shot.all_sequences_for_project(self.project)
        print("\n### sequences info ###")
        pp.pprint(sequences)

        shots = gazu.shot.all_shots_for_project(self.project)
        print("\n### shots info ###")
        pp.pprint(shots)

        assets = gazu.asset.all_assets_for_project(self.project)
        print("\n### assets info ###")
        pp.pprint(assets)

        self._all_task_types = gazu.task.all_task_types_for_project(self.project)
        print("\n### task_types info of selected project ###")
        pp.pprint(self._all_task_types)

        tasks_for_shot = gazu.task.all_tasks_for_shot(self.shot)
        print("\n### tasks info of selected shot ###")
        pp.pprint(tasks_for_shot)

        tasks_for_asset = gazu.task.all_tasks_for_asset(self.asset)
        print("\n### tasks info of selected asset ###")
        pp.pprint(tasks_for_asset)

    # def make_working_file(self):
    #     # maya = pizza.files.new_software("Maya", "maya", "ma", ['mb', 'fbx'])
    #     maya = pizza.files.get_software_by_name("Maya")
    #     print("\n### software info of maya ###")
    #     pp.pprint(maya)
    #     # working = pizza.files.new_working_file(self._tasks_for_asset[0],
    #     #                                       name="maya working file", software=maya,
    #     #                                       comment="This is for test")
    #     print("\n### working files info for 'make walk' task ###")
    #     # pp.pprint(working)
    #     tasks = pizza.task.all_tasks_for_asset(self.asset)
    #     working_file = pizza.files.get_working_files_for_task(tasks[0])
    #     pp.pprint(working_file)
    #     path = pizza.files.build_working_file_path(tasks[0], name="working file path",
    #                                               software=maya)
    #     print("\n### working file path for 'maya working file' ###")
    #     pp.pprint(path)
    #     # Make new software info, working file info and path
    #
    #     dir_path_list = path.split('/')[:-1]
    #     dir_path = '/'.join(dir_path_list)
    #     os.makedirs(dir_path, exist_ok=True)
    #     # Make local folders
    #
    #     # pizza.files.upload_working_file(working_file[0], path+"."+maya['file_extension']')
    #     pizza.files.download_working_file(working_file[0], file_path=path + '_down' + "." + maya['file_extension'])
    #
    #     return working_file[0]
    #
    # def make_output_file(self):
    #     working = self.make_working_file()
    #     # maya_output = pizza.files.new_output_type("Maya Output Type", "maya output")
    #     maya_output = pizza.files.get_output_type_by_name("Maya Output Type")
    #     task_types = pizza.task.all_task_types_for_asset(self._asset[0])
    #     # output = pizza.files.new_entity_output_file(self._asset[0], maya_output, task_types[0],
    #     #                                            comment="output file test", working_file=working,
    #     #                                            name="maya output file", representation="ma")
    #     output = pizza.files.all_output_files_for_entity(self._asset[0], maya_output, task_types[0],
    #                                                     'maya output file')
    #     print("\n### output file info for 'maya output file' ###")
    #     file = pizza.files.get_output_file(output[0]['id'])
    #     pp.pprint(file)
    #     path = pizza.files.build_entity_output_file_path(self._asset[0], maya_output, task_types[0],
    #                                                     name="output file path", representation="ma")
    #     print("\n### output file path for 'maya output file' ###")
    #     pp.pprint(path)
    #     # Make new output file info and path related with working file
    #
    #     dir_path_list = path.split('/')[:-1]
    #     dir_path = '/'.join(dir_path_list)
    #     os.makedirs(dir_path, exist_ok=True)
    #     # Make local folders
    #
    # def make_preview_file(self):
    #     good = pizza.task.get_task_status_by_name("Good")
    #     path = '/mnt/project/pizza/shots/jt_seq/jt0010/layout/output/play_test.mov'
    #     path2 = '/home/rapa/사진/스크린샷, 2023-01-11 14-15-59.png'
    #     comment = pizza.task.add_comment(self._tasks_for_asset[0], task_status=good,
    #                                     comment="task comment")
    #     # preview = pizza.task.create_preview((self._tasks_for_asset[0]), comment=comment)
    #     # # Make new preview file model
    #
    #     preview = pizza.files.get_all_preview_files_for_task(self._tasks_for_asset[0])
    #     print("\n### all preview files info for 'make walk' ###")
    #     pp.pprint(preview)
    #
    #     pizza.task.upload_preview_file(preview[0], path)
    #     pizza.task.add_preview(self._tasks_for_asset[0], comment, preview_file_path=path2)
    #     pizza.task.set_main_preview(preview[1])
    #     # Upload preview file



def main():
    project = 'Test_Euimin'
    sequence = "My_seq"
    shot = "My_shot"

    kt = MakeKitsuFiles()
    kt.update_file_tree()

    kt.print_info()
    # kt.update_file_tree()


if __name__ == "__main__":
    main()