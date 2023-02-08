#coding:uft8
import os
import gazu
import pprint as pp
import maya.cmds as mc


class SaveAsKitsuPath:
    def __init__(self):
        gazu.client.set_host("http://192.168.3.116/api")
        gazu.set_event_host("http://192.168.3.116")
        gazu.log_in("pipeline@rapa.org", "netflixacademy")

        self._working_path = None
        self._output_path = None
        self._project_list = None
        self._sequence_list = None
        self._entity_list = None
        self._task_type_list = None
        self._task_list = None
        self._software_list = None
        self._output_type_list = None

        # output, working file 만들기 위한 분류
        self._project = None
        self._sequence = None
        self._asset_type = None
        self._entity = None
        # output file의 entity(asset / shot)
        self._task_type = None
        self._task = None
        self._software = None
        self._output_type = None

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
        self._sequence = gazu.shot.get_sequence_by_name(self.project)

    @property
    def asset_type(self):
        return self._asset_type

    @asset_type.setter
    def asset_type(self, value):
        self._asset_type = gazu.asset.get_asset_type_by_name(value)
    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, value):
        if value == "Shot":
            self._entity = gazu.shot.get_shot_by_name(self.sequence, value)
        elif value == "Asset":
            self._entity = gazu.shot.get_shot_by_name(self.project, value, self.asset_type)

    @property
    def task_type(self):
        return self._task_type

    @task_type.setter
    def task_type(self, value):
        self._task_type = gazu.task.get_task_type_by_name(value)

    @property
    def task(self):
        return self._task

    @task.setter
    def task(self, value):
        self._task = gazu.task.get_task_by_name(self.entity, self.task_type, value)

    @property
    def software(self):
        return self._software

    @software.setter
    def software(self, value):
        self._software = gazu.files.get_software_by_name(value)

    @property
    def output_type(self):
        return self._output_type

    @output_type.setter
    def output_type(self, value):
        self.output_type = gazu.files.get_output_type_by_name(value)

    def get_kitsu_path(self):
        pass

    def make_folder_tree(self):
        pass

    def save_working_file(self):
        pass

    def export_output_file(self):
        pass

    def make_kitsu_file_data(self):
        pass


def main():
    save_path = SaveAsKitsuPath()
    save_path.project = "A_project"
    save_path.sequence = ""
    save_path.entity = "Shot"


if __name__ == "__main__":
    main()
