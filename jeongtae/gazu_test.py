import gazu
import pprint as pp
import os

class TestGazu:

    def __init__(self):
        gazu.client.set_host("http://192.168.3.116/api")
        gazu.set_event_host("http://192.168.3.116")
        gazu.log_in("pipeline@rapa.org", "netflixacademy")
        self._project = None
        self._person = None
        self._asset_type = None
        self._asset = None
        self._seq = None
        self._shot = None
        self._path = None
        self._task = None
        self._status = None
        self._output_type = None
        self._preview_path = None
        self._software = None

    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, value):
        self._project = gazu.project.get_project_by_name(value)

    @property
    def person(self):
        return self._person

    @person.setter
    def person(self, value):
        self._person = value

    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, value):
        self._asset = value

    @property
    def asset_type(self):
        return self._asset_type

    @asset_type.setter
    def asset_type(self, value):
        self._asset_type = value

    @property
    def seq(self):
        return self._seq

    @seq.setter
    def seq(self, value):
        self._seq = value

    @property
    def shot(self):
        return self._shot

    @shot.setter
    def shot(self, value):
        self._shot = value

    @property
    def task_type(self):
        return self._task_type

    @task_type.setter
    def task_type(self, value):
        self._task_type = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def output_type(self):
        return self._output_type

    @output_type.setter
    def output_type(self, value):
        self._output_type = gazu.files.new_output_type(value[0], value[1])

    @property
    def preview_path(self):
        return self._preview_path

    @preview_path.setter
    def preview_path(self, value):
        self._preview_path = value

    @property
    def software(self):
        return self._software

    @software.setter
    def software(self, value):
        self._software = value

    def new_asset_type(self):
        project = self.project
        asset_type = self._asset_type
        all_asset_types = gazu.asset.all_asset_types_for_project(project)
        if asset_type == None:
            raise ValueError("Please input asset_type")
        for x in all_asset_types:
            if x['name'] == asset_type:
                print("asset_type name already exists.")
                asset_type_info = gazu.asset.get_asset_type_by_name(asset_type)
                return asset_type_info
            else:
                asset_type = gazu.asset.new_asset_type(asset_type)
                return asset_type

    def new_asset(self):
        project = self.project
        asset_type_dict = self.new_asset_type()
        asset_name = self._asset
        all_asset = gazu.asset.all_assets_for_project_and_type(project, asset_type_dict['id'])
        if all_asset == []:
            asset = gazu.asset.new_asset(project, asset_type_dict, asset_name)
            return asset
        else:
            for x in all_asset:
                if x['name'] == asset_name:
                    print("asset name already exists.")
                    asset_info = gazu.asset.get_asset_by_name(project, asset_name, asset_type=asset_type_dict)
                    return asset_info
                else:
                    asset2 = gazu.asset.new_asset(project, asset_type_dict, asset_name)
                    return asset2

    def new_seq(self):
        project = self.project
        all_seq = gazu.shot.all_sequences_for_project(project)
        seq_name = self._seq
        if seq_name == None:
            raise ValueError("Please input sequence_type")
        for x in all_seq:
            if x['name'] == seq_name:
                print("sequence name already exists.")
                seq_info = gazu.shot.get_sequence_by_name(project,seq_name)
                return seq_info
            else:
                sequence = gazu.shot.new_sequence(project, seq_name)
                return sequence

    def new_shot(self):
        project = self.project
        shot_name = self._shot
        seq_dict = self.new_seq()
        all_shot = gazu.shot.all_shots_for_sequence(seq_dict)
        if all_shot == []:
            shot = gazu.shot.new_shot(project, seq_dict, shot_name)
            return shot
        else:
            for x in all_shot:
                if x['name'] == shot_name:
                    print("shot name already exists.")
                    shot_info = gazu.shot.get_shot_by_name(seq_dict, shot_name)
                    return shot_info
                else:
                    shot2 = gazu.shot.new_shot(project, seq_dict, shot_name)
                    return shot2

    def assign_task(self, task):
        person_name = gazu.person.get_person_by_full_name(self._person)
        gazu.task.assign_task(task, person_name)

    def get_task_type(self):
        task_type_name = self._task_type
        if task_type_name == None:
            print("Please input task_type")
        else:
            task_type = gazu.task.get_task_type_by_name(task_type_name)
            # task_type = gazu.task.new_task_type(task_type_name)
            return task_type

    def new_task(self, entity, name):
        asset_dict = self.new_asset()
        shot_dict = self.new_shot()
        task_type = self.get_task_type()
        if entity == 'asset':
            all_asset_task = gazu.task.all_tasks_for_asset(asset_dict)
            if all_asset_task == []:
                asset_task = gazu.task.new_task(asset_dict, task_type, name=name)
                return asset_task
            else:
                for x in all_asset_task:
                    if x['name'] == name:
                        print("task name already exists.")
                        asset_task_info = gazu.task.get_task_by_name(asset_dict, task_type, name=name)
                        return asset_task_info
                    else:
                        asset_task2 = gazu.task.new_task(asset_dict, task_type, name=name)
                        return asset_task2
        elif entity == 'shot':
            all_shot_task = gazu.task.all_tasks_for_shot(shot_dict)
            if all_shot_task == []:
                shot_task = gazu.task.new_task(shot_dict, task_type, name=name)
                return shot_task
            else:
                for i in all_shot_task:
                    if i["name"] == name:
                        print("task name already exists.")
                        shot_task_info = gazu.task.get_task_by_name(shot_dict, task_type, name=name)
                        return shot_task_info
                    else:
                        shot_task2 = gazu.task.new_task(shot_dict, task_type, name=name)
                        return shot_task2

    def upload_preview(self, task):
        task_status = gazu.task.get_task_status_by_name("todo")
        comment = gazu.task.add_comment(task, task_status, comment="Change status to work in progress")
        preview_file = gazu.task.add_preview(task, comment, self._preview_path)
        gazu.task.set_main_preview(preview_file)

    def get_file_tree(self):
        mount_point = self._path[0]
        root = self._path[1]
        tree = {
            "working": {
                "mountpoint": mount_point,
                "root": root,
                "folder_path": {
                    "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>/working/v<Revision>",
                    "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>/working/v<Revision>",
                    "sequence": "<Project>/sequences/<Sequence>>/<TaskType>/working",
                    "style": "lowercase",
                },
                "file_name": {
                    "shot": "<Project>_<Sequence>_<Shot>_<TaskType>_<Revision>",
                    "asset": "<Project>_<AssetType>_<Asset>_<TaskType>_<Revision>",
                    "sequence": "<Project>_<Sequence>_<TaskType>",
                    "style": "lowercase"
                }
            },
            "output": {
                "mountpoint": mount_point,
                "root": root,
                "folder_path": {
                    "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>/output/<OutputType>/v<Revision>",
                    "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>/output/<OutputType>/v<Revision>",
                    "sequence": "<Project>/sequences/<Sequence>>/<TaskType>/output",
                    "style": "lowercase"
                },
                "file_name": {
                    "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>/output/<OutputType>/v<Revision>",
                    "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>/output/<OutputType>/v<Revision>",
                    "sequence": "<Project>_<Sequence>_<TaskType>",
                    "style": "lowercase"
                }
            }
        }
        return tree

    def new_working_file(self, task):
        project = self.project
        tree = self.get_file_tree()
        maya = gazu.files.get_software_by_name(self._software)
        gazu.files.update_project_file_tree(project, tree)
        working_file = gazu.files.new_working_file(task, software=maya)
        working_file_path = os.path.dirname(working_file.get('path'))
        if os.path.exists(working_file_path):
            print("path exists")
        else:
            print("create working file path :", working_file_path)
            os.makedirs(working_file_path)

    def template_working_path(self, task):
        last_revision = gazu.files.get_last_working_file_revision(task)
        all_working_files = gazu.files.get_working_files_for_task(task)
        working_file_path = os.path.dirname(
            gazu.files.build_working_file_path(task, revision=last_revision.get('revision'))
        )
        for a in all_working_files:
            if a["revision"] == last_revision.get('revision'):
                software = gazu.files.get_software(a.get("software_id"))
                return a.get("path") + "." + software.get("file_extension")

    def new_output_file(self, entity, representation):
        output_type = self._output_type
        task_type = self.get_task_type()
        gazu.files.update_project_file_tree(self.project, self.get_file_tree())
        output_file = gazu.files.new_entity_output_file(entity, output_type, task_type, "publish output_file",
                                                        representation=representation,
                                                        )
        output_file_path = os.path.dirname(output_file.get('path'))
        if os.path.exists(output_file_path):
            print("path exists")
        else:
            print("create output file path :", output_file_path)
            os.makedirs(output_file_path)

    def template_output_path(self, entity):
        output_type = self._output_type
        task_type = self.get_task_type()
        last_revision = gazu.files.get_last_entity_output_revision(entity, output_type, task_type, name='main')
        all_output_files = gazu.files.all_output_files_for_entity(entity, output_type, task_type)
        for output_file in all_output_files:
            if output_file.get("revision") == last_revision:
                return output_file.get("path") + "." + output_file.get("representation")

    def new_casting_path_for_shot(self, entity, new):
        project = self.project
        shot_casting = gazu.casting.get_shot_casting(entity)
        shot_casting.append(new)
        gazu.casting.update_shot_casting(project, entity, casting=shot_casting)


