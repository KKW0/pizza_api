#coding:utf8
import pprint as pp
import gazu
import os

# gazu - login
gazu.client.set_host("http://192.168.3.116/api")
gazu.set_event_host("http://192.168.3.116")
gazu.log_in("pipeline@rapa.org", "netflixacademy")

# create project
new_prod = gazu.project.new_project("Test_Euimin")
# pp.pprint(new_prod)

# create product?
characters = gazu.asset.new_asset_type("Characters")
props = gazu.asset.new_asset_type("Props")

# create asset
rabbit = gazu.asset.new_asset(new_prod, characters, "Rabbit")
monkey = gazu.asset.new_asset(new_prod, characters, "Monkey")
chair = gazu.asset.new_asset(new_prod, props, "Chair")

# create seq / shot
sequence = gazu.shot.new_sequence(new_prod, "My_seq")
shot = gazu.shot.new_shot(new_prod, sequence, "My_shot")


# create task_type
modeling = gazu.task.get_task_type_by_name("Modeling")
rigging = gazu.task.get_task_type_by_name("Rigging")
concept = gazu.task.get_task_type_by_name("Concept")
uv = gazu.task.get_task_type_by_name("UV")
layout = gazu.task.get_task_type_by_name("Layout")

monkey_info = gazu.asset.get_asset_by_name(new_prod, "Monkey")
rabbit_info = gazu.asset.get_asset_by_name(new_prod, "Rabbit")

# create asset tasks type / status hip
task = gazu.task.new_task(monkey, modeling)
gazu.task.start_task(task)

wip1 = gazu.task.get_task_status_by_short_name("wip")
test_rabbit = gazu.task.get_task_by_name(rabbit_info['id'], concept)
# comment1 = gazu.task.add_comment(test_rabbit, wip1, "Cherry")
# preview_file = gazu.task.add_preview(test_rabbit, comment1, "/home/rapa/test.jpeg")
# gazu.task.set_main_preview(preview_file)


wip2 = gazu.task.get_task_status_by_short_name("wip")
test_monkey = gazu.task.get_task_by_name(monkey_info['id'], modeling)
# comment2 = gazu.task.add_comment(test_monkey, wip2, "체리에요")
# preview_file = gazu.task.add_preview(test_monkey, comment2, "/home/rapa/test.jpeg")
# gazu.task.set_main_preview(preview_file)

# test_download = gazu.files.download_preview_file(test_rabbit, '/home/rapa')


for asset in gazu.asset.all_assets_for_project(new_prod):
    gazu.task.new_task(asset, modeling)
    gazu.task.new_task(asset, rigging)
    gazu.task.new_task(asset, concept)
    gazu.task.new_task(asset, uv)

gazu.task.new_task(shot, layout)
# pp.pprint(test_monkey)


task_type = gazu.task.get_task_type_by_name(layout)
# pp.pprint(task_type)


# for asset in gazu.asset.all_assets_for_project(new_prod):
#     for task in gazu.task.all_tasks_for_asset(asset):
#         path = os.path.dirname(gazu.files.build_working_file_path(task))[1:]
#         os.makedirs(path, exist_ok=True)
#
# for shot in gazu.shot.all_shots_for_project(new_prod):
#     for task in gazu.task.all_tasks_for_shot(shot):
#         path = os.path.dirname(gazu.files.build_working_file_path(task))[1:]
#         os.makedirs(path, exist_ok=True)

# my_asset = gazu.asset.get_asset_by_name('proj_name', 'asset_name')
# my_sequence = gazu.shot.get_sequence_by_name('proj_name', 'seq_name')
# my_shot = gazu.shot.get_shot_by_name(my_sequence, 'shot_name')
# asset_castings = gazu.casting.get_shot_casting(my_shot)
# new = {"추가사항" : "입니다"}
# asset_castings.append(new)
# gazu.casting.update_shot_casting('proj_name', my_shot, casting=asset_castings)
#
# cast_in = gazu.casting.get_asset_cast_in(my_asset)
