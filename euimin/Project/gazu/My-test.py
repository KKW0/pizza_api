import gazu
import os
import pprint as pp


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


# create asset tasks type / status wip
task = gazu.task.new_task(chair, concept)
# gazu.task.start_task(task)


for asset in gazu.asset.all_assets_for_project(new_prod):
    gazu.task.new_task(asset, modeling)
    gazu.task.new_task(asset, rigging)
    gazu.task.new_task(asset, concept)
    gazu.task.new_task(asset, uv)

gazu.task.new_task(shot, layout)

# person = gazu.person.all_persons()
person_name = gazu.person.get_person_by_full_name("euimin")
rabbit_concept = gazu.task.get_task_type(concept['id'])
pp.pprint(rabbit_concept)
# pp.pprint(person_name)
# pp.pprint(person)
gazu.task.assign_task(task, person_name)

# 요기는 동작이 안됩니당..
# def assign_user(self):
#     task = gazu.task.new_task(task_name, task_type) # ex) rabbit, concept
#     person_name = gazu.person.get_person_by_full_name("euimin") # ex) user_name
#     # person = gazu.person.all_persons() ex) person[0] -> one person number?
#     gazu.task.assign_task(task, person_name) # ex) task, person_name or person[0]

# gazu.files.set_project_file_tree(new_prod, 'simple')
#
# for asset in gazu.asset.all_assets_for_project(new_prod):
#     for task in gazu.task.all_tasks_for_asset(asset):
#         path = os.path.dirname(gazu.files.build_working_file_path(task))[1:]
#         os.makedirs(path)
#
# for shot in gazu.shot.all_shots_for_project(new_prod):
#     for task in gazu.task.all_tasks_for_shot(shot):
#         path = os.path.dirname(gazu.files.build_working_file_path(task))[1:]
#         os.makedirs(path)