def main():
    tg = TestGazu()
    tg.software = 'Maya'
    tg.project = 'jeongtae'
    tg.person = 'pipeline API'
    tg.path = "/mnt/project/pizza", "kitsu"
    tg.preview_path = '/home/rapa/undi_image.jpg'
    tg.asset_type = 'Prop'
    tg.asset = 'chair'
    tg.seq = 'seq1'
    tg.shot = 'shot02'
    tg.task_type = "layout"
    tg.status = "todo"
    asset_dict = tg.new_asset()
    shot_dict = tg.new_shot()
    tg.output_type = "playblast", "image"
    shot_task = tg.new_task("shot", "new")
    # asset_task = tg.new_task("asset", "new")
    # tg.assign_task(shot_task)
    # tg.upload_preview(asset_task)
    # tg.new_working_file(asset_task)
    # tg.template_working_path(asset_task)
    # tg.new_output_file(asset_dict, 'fbx')
    # tg.upload_preview(asset_task)
    # tg.new_working_file(shot_task)
    # pp.pprint(tg.template_working_path(shot_task))
    # tg.new_output_file(shot_dict,'jpg')
    # tg.template_output_path(shot_dict)
    # tg.template_output_path(asset_dict)
    # new = {"asset_id": asset_dict['id'], "nb_occurences": 3}
    # tg.new_casting_path_for_shot(shot_dict, new)


if __name__ == "__main__":
    main()

