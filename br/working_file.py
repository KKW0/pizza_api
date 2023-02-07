import os
import gazu
import pprint as pp

class MyGazu:
    def __init__(self):
        gazu.client.set_host("http://192.168.3.116/api")
        gazu.log_in("pipeline@rapa.org", "netflixacademy")
        self.project = None
        self.asset = None
        self.task = None
        self.task_type = None

    def set_project(self, name):
        self.project = gazu.project.get_project_by_name(name)

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

    def update_file_tree(self):
        project = gazu.project.get_project_by_name(self.project_name)
        gazu.files.update_project_file_tree(project,
                                        dict(working=dict(mountpoint="/working_files", root="productions", folder_path={
                                            "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>",
                                            "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>",
                                            "sequence": "<Project>/sequences/<Sequence>>/<TaskType>",
                                            "style": "lowercase"
                                        }, file_name={
                                            "shot": "<Project>_<Sequence>_<Shot>_<TaskType>",
                                            "asset": "<Project>_<AssetType>_<Asset>_<TaskType>",
                                            "sequence": "<Project>_<Sequence>_<TaskType>",
                                            "style": "lowercase"
                                        }), output={
                                            "mountpoint": "/output_files",
                                            "root": "productions",
                                            "folder_path": {
                                                "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>",
                                                "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>",
                                                "sequence": "<Project>/sequences/<Sequence>>/<TaskType>",
                                                "style": "lowercase"
                                            },
                                            "file_name": {
                                                "asset": "<Project>_<AssetType>_<Asset>_<TaskType>",
                                                "shot": "<Project>_<Sequence>_<Shot>_<TaskType>",
                                                "sequence": "<Project>_<Sequence>_<TaskType>",
                                                "style": "lowercase"
                                            }
                                        }, preview={
                                            "mountpoint": "/preview_files",
                                            "root": "productions",
                                            "folder_path": {
                                                "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>",
                                                "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>",
                                                "sequence": "<Project>/sequences/<Sequence>>/<TaskType>",
                                                "style": "lowercase"
                                            },
                                            "file_name": {
                                                "asset": "<Project>_<AssetType>_<Asset>_<TaskType>",
                                                "shot": "<Project>_<Sequence>_<Shot>_<TaskType>",
                                                "sequence": "<Project>_<Sequence>_<TaskType>",
                                                "style": "lowercase"
                                            }
                                            }
                                            )
                                            )

def main():
    project = 'Test_bbr'
    asset = 'Desk'
    task = 'Modeling'

    gz = MyGazu()
    gz.set_project('Test_bbr')
    gz.set_asset('Desk')
    gz.new_task('modeling')
    # gz.set_task('modeling')
    preview_file = '/home/rapa/다운로드/desk.jpg'
    gz.set_preview('New preview file', preview_file)


if __name__ == "__main__":
    main()