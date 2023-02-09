import os
import gazu
import pprint as pp

class MyGazu:
    def __init__(self):
        gazu.client.set_host("http://192.168.3.116/api")
        gazu.log_in("pipeline@rapa.org", "netflixacademy")
        self.project = None
        self.shot = None
        self.seq = None
        self.asset = None
        self.task = None
        self.task_type = None

    def set_project(self, name):
        self.project = gazu.project.get_project_by_name(name)

    def set_shot(self, name):
        self.shot = gazu.shot.get_shot_by_name(self.seq, name)
        pp.pprint(self.shot)

    def set_seq(self, name):
        self.seq = gazu.shot.get_sequence_by_name(self.project, name)
        pp.pprint(self.seq)

    def set_asset(self, name):
        self.asset = gazu.asset.get_asset_by_name(self.project, name)

    def set_task(self, name):
        self.task_type = gazu.task.get_task_type_by_name(name)
        tasks = gazu.task.all_tasks_for_asset(self.asset)
        for task in tasks:
            if task['task_type_name'] == name:
                self.task = task

    def set_preview(self, comment, img):
        comment_dict = gazu.task.add_comment(self.task, {'id': self.task['task_status_id']}, comment)
        gazu.task.add_preview(self.task, comment_dict, preview_file_path=img)

    def new_task(self, name):
        self.task_type = gazu.task.get_task_type_by_name(name)
        self.task = gazu.task.new_task(self.asset, self.task_type)

    def new_task2(self, name):
        tasks = gazu.task.all_tasks_for_shot(self.shot)
        for i in tasks:
            if i.get('task_type_name') == name:
                task = i
        pp.pprint(task2)

    def update_file_tree(self):
        gazu.files.update_project_file_tree(self.project, {
            "working": {
                "mountpoint": "/mnt/project",
                "root": "pizza",
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
                "mountpoint": "/mnt/project",
                "root": "pizza",
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

    def create_tree_dir(self):
        for shot in gazu.shot.all_shots_for_project(self.project):
            for task in gazu.task.all_tasks_for_shot(shot):
                path = os.path.dirname(
                    gazu.files.build_working_file_path(task)
                )
        os.makedirs(path)
        for asset in gazu.asset.all_assets_for_project(self.project):
            for task in gazu.task.all_tasks_for_asset(asset):
                path = os.path.dirname(
                    gazu.files.build_working_file_path(task)
                )
        os.makedirs(os.sep + path)

    def update_working(self):
        for shot in gazu.shot.all_shots_for_project(self.project_name):
            for task in gazu.task.all_tasks_for_shot(shot):
                working_file_path = os.path.dirname(
                    gazu.files.build_working_file_path(task)
                )
                if os.path.exists(working_file_path):
                    print("path exists Working_file_path :", working_file_path)
                    pass
                else:
                    print("Working_file_path :", working_file_path)
                    os.makedirs(working_file_path)

        for asset in gazu.asset.all_assets_for_project(self.project_name):
            for task in gazu.task.all_tasks_for_asset(asset):
                print("asset :", asset['name'])
                print("task :", task['task_type_name'])
                working_file_path = os.path.dirname(
                    gazu.files.build_working_file_path(task)
                )
                if os.path.exists(working_file_path):
                    print("path exists", working_file_path)
                    pass
                else:
                    print("Working_file_path :", working_file_path)
                    os.makedirs(working_file_path)

    def update_output(self, output_type):
        """

        :param output_type:
        :return:
        """
        output = gazu.files.get_output_type_by_name(output_type)
        for shot in gazu.shot.all_shots_for_project(self.project):
            for task in gazu.task.all_tasks_for_shot(shot):
                output_file_path = os.path.dirname(
                    gazu.files.build_entity_output_file_path(shot, output,
                                                             gazu.task.get_task_type_by_name(task['task_type_name']))
                )
                if os.path.exists(output_file_path):
                    print("path exists Output_file_path :", output_file_path)
                    pass
                else:
                    print("Output_file_path :", output_file_path)
                    os.makedirs(output_file_path)

        for asset in gazu.asset.all_assets_for_project(self.project):
            for task in gazu.task.all_tasks_for_asset(asset):
                output_file_path = os.path.dirname(
                    gazu.files.build_entity_output_file_path(asset, output_type,
                                                             gazu.task.get_task_type_by_name(task['task_type_name']))
                )
                if os.path.exists(output_file_path):
                    print("path exists", output_file_path)
                    pass
                else:
                    print("Output_file_path :", output_file_path)
                    os.makedirs(output_file_path)

    def working_publish_for_asset(self, asset, task_type):
        """

        :param asset:
        :param task_type:
        :return:
        """
        pick_asset = gazu.asset.get_asset_by_name(self.project, asset)
        tasks = gazu.task.all_tasks_for_asset(pick_asset)
        # print(task_type)
        for i in tasks:
            # print(i['task_type_name'])
            if task_type == i['task_type_name']:
                task = i
        new_working_file = gazu.files.new_working_file(task)
        working_file_path = os.path.dirname(new_working_file['path'])
        if os.path.exists(working_file_path):
            print("path exists :", working_file_path)
        else:
            print("create working file path :", working_file_path)
            os.makedirs(working_file_path)
        print(new_working_file['path'])

    def working_path_for_asset(self, asset, task_type):
        """

        :param asset:
        :param task_type:
        :return:
        """
        pick_asset = gazu.asset.get_asset_by_name(self.project, asset)
        tasks = gazu.task.all_tasks_for_asset(pick_asset)
        for i in tasks:
            if task_type == i['task_type_name']:
                task = i
        last_revision = gazu.files.get_last_working_file_revision(task)
        all_working_files = gazu.files.get_working_files_for_task(task)
        working_file_path = os.path.dirname(
            gazu.files.build_working_file_path(task, revision=last_revision['revision'] + 1)
        )
        for a in all_working_files:
            print(f'revision : {a["revision"]} \npath : {a["path"]}')
        print(f'Saved working file path : {working_file_path}')

        all_working_files = gazu.files.get_working_files_for_task(task)
        working_file_path = os.path.dirname(
            gazu.files.build_working_file_path(task, revision=last_revision['revision']+1)
        )
        for a in all_working_files:
            print(f'revision : {a["revision"]} \npath : {a["path"]}')
        print(f'Saved working file path : {working_file_path}')

    def get_working_publish_for_shot(self, sequence, shot, t_type):
        """
        :param t_type:
        :param sequence:
        :param shot:
        :return:
        """
        # sequence = gazu.shot.get_sequence_by_name(self.project, self.seq)
        pick_sequence = gazu.shot.get_sequence_by_name(self.project, sequence)
        pick_shot = gazu.shot.get_shot_by_name(pick_sequence, shot)
        tasks = gazu.task.all_tasks_for_shot(pick_shot)
        task = None
        for a in tasks:
            print(a['task_type_name'])
            if a['task_type_name'].lower() == t_type.lower():
                task = a
        new_working_file = gazu.files.new_working_file(task)
        # print(new_working_file)
        working_file_path = os.path.dirname(new_working_file['path'])
        if os.path.exists(working_file_path):
            print("path exists :", working_file_path)
        else:
            print("create working file path :", working_file_path)
            os.mkdir(working_file_path)
        print(new_working_file['path'])

    def get_output_publish_for_shot(self, sequence, shot, output_type, t_type):
        """

        :param t_type:
        :param sequence:
        :param shot:
        :param output_type:
        :return:
        """
        pick_sequence = gazu.shot.get_sequence_by_name(self.project, sequence)
        pick_shot = gazu.shot.get_shot_by_name(pick_sequence, shot)
        # output_type = gazu.files.new_output_type("OBJ", "obj")
        output = gazu.files.get_output_type_by_name("OBJ")
        task_types = gazu.task.all_task_types_for_shot(pick_shot)
        task_type = None
        for a in task_types:
            if a['name'].lower() == t_type.lower():
                task_type = a
        new_output_file = gazu.files.new_entity_output_file(pick_shot, output, task_type, "publish test")
        output_file_path = os.path.dirname(new_output_file['path'])
        if os.path.exists(output_file_path):
            print("path exists :", output_file_path)
        else:
            print("create output file path :", output_file_path)
            os.makedirs(output_file_path)
        print(new_output_file['path'])

        pick_shot = gazu.shot.get_shot_by_name(pick_sequence, shot)
        tasks = gazu.task.all_tasks_for_shot(pick_shot)
        task = None
        for a in tasks:
            if a['task_type_name'].lower() == t_type.lower():
                task = a
        last_revision = gazu.files.get_last_working_file_revision(task)
        all_working_files = gazu.files.get_working_files_for_task(task)
        working_file_path = os.path.dirname(
            gazu.files.build_working_file_path(task, revision=last_revision['revision']+1)
        )
        for a in all_working_files:
            print(f'revision : {a["revision"]} \npath : {a["path"]}')
        print(f'Saved working file path : {working_file_path}')

    def get_working_path_for_shot(self, sequence, shot, t_type):
        """

        :param t_type:
        :param sequence:
        :param shot:
        :return:
        """
        pick_sequence = gazu.shot.get_sequence_by_name(self.project, sequence)
        pick_shot = gazu.shot.get_shot_by_name(pick_sequence, shot)
        tasks = gazu.task.all_tasks_for_shot(pick_shot)
        # pp.pprint(tasks)
        task2 = None
        for a in tasks:
            if a['task_type_name'].lower() == t_type.lower():
                task2 = a
        print(task2)
        last_revision = gazu.files.get_last_working_file_revision(task2)
        print(last_revision)
        all_working_files = gazu.files.get_working_files_for_task(task2)
        working_file_path = os.path.dirname(
            gazu.files.build_working_file_path(task2, revision=last_revision['revision'] + 1)
        )
        for a in all_working_files:
            print(f'revision : {a["revision"]} \npath : {a["path"]}')
        print(f'Saved working file path : {working_file_path}')

    def get_output_path_for_shot(self, sequence, shot, output_type, t_type):
        """

        :param t_type:
        :param sequence:
        :param shot:
        :param output_type:
        :return:
        """
        pick_sequence = gazu.shot.get_sequence_by_name(self.project, sequence)
        pick_shot = gazu.shot.get_shot_by_name(pick_sequence, shot)
        output = gazu.files.get_output_type_by_name(output_type)
        task_types = gazu.task.all_task_types_for_shot(pick_shot)
        task_type = None
        for a in task_types:
            if a['name'].lower() == t_type.lower():
                task_type = a
        last_revision = gazu.files.get_last_entity_output_revision(pick_shot, output, task_type, name='main')
        output_file_path = os.path.dirname(
            gazu.files.build_entity_output_file_path(pick_shot, output, task_type, revision=last_revision+1)
        )
        all_output_files = gazu.files.all_output_files_for_entity(pick_shot, output_type=output, task_type=task_type)
        for a in all_output_files:
            print(f'revision : {a["revision"]} \npath : {a["path"]}')
        print(f'Saved output file path : {output_file_path}')

    def casting_create(self, asset, sequence, shot):
        """

        :param sequence:
        :param asset: asset name
        :param shot: shot name
        :return:
        """
        pick_asset = gazu.asset.get_asset_by_name(self.project, asset)
        pick_sequence = gazu.shot.get_sequence_by_name(self.project, sequence)
        pick_shot = gazu.shot.get_shot_by_name(pick_sequence, shot)
        asset_castings = gazu.casting.get_shot_casting(pick_shot)
        new = {"asset_id": pick_asset['id'], "nb_occurences": 3}
        asset_castings.append(new)
        gazu.casting.update_shot_casting(self.project, pick_shot, casting=asset_castings)

    # def casting_delete(self, asset, sequence, shot):
    #     """
    #
    #     :param asset:
    #     :param sequence:
    #     :param shot:
    #     :return:
    #     """
    #     pick_sequence = gazu.shot.get_sequence_by_name(self.project, sequence)
    #     pick_shot = gazu.shot.get_shot_by_name(pick_sequence, shot)
    #     pick_asset = gazu.asset.get_asset_by_name(self.project, asset)
    #     asset_name = pick_asset['name']
    #     asset_castings = gazu.casting.get_shot_casting(pick_shot)
    #     filtered_assets = [a for a in asset_castings if asset_name != a.get('asset_name')]
    #     gazu.casting.update_shot_casting(self.project, pick_shot, casting=filtered_assets)

    def get_path_for_casting(self, asset):
        """

        :param asset:
        :return:
        """
        pick_asset = gazu.asset.get_asset_by_name(self.project_name, asset)
        cast_in = gazu.casting.get_asset_cast_in(pick_asset)
        for shot in cast_in:
            tasks = gazu.task.all_tasks_for_shot(shot['shot_id'])
            for task in tasks:
                all_working_files = gazu.files.get_working_files_for_task(task)
                for a in all_working_files:
                    basename = os.path.basename(a['path'])
                    print(f'{basename} : {a["path"]}')


def main():
    project = 'Test_bbr'
    shot = 'shot_01'
    seq = 'seq_01'
    asset = 'Cow'
    task = 'Modeling'

    gz = MyGazu()
    gz.set_project('Test_bbr')
    # gz.set_seq('seq_01')
    # gz.set_shot('shot_01')
    # gz.set_asset('Cow')
    # gz.update_file_tree()
    # gz.create_tree_dir()
    # test.get_path_for_casting("rocket")
    # gz.new_task('modeling')
    # gz.new_task2('Layout')
    # print(gz.new_task2())
    # gz.set_task('modeling')
    # preview_file = '/home/rapa/다운로드/cow.jpg'
    # gz.set_preview('New preview file', preview_file)
    # gz.get_working_publish_for_shot('seq_01', 'shot_01', 'layout')
    # gz.get_working_path_for_shot('seq_01', 'shot_01', 'layout')
    # gz.get_output_publish_for_shot('seq_01', 'shot_01', 'OBJ', 'layout')
    gz.get_output_path_for_shot('seq_01', 'shot_01', 'OBJ', 'layout')
    # gz.working_publish_for_asset('Cow', 'modeling')
    # gz.working_path_for_asset('Cow', 'modeling')


if __name__ == "__main__":
    main()