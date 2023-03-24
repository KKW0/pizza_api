import gazu
import os
import pprint as pp

gazu.client.set_host("http://192.168.3.116/api")
gazu.set_event_host("http://192.168.3.116")
gazu.log_in("pipeline@rapa.org", "netflixacademy")
mountpoint = '/mnt/project/pizza'
root = 'kitsu'
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
project = gazu.project.get_project_by_name('Project1')
gazu.files.update_project_file_tree(project, tree)
seq_name='seq_1'
shot_name = 'sh3'
task_type_name = 'Matchmove'
output_type = gazu.files.new_output_type('fbx', 'model')
seq_dict = gazu.shot.get_sequence_by_name(project, seq_name)
shot_dict = gazu.shot.get_shot_by_name(seq_dict, shot_name)
task_type = gazu.task.get_task_type_by_name(task_type_name)
task = gazu.task.get_task_by_name(shot_dict, task_type)
# pp.pprint(task)
# working_file = gazu.files.new_working_file(task)
# working_last_revision = gazu.files.get_last_working_file_revision(task)
# pp.pprint(working_last_revision)

#
#
# output_file = gazu.files.new_entity_output_file(task, output_type, task_type, "publish output_file", representation='FBX')
# gazu.files.new_entity_output_file(shot_dict, output_type, task_type, comment='model',representation='fbx')
last_output_file = gazu.files.get_last_output_files_for_entity(shot_dict)
output_file_path = os.path.dirname(last_output_file[0]['path'])
# pp.pprint(output_file_path)
if not os.path.exists(output_file_path):
    os.makedirs(output_file_path)
# pp.pprint(last_output_file)