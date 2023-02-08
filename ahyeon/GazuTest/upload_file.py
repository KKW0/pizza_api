import os
import gazu
import pprint as pp


class MakeKitsuTree:
    '''
    dot = gazu.task.get_task_type_by_name(".")
    projects = gazu.project.all_projects()
    gazu.task.remove_task_type(dot)
    오류 발생!!!!!! 삭제가 안됨!!!!!!!!!
    '''

    def __init__(self):
        gazu.client.set_host("http://192.168.3.116/api")
        gazu.set_event_host("http://192.168.3.116")
        gazu.log_in("pipeline@rapa.org", "netflixacademy")
        # set host and log in

        self._project = None
        self._asset = None
        self._episode = None
        self._sequence = None
        self._shot = None
        self._all_task_types = None
        self._tasks_for_shot = None
        self._tasks_for_asset = None
        self._path = os.getcwd()

    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, value):
        self._project = gazu.project.get_project_by_name(value)

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, value):
        self._sequence = gazu.shot.get_sequence_by_name(self.project, value)

    @property
    def shot(self):
        return self._shot

    @shot.setter
    def shot(self, value):
        self._shot = gazu.shot.get_shot_by_name(self._sequence, value)

    def make_new_kitsu_tree(self):
        human = gazu.asset.new_asset_type('Human')
        dog = gazu.asset.new_asset_type('Dog')
        # Set New asset type

        all_tasks = gazu.task.all_task_types()
        for task_dict in all_tasks:
            if 'Puppy' or 'Kitty' or 'Dear' == task_dict['name']:
                puppy = gazu.task.get_task_type_by_name("Puppy")
                kitty = gazu.task.get_task_type_by_name("Kitty")
                dear = gazu.task.get_task_type_by_name("Dear")
            else:
                puppy = gazu.task.new_task_type('Puppy', color='#00FF01')
                kitty = gazu.task.new_task_type('Kitty', color='#00FF01')
                dear = gazu.task.new_task_type('Dear', color='#00FF01', entity='Shot')
        # Set New task type for asset, shot

        all_status = gazu.task.all_task_statuses()
        for status in all_status:
            if 'Good' or 'Bad' in status['name']:
                good = gazu.task.get_task_status_by_name("Good")
                bad = gazu.task.get_task_status_by_name("Bad")
            else:
                good = gazu.task.new_task_status("Good", "good", color='#00FF00')
                bad = gazu.task.new_task_status("Bad", "bad", color='#00FF01')
        # Set New task status

        project = gazu.project.new_project("A_project", "featurefilm", asset_types=[dog, human],
                                           task_types=[puppy, kitty, dear], task_statuses=[good, bad])
        # Set New project

        first_walk = gazu.shot.new_episode(project, "First Walk")
        second_walk = gazu.shot.new_episode(project, "Second Walk")
        # Set New episode in project

        my_dog = gazu.shot.new_sequence(project, "My Dog", episode=first_walk)
        your_dog = gazu.shot.new_sequence(project, "Your Dog", episode=first_walk)
        # Set New sequence in episode

        shot_datadict = {
            'Description': 'This shot is for filming Thomas\'s tail',
            'extra_data': 'shot data'}
        # Set New extra data for shot

        tail = gazu.shot.new_shot(project, my_dog, "tail", frame_in=1, frame_out=10,
                                  data=shot_datadict)
        tail2 = gazu.shot.new_shot(project, my_dog, "tail2", frame_in=1, frame_out=10,
                                   data=shot_datadict)
        # Set New shot in project, seq

        gazu.task.new_task(tail, dear, task_status=good, name='first task')
        # Set New task in shot as task type

        thomas_data = {
            'birth': '2017-05-17',
            'adoption': '2018-02-28',
            'color': 'blue merle'}
        # Set New extra data for asset

        thomas = gazu.asset.new_asset(project, dog, 'Thomas', description="He is very handsome dog",
                                      extra_data=thomas_data, episode=first_walk)
        # Set New asset

        gazu.task.new_task(thomas, puppy, task_status=good, name='make walk')
        # Set New task in asset as task type

        # Set File Tree of the project
        tree = {
            "working": {
                "mountpoint": "/mnt/pipeline/personal/ahyeonJo",
                "root": "kitsu",
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
                "mountpoint": "/mnt/pipeline/personal/ahyeonJo",
                "root": "kitsu",
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
        gazu.files.update_project_file_tree(project, tree)

    def print_info(self):
        print("\n### project info ###")
        pp.pprint(self._project)
        # get project info

        sequences = gazu.shot.all_sequences_for_project(self._project)
        print("\n### sequences info ###")
        pp.pprint(sequences)

        shots = gazu.shot.all_shots_for_project(self._project)
        print("\n### shots info ###")
        pp.pprint(shots)

        self._asset = gazu.asset.all_assets_for_project(self._project)
        print("\n### assets info ###")
        pp.pprint(self._asset)

        self._all_task_types = gazu.task.all_task_types_for_project(self.project)
        print("\n### task_types info of A_project ###")
        pp.pprint(self._all_task_types)

        self._tasks_for_shot = gazu.task.all_tasks_for_shot(shots[0])
        print("\n### tasks info of thomas shot ###")
        pp.pprint(self._tasks_for_shot)

        self._tasks_for_asset = gazu.task.all_tasks_for_asset(self._asset[0])
        print("\n### tasks info of thomas asset ###")
        pp.pprint(self._tasks_for_asset)

    def make_working_file(self):
        # maya = gazu.files.new_software("Maya", "maya", "ma")
        maya = gazu.files.get_software_by_name("Maya")
        print("\n### software info of maya ###")
        pp.pprint(maya)
        # working = gazu.files.new_working_file(self._tasks_for_asset[0],
        #                                       name="maya working file", software=maya,
        #                                       comment="This is for test")
        print("\n### working files info for 'make walk' task ###")
        # pp.pprint(working)
        working_file = gazu.files.get_working_files_for_task(self._tasks_for_asset[0])
        pp.pprint(working_file)
        path = gazu.files.build_working_file_path(self._tasks_for_asset[0], name="working file path",
                                                  software=maya)
        print("\n### working file path for 'maya working file' ###")
        pp.pprint(path)
        # Make new software info, working file info and path

        dir_path_list = path.split('/')[:-1]
        dir_path = '/'.join(dir_path_list)
        os.makedirs(dir_path, exist_ok=True)
        # Make local folders

        # gazu.files.upload_working_file(working_file[0], path+"."+maya['file_extension']')
        gazu.files.download_working_file(working_file[0], file_path=path+'_down'+"."+maya['file_extension'])

        return working_file[0]

    def make_output_file(self):
        working = self.make_working_file()
        # maya_output = gazu.files.new_output_type("Maya Output Type", "maya output")
        maya_output = gazu.files.get_output_type_by_name("Maya Output Type")
        task_types = gazu.task.all_task_types_for_asset(self._asset[0])
        # output = gazu.files.new_entity_output_file(self._asset[0], maya_output, task_types[0],
        #                                            comment="output file test", working_file=working,
        #                                            name="maya output file", representation="ma")
        output = gazu.files.all_output_files_for_entity(self._asset[0], maya_output, task_types[0],
                                                        'maya output file')
        print("\n### output file info for 'maya output file' ###")
        file = gazu.files.get_output_file(output[0]['id'])
        pp.pprint(file)
        path = gazu.files.build_entity_output_file_path(self._asset[0], maya_output, task_types[0],
                                                        name="output file path", representation="ma")
        print("\n### output file path for 'maya output file' ###")
        pp.pprint(path)
        # Make new output file info and path related with working file

        dir_path_list = path.split('/')[:-1]
        dir_path = '/'.join(dir_path_list)
        os.makedirs(dir_path, exist_ok=True)
        # Make local folders

    def make_preview_file(self):
        good = gazu.task.get_task_status_by_name("Good")
        path = '/mnt/project/pizza/shots/jt_seq/jt0010/layout/output/play_test.mov'
        path2 = '/home/rapa/사진/스크린샷, 2023-01-11 14-15-59.png'
        comment = gazu.task.add_comment(self._tasks_for_asset[0], task_status=good,
                                        comment="task comment")
        # preview = gazu.task.create_preview((self._tasks_for_asset[0]), comment=comment)
        # # Make new preview file model
        # # ??? upload와 차이가 뭔지 모르겠음
        preview = gazu.files.get_all_preview_files_for_task(self._tasks_for_asset[0])
        print("\n### all preview files info for 'make walk' ###")
        pp.pprint(preview)

        gazu.task.upload_preview_file(preview[0], path)
        gazu.task.add_preview(self._tasks_for_asset[0], comment, preview_file_path=path2)
        gazu.task.set_main_preview(preview[1])
        # Upload preview file


def main():
    kt = MakeKitsuTree()
    kt.make_new_kitsu_tree()
    kt.project = "A_project"
    kt.sequence = "My Dog"
    kt.shot = "tail"
    #
    # kt.print_info()
    # kt.make_working_file()
    # kt.make_output_file()
    # kt.make_preview_file()
    pp.pprint(kt.make_output_file())


if __name__ == "__main__":
    main()