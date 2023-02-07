import os
import gazu
import pprint as pp


gazu.client.set_host("http://192.168.3.116/api")
gazu.set_event_host("http://192.168.3.116")
gazu.log_in("pipeline@rapa.org", "netflixacademy")

project = gazu.project.get_project_by_name("A_project")
path = os.getcwd()

# tree_sample = {
#     "working": {
#         "mountpoint": "/mnt/pipeline/personal/ahyeonJo",
#         "root": "kitsu",
#         "folder_path": {
#             "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>/working/v<Revision>",
#             "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>/working/v<Revision>",
#             "style": "lowercase"
#         },
#         "file_name": {
#             "shot": "<Project>_<Sequence>_<Shot>_<TaskType>_<Revision>",
#             "asset": "<Project>_<AssetType>_<Asset>_<TaskType>_<Revision>.<Extension>",
#             "style": "lowercase"
#         }
#     },
#     "output": {
#         "mountpoint": "/mnt/pipeline/personal/ahyeonJo",
#         "root": "kitsu",
#         "folder_path": {
#             "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>/output/<OutputType>/v<Revision>",
#             "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>/output/<OutputType>/v<Revision>",
#             "style": "lowercase"
#         },
#         "file_name": {
#             "shot": "<Project>_<Sequence>_<Shot>_<OutputType>_v<Revision>",
#             "asset": "<Project>_<AssetType>_<Asset>_<OutputType>_v<Revision>",
#             "style": "lowercase"
#         }
#     }
# }
# gazu.files.update_project_file_tree(project, tree_sample)

# project = gazu.project.get_project_by_name("jeongtae")
# pp.pprint(project)
# set host and log in


# human = gazu.asset.new_asset_type('Human')
# dog = gazu.asset.new_asset_type('Dog')p
# # Set New asset type
#
# puppy = gazu.task.new_task_type('Puppy_2', color='#00FF01')
# kitty = gazu.task.new_task_type('Kitty_2', color='#00FF01')
# dear = gazu.task.new_task_type('Dear_2', color='#00FF01', entity='Shot')
# # Set New task type for asset, shot
#
# good = gazu.task.new_task_status("Good_2", "good_2", color='#00FF00')
# bad = gazu.task.new_task_status("Bad_2", "bad_2", color='#00FF01')
# # Set New task status
#
# project = gazu.project.new_project("A_project", "featurefilm", asset_types=[dog, human],
#                                    task_types=[puppy, kitty, dear], task_statuses=[good, bad])
# # Set New project
#
# first_walk = gazu.shot.new_episode(project, "First Walk")
# second_walk = gazu.shot.new_episode(project, "Second Walk")
# # Set New episode in project
#
# my_dog = gazu.shot.new_sequence(project, "My Dog", episode=first_walk)
# your_dog = gazu.shot.new_sequence(project, "Your Dog", episode=first_walk)
# # Set New sequence in episode
#
# shot_datadict = {
#     'Description': 'This shot is for filming Thomas\'s tail',
#     'extra_data': 'shot data'}
# # Set New extra data for shot
#
# tail = gazu.shot.new_shot(project, my_dog, "tail", frame_in=1, frame_out=10,
#                           data=shot_datadict)
# tail2 = gazu.shot.new_shot(project, my_dog, "tail2", frame_in=1, frame_out=10,
#                            data=shot_datadict)
# # Set New shot in project, seq
#
# gazu.task.new_task(tail, dear, name='first task')
# # Set New task in shot as task type
#
# thomas_data = {
#     'birth': '2017-05-17',
#     'adoption': '2018-02-28',
#     'color': 'blue merle'}
# # Set New extra data for asset
#
# thomas = gazu.asset.new_asset(project, dog, 'Thomas', description="He is very handsome dog",
#                               extra_data=thomas_data, episode=first_walk)
# # Set New asset
#
# gazu.task.new_task(thomas, puppy, name='make walk')
# # Set New task in asset as task type


# print("\n### project info ###")
# pp.pprint(project)
# # get project info
#
sequences = gazu.shot.all_sequences_for_project(project)
# print("\n### sequences info ###")
# pp.pprint(sequences)
#
shots = gazu.shot.all_shots_for_project(project)
# print("\n### shots info ###")
# pp.pprint(shots)
#
assets = gazu.asset.all_assets_for_project(project)
# print("\n### assets info ###")
# pp.pprint(assets)
#
all_task_types = gazu.task.all_task_types_for_shot(shots[0])
# print("\n### task_types info of tail ###")
# pp.pprint(all_task_types)
#
tasks_for_shot = gazu.task.all_tasks_for_shot(shots[0])
# print("\n### tasks info of thomas shot ###")
# pp.pprint(tasks_for_shot)
#
tasks_for_asset = gazu.task.all_tasks_for_asset(assets[0])
# print("\n### tasks info of tail asset ###")
# pp.pprint(tasks_for_asset)
# pp.pprint(tasks_for_shot)
# pp.pprint(tasks_for_shot[0])
working_file = gazu.files.get_working_files_for_task(tasks_for_shot[0])
pp.pprint(working_file[0])
# gazu.files.upload_working_file(working_file[0], '/mnt/pipeline/personal/ahyeonJo/kitsu/To_Do_list.txt')
# gazu.files.download_working_file(working_file[0], file_path='/home/rapa/testttttt.txt')
#
#
#
# gazu.task.upload_preview_file(tasks_for_shot[0], '/mnt/project/pizza/shots/jt_seq/jt0010/layout/output/play_test.mov')