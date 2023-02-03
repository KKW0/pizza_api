import gazu
import os
import pprint as pp


class UploadNewFileToDB:
    def __init__(self):
        gazu.client.set_host("http://192.168.3.116/api")
        gazu.set_event_host("http://192.168.3.116")
        gazu.log_in("pipeline@rapa.org", "netflixacademy")
        self.new_prod = None
        self.characters = None
        self.props = None
        self.rabbit = None
        self.monkey = None
        self.chair = None
        self.sequence = None
        self.shot = None
        self.modeling = None
        self.rigging = None
        self.concept = None
        self.uv = None
        self.layout = None

    def create_project_and_etc(self):
        self.new_prod = gazu.project.new_project("Test_Euimin")
        self.characters = gazu.asset.new_asset_type("Characters")
        self.props = gazu.asset.new_asset_type("Props")
        self.rabbit = gazu.asset.new_asset(self.new_prod, self.characters, "Rabbit")
        self.monkey = gazu.asset.new_asset(self.new_prod, self.characters, "Monkey")
        self.chair = gazu.asset.new_asset(self.new_prod, self.props, "Chair")
        self.sequence = gazu.shot.new_sequence(self.new_prod, "My_seq")
        self.shot = gazu.shot.new_shot(self.new_prod, self.sequence, "My_shot")

    def get_project_and_etc(self):
        self.new_prod = gazu.project.get_project_by_name("Test_Euimin")
        self.modeling = gazu.task.get_task_type_by_name("Modeling")
        self.rigging = gazu.task.get_task_type_by_name("Rigging")
        self.concept = gazu.task.get_task_type_by_name("Concept")
        self.uv = gazu.task.get_task_type_by_name("UV")
        self.layout = gazu.task.get_task_type_by_name("Layout")

    def make_tasks_in_kitsu(self):
        for asset in gazu.asset.all_assets_for_project(new_prod):
            gazu.task.new_task(asset, modeling)
            gazu.task.new_task(asset, rigging)
            gazu.task.new_task(asset, concept)
            gazu.task.new_task(asset, uv)
        gazu.task.new_task(shot, layout)

    def make_folder_tree_in_mnt(self):
        gazu.files.set_project_file_tree(self.new_prod, 'simple')
        for asset in gazu.asset.all_assets_for_project(self.new_prod):
            for task in gazu.task.all_tasks_for_asset(asset):
                path = os.path.dirname(gazu.files.build_working_file_path(task))[1:]
                os.makedirs(path)

        for shot in gazu.shot.all_shots_for_project(self.new_prod):
            for task in gazu.task.all_tasks_for_shot(shot):
                path = os.path.dirname(gazu.files.build_working_file_path(task))[1:]
                os.makedirs(path)


def main():
    ud = UploadNewFileToDB()
    # ud.create_project_and_etc()
    ud.get_project_and_etc()
    # ud.make_tasks_in_kitsu()
    ud.make_folder_tree_in_mnt()


if __name__ == "__main__":
    main()
