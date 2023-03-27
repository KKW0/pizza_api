#coding:utf8
import os
import gazu
import pprint as pp

gazu.client.set_host("http://192.168.3.116/api")
gazu.set_event_host("http://192.168.3.116")
gazu.log_in("pipeline@rapa.org", "netflixacademy")

class SET():
    def __init__(self):
        self.project = gazu.project.get_project_by_name('RAPA')
        self.asset = gazu.asset.get_asset_by_name(self.project, 'Village')
        self.asset2 = gazu.asset.get_asset_by_name(self.project, 'Classroom')
        self.s_asset1 = gazu.asset.get_asset_by_name(self.project, 'Car')
        self.s_asset2 = gazu.asset.get_asset_by_name(self.project, 'Chair')
        self.s_asset3 = gazu.asset.get_asset_by_name(self.project, 'House')
        self.s_asset4 = gazu.asset.get_asset_by_name(self.project, 'Person')
        # self.user = gazu.person.get_person_by_full_name('ahyeon jo')
        self.task_status = gazu.task.get_task_status_by_name('Todo')
        self.task_type_layoutpizza = gazu.task.get_task_type_by_name('LayoutPizza')
        self.task_type_lay = gazu.task.get_task_type_by_name('Layout')
        self.task_type_md = gazu.task.get_task_type_by_name('Modeling')
        self.task_type_mm = gazu.task.get_task_type_by_name('Matchmove')
        self.task_type_cam = gazu.task.get_task_type_by_name('Camera')
        gazu.task.get_task_type_by_name('Storyboard')
        self.comment = '레이아웃 작업 완료되었습니다. 변경사항: 배치 수정'
        self.software = gazu.files.all_softwares()[1]  # 마야
        self.seq1 = gazu.shot.get_sequence_by_name(self.project, 'SQ01')
        self.seq2 = gazu.shot.get_sequence_by_name(self.project, 'SQ02')
        self.shot1 = gazu.shot.get_shot_by_name(self.seq1, '0010')
        self.shot2 = gazu.shot.get_shot_by_name(self.seq1, '0020')
        self.output_type_mb = gazu.files.get_output_type_by_name('MayaBinary')
        self.output_type_ma = gazu.files.get_output_type_by_name('MayaAskii')
        self.output_type_ujpg = gazu.files.get_output_type_by_name('UndistortionJpg')
        self.output_type_pmov = gazu.files.get_output_type_by_name('PreviewMov')
        self.output_type_abc = gazu.files.get_output_type_by_name('Alembic')
        self.output_type_fbx = gazu.files.get_output_type_by_name('FBX')

        # mountpoint = '/mnt/project'
        # root = 'JS'
        # tree = {
        #     "working": {
        #         "mountpoint": mountpoint,
        #         "root": root,
        #         "folder_path": {
        #             "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>/working/v<Revision>",
        #             "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>/working/v<Revision>",
        #             "style": "lowercase"
        #         },
        #         "file_name": {
        #             "shot": "<Project>_<Sequence>_<Shot>_<TaskType>_<Revision>",
        #             "asset": "<Project>_<AssetType>_<Asset>_<TaskType>_<Revision>",
        #             "style": "lowercase"
        #         }
        #     },
        #     "output": {
        #         "mountpoint": mountpoint,
        #         "root": root,
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
        #
        # gazu.files.update_project_file_tree(self.project, tree)


        self.task = gazu.task.get_task_by_entity(self.shot2, self.task_type_mm)
        gazu.task.add_comment(self.task, self.task_status, self.comment)
        self.comment_dict = gazu.task.get_last_comment_for_task(self.task)
        w1 = gazu.files.new_working_file(self.task, software=self.software, comment=self.comment)
        gazu.files.new_entity_output_file(self.shot2, self.output_type_ujpg, self.task_type_mm,
                                          self.comment, w1, representation='jpg')
        wpath = gazu.files.build_working_file_path(self.task)
        path = gazu.files.build_entity_output_file_path(self.shot2, self.output_type_ujpg, self.task_type_mm,
                                                        representation='jpg', nb_elements='1')
        os.makedirs(wpath)
        os.makedirs(path)

        self.task = gazu.task.get_task_by_entity(self.shot2, self.task_type_cam)
        gazu.task.add_comment(self.task, self.task_status, self.comment)
        self.comment_dict = gazu.task.get_last_comment_for_task(self.task)
        w2 = gazu.files.new_working_file(self.task, comment=self.comment)
        gazu.files.new_entity_output_file(self.shot2, self.output_type_abc, self.task_type_cam,
                                          self.comment, w2, representation='abc')
        wpath = gazu.files.build_working_file_path(self.task)
        path = gazu.files.build_entity_output_file_path(self.shot2, self.output_type_abc, self.task_type_cam,
                                                        representation='abc', nb_elements='1')
        os.makedirs(wpath)
        os.makedirs(path)

        # self.task = gazu.task.get_task_by_entity(self.s_asset1, self.task_type_md)
        # gazu.task.add_comment(self.task, self.task_status, self.comment)
        # self.comment_dict = gazu.task.get_last_comment_for_task(self.task)
        # w3 = gazu.files.new_working_file(self.task, comment=self.comment)
        # gazu.files.new_entity_output_file(self.s_asset1, self.output_type_fbx, self.task_type_md,
        #                                   self.comment, w3, nb_elements='2', representation='fbx')
        # wpath = gazu.files.build_working_file_path(self.task)
        # path = gazu.files.build_entity_output_file_path(self.s_asset1, self.output_type_fbx, self.task_type_md,
        #                                                 representation='fbx', nb_elements='2')
        # os.makedirs(wpath)
        # os.makedirs(path)
        #
        # self.task = gazu.task.get_task_by_entity(self.s_asset2, self.task_type_md)
        # gazu.task.add_comment(self.task, self.task_status, self.comment)
        # self.comment_dict = gazu.task.get_last_comment_for_task(self.task)
        # w3 = gazu.files.new_working_file(self.task, comment=self.comment)
        # gazu.files.new_entity_output_file(self.s_asset2, self.output_type_fbx, self.task_type_md,
        #                                   self.comment, w3, nb_elements='5', representation='fbx')
        # wpath = gazu.files.build_working_file_path(self.task)
        # path = gazu.files.build_entity_output_file_path(self.s_asset2, self.output_type_fbx, self.task_type_md,
        #                                                 representation='fbx', nb_elements='5')
        # os.makedirs(wpath)
        # os.makedirs(path)
        #
        # self.task = gazu.task.get_task_by_entity(self.s_asset3, self.task_type_md)
        # gazu.task.add_comment(self.task, self.task_status, self.comment)
        # self.comment_dict = gazu.task.get_last_comment_for_task(self.task)
        # w3 = gazu.files.new_working_file(self.task, comment=self.comment)
        # gazu.files.new_entity_output_file(self.s_asset3, self.output_type_fbx, self.task_type_md,
        #                                   self.comment, w3, nb_elements='1', representation='fbx')
        # wpath = gazu.files.build_working_file_path(self.task)
        # path = gazu.files.build_entity_output_file_path(self.s_asset3, self.output_type_fbx, self.task_type_md,
        #                                                 representation='fbx', nb_elements='1')
        # os.makedirs(wpath)
        # os.makedirs(path)
        #
        # self.task = gazu.task.get_task_by_entity(self.s_asset4, self.task_type_md)
        # gazu.task.add_comment(self.task, self.task_status, self.comment)
        # self.comment_dict = gazu.task.get_last_comment_for_task(self.task)
        # w3 = gazu.files.new_working_file(self.task, comment=self.comment)
        # gazu.files.new_entity_output_file(self.s_asset4, self.output_type_fbx, self.task_type_md,
        #                                   self.comment, w3, nb_elements='1', representation='fbx')
        # wpath = gazu.files.build_working_file_path(self.task)
        # path = gazu.files.build_entity_output_file_path(self.s_asset4, self.output_type_fbx, self.task_type_md,
        #                                                 representation='fbx', nb_elements='1')
        # os.makedirs(wpath)
        # os.makedirs(path)

s = SET()