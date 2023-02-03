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

    def make_new_kitsu_tree(self):
        human = gazu.asset.new_asset_type('Human')
        dog = gazu.asset.new_asset_type('Dog')
        # Set New asset type

        puppy = gazu.task.new_task_type('Puppy', color='#00FF01')
        kitty = gazu.task.new_task_type('Kitty', color='#00FF01')
        dear = gazu.task.new_task_type('Dear', color='#00FF01', entity='Shot')
        # Set New task type for asset, shot

        good = gazu.task.new_task_status("Good", "g", color='#00FF00')
        bad = gazu.task.new_task_status("Bad", "b", color='#00FF01')
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

        gazu.task.new_task(tail, dear, name='first task')
        # Set New task in shot as task type

        thomas_data = {
            'birth': '2017-05-17',
            'adoption': '2018-02-28',
            'color': 'blue merle'}
        # Set New extra data for asset

        thomas = gazu.asset.new_asset(project, dog, 'Thomas', description="He is very handsome dog",
                                      extra_data=thomas_data, episode=first_walk)
        # Set New asset

        gazu.task.new_task(thomas, puppy, name='make walk')
        # Set New task in asset as task type

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

        assets = gazu.asset.all_assets_for_project(self._project)
        print("\n### assets info ###")
        pp.pprint(assets)

        self._all_task_types = gazu.task.all_task_types_for_shot(shots[0])
        print("\n### task_types info of tail ###")
        pp.pprint(self._all_task_types)

        self._tasks_for_asset = gazu.task.all_tasks_for_asset(shots[0])
        print("\n### tasks info of tail shot ###")
        pp.pprint(self._tasks_for_asset)

        self._tasks_for_shot = gazu.task.all_tasks_for_shot(assets[0])
        print("\n### tasks info of thomas asset ###")
        pp.pprint(self._tasks_for_shot)

    def make_working_file(self):
        working_file = gazu.files.new_working_file(self._tasks_for_shot[0]['id'],
                                                   name="new_working_file", comment="This is for test")
        pp.pprint(working_file)
        # gazu.files.upload_working_file(working_file, self._path+'/'+working_file['name']+
        #                                '.'+working_file['extension'])


def main():
    kt = MakeKitsuTree()
    # kt.make_new_kitsu_tree()
    kt.project("A_project")
    kt.sequence("My Dog")
    kt.shot("tail")

    kt.print_info()
    kt.make_working_file()


if __name__ == "__main__":
    main()

# gazu.task.upload_preview_file(tasks[0]['id'], '/mnt/project/pizza/shots/jt_seq/jt0010/layout/output/play_test.mov')