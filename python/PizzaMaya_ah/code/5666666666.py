#coding:utf8
import os
import gazu
import pprint as pp

gazu.client.set_host("http://192.168.3.116/api")
gazu.set_event_host("http://192.168.3.116")
gazu.log_in("pipeline@rapa.org", "netflixacademy")

# class SET():
#     def test_setUp(self):
#         # gazu.client.set_host("http://192.168.3.116/api")
#         # gazu.log_in("pipeline@rapa.org", "netflixacademy")
#         #
#         # # 테스트용 클래스변수 정의
#         # self.project = gazu.project.get_project_by_name('Project1')
#         # self.asset = gazu.asset.get_asset_by_name(self.project, 'lecture')
#         # self.user = gazu.person.get_person_by_full_name('ahyeon jo')
#         # self.task_status = gazu.task.get_task_status_by_name('Todo')
#         # self.task_type = gazu.task.get_task_type_by_name('LayoutPizza')
#         # self.task = gazu.task.get_task_by_entity(self.asset, self.task_type)
#         # self.comment = 'Unit Test'
#         # # gazu.task.add_comment(self.task, self.task_status, self.comment)
#         # self.comment_dict = gazu.task.get_last_comment_for_task(self.task)
#         # print(self.comment_dict)
#         # self.software = gazu.files.all_softwares()[1]  # 마야
#         # self.sa1 = gazu.asset.get_asset_by_name(self.project, 'dog')
#         # self.sa2 = gazu.asset.get_asset_by_name(self.project, 'chair')
#         # self.sa3 = gazu.asset.get_asset_by_name(self.project, 'computer')
#         # self.sa4 = gazu.asset.get_asset_by_name(self.project, 'paper')
#         # self.sa5 = gazu.asset.get_asset_by_name(self.project, 'human')
#         # self.sa6 = gazu.asset.get_asset_by_name(self.project, 'assetcasttest')
#         # self.seq1 = gazu.shot.get_sequence_by_name(self.project, 'seq_1')
#         # self.seq2 = gazu.shot.get_sequence_by_name(self.project, 'seq_2')
#         # self.shot1 = gazu.shot.get_shot_by_name(self.seq1, 'sh1')
#         # self.shot2 = gazu.shot.get_shot_by_name(self.seq1, 'sh2')
#         # self.shot3 = gazu.shot.get_shot_by_name(self.seq1, 'sh3')
#         # # mb = gazu.files.new_output_type('MayaBinary', 'mb')
#         # # ma = gazu.files.new_output_type('MayaAskii', 'ma')
#         # # gazu.files.new_output_type('UndistortionJpg', 'jpg')
#         # # gazu.files.new_output_type('PreviewMov', 'mov')
#         # # JPG, OBJ, FBX, Alembic, MPEG-4 이미 있음
#         # # w = gazu.files.new_working_file(self.task, software=self.software, comment=self.comment)
#         # # gazu.files.new_entity_output_file(self.asset, mb, self.task_type, self.comment, w, representation='mb')
#         # self.output_type_mb = gazu.files.get_output_type_by_name('MayaBinary')
#         # self.output_type_ma = gazu.files.get_output_type_by_name('MayaAskii')
#         # self.output_type_ujpg = gazu.files.get_output_type_by_name('UndistortionJpg')
#         # self.output_type_pmov = gazu.files.get_output_type_by_name('PreviewMov')
#         # self.output_type_abc = gazu.files.get_output_type_by_name('Alembic')
#         # working_file = gazu.files.get_working_files_for_task(self.task)
#         # self.working_file = working_file[0]
#         # output_file = gazu.files.get_last_output_files_for_entity(self.asset, self.output_type_mb, self.task_type)
#         # self.output_file = output_file[0]
#         # # self.path = '/home/rapa/foldertree_test/a/b/c/d/e/f/g/working/working_file'
#         # # self.path2 = '/home/rapa/foldertree_test/a/b/c/d/e/f/g/output/output_file'
#         # task_type = gazu.task.get_task_type_by_name('Matchmove')
#         # task = gazu.task.get_task_by_entity(self.shot2['id'], task_type)
#         # # ww = gazu.files.get_working_files_for_task(task)
#         # # pp.pprint(ww)
#         # # w1 = gazu.files.new_working_file(task)
#         # # w2 = gazu.files.new_working_file(task)
#         # # a2 = gazu.files.new_entity_output_file(self.shot2, self.output_type_abc, task_type, 'ppp', w2)
#         # # d = gazu.files.get_last_output_files_for_entity(self.shot2, self.output_type_ujpg, task_type)
#         # # c = gazu.files.get_last_output_files_for_entity(self.shot2, self.output_type_abc, task_type)
#         # # pp.pprint(d)
#         # # pp.pprint(c)
#         # # www = gazu.files.get_last_working_files(task)
#         # # pp.pprint(www)
#         # a1 = gazu.files.new_entity_output_file(self.shot2, self.output_type_ujpg, task_type, 'sss', www['main'])
#         # c = gazu.files.get_last_output_files_for_entity(self.shot2['id'], self.output_type_ujpg, task_type)
#         # pp.pprint(c)
#         # g = gazu.shot.get_shot('c5395426-6068-4deb-b55b-99d76817eabb')
#         # pp.pprint(g)
#
#
#
#         # mountpoint = '/mnt/project/pizza'
#         # root = 'kitsu'
#         # tree = {
#         #     "working": {
#         #         "mountpoint": mountpoint,
#         #         "root": root,
#         #         "folder_path": {
#         #             "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>/working/v<Revision>",
#         #             "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>/working/v<Revision>",
#         #             "style": "lowercase"
#         #         },
#         #         "file_name": {
#         #             "shot": "<Project>_<Sequence>_<Shot>_<TaskType>_<Revision>",
#         #             "asset": "<Project>_<AssetType>_<Asset>_<TaskType>_<Revision>",
#         #             "style": "lowercase"
#         #         }
#         #     },
#         #     "output": {
#         #         "mountpoint": mountpoint,
#         #         "root": root,
#         #         "folder_path": {
#         #             "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>/output/<OutputType>/v<Revision>",
#         #             "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>/output/<OutputType>/v<Revision>",
#         #             "style": "lowercase"
#         #         },
#         #         "file_name": {
#         #             "shot": "<Project>_<Sequence>_<Shot>_<OutputType>_v<Revision>",
#         #             "asset": "<Project>_<AssetType>_<Asset>_<OutputType>_v<Revision>",
#         #             "style": "lowercase"
#         #         }
#         #     }
#         # }
#         project = gazu.project.get_project_by_name('Project1')
#         # gazu.files.update_project_file_tree(project, tree)
#         asset_name = 'chair'
#         task_type_name = 'Modeling'
#         output_type = gazu.files.new_output_type('FBX', 'fbx')
#         asset_dict = gazu.asset.get_asset_by_name(project, asset_name)
#         # task_type = gazu.task.get_task_type_by_name('Modeling')
#         a = gazu.task.new_task(asset_dict, task_type, 'Todo')
#         task = gazu.task.get_task_by_name(asset_dict, task_type)
#         # pp.pprint(task)
#         # working_file = gazu.files.new_working_file(task)
#         # working_last_revision = gazu.files.get_last_working_file_revision(task)
#         # pp.pprint(working_last_revision)
#         # ww = gazu.files.get_last_working_files(task)
#         # pp.pprint(ww)
#         #
#         # output_file = gazu.files.new_entity_output_file(asset_dict, output_type, task_type, "publish output_file",
#         #                                                 working_file=working_file,
#         #                                                 nb_elements='20',
#         #                                                 representation='fbx')
#         # gazu.files.new_entity_output_file(asset_dict, output_type, task_type, comment='stage')
#         # last_output_file = gazu.files.get_last_output_files_for_entity(asset_dict)
#         # output_file_path = os.path.dirname(last_output_file.get('path'))
#         # if os.path.exists(output_file_path):
#         #     os.makedirs(output_file_path)
#         # pp.pprint(last_output_file)
#         #
#
#
# s = SET()
# s.test_setUp()


project = gazu.project.get_project_by_name('Project1')
asset_name = 'chair'
asset_dict = gazu.asset.get_asset_by_name(project, asset_name)


proj = gazu.project.all_projects()
task_type = gazu.task.get_task_type_by_name('asdfasdfasf')
for pro in proj:
    tasks = gazu.task.all_tasks_for_task_type(pro, task_type)
    print(tasks)
    # pp.pprint(tasks)
    for tas in tasks:
        print(tas)
        gazu.task.remove_task(tas)
# gazu.task.remove_task_type(task_type)

# print(gazu.task.get_task('cb3ab26d-75ec-4a31-b2da-d15fcfb598a4'))

# aa = gazu.files.get_output_file('cb3ab26d-75ec-4a31-b2da-d15fcfb598a4')
# print(aa)

aa = gazu.files.all_output_types_for_entity(asset_dict)
print(aa)

'93eb1da9-718f-4132-9461-5872577a4974'

