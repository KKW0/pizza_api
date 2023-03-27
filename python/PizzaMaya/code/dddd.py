#coding:utf8
import os
import gazu

gazu.client.set_host("http://192.168.3.116/api")
gazu.set_event_host("http://192.168.3.116")
gazu.log_in("pipeline@rapa.org", "netflixacademy")

project = gazu.project.get_project_by_name('RAPA')

asset = gazu.asset.get_asset_by_name(project, 'Village')
asset2 = gazu.asset.get_asset_by_name(project, 'Classroom')

s_asset1 = gazu.asset.get_asset_by_name(project, 'Car')
s_asset2 = gazu.asset.get_asset_by_name(project, 'Chair')
s_asset3 = gazu.asset.get_asset_by_name(project, 'House')
s_asset4 = gazu.asset.get_asset_by_name(project, 'Person')

task_status = gazu.task.get_task_status_by_name('Todo')

task_type_layoutpizza = gazu.task.get_task_type_by_name('LayoutPizza')
task_type_lay = gazu.task.get_task_type_by_name('Layout')
task_type_md = gazu.task.get_task_type_by_name('Modeling')
task_type_mm = gazu.task.get_task_type_by_name('Matchmove')
task_type_cam = gazu.task.get_task_type_by_name('Camera')
task_type_str = gazu.task.get_task_type_by_name('Storyboard')
task_type_ani = gazu.task.get_task_type_by_name('Animation')
task_type_li = gazu.task.get_task_type_by_name('Lighting')
task_type_pl = gazu.task.get_task_type_by_name('Plate')

comment = '레이아웃 작업 완료되었습니다. 변경사항: 배치 수정'
software = gazu.files.all_softwares()[1]  # 마야

seq1 = gazu.shot.get_sequence_by_name(project, 'SQ01')

shot1 = gazu.shot.get_shot_by_name(seq1, '0010')
shot2 = gazu.shot.get_shot_by_name(seq1, '0020')

output_type_mb = gazu.files.get_output_type_by_name('MayaBinary')
output_type_ma = gazu.files.get_output_type_by_name('MayaAskii')
output_type_ujpg = gazu.files.get_output_type_by_name('UndistortionJpg')
output_type_pmov = gazu.files.get_output_type_by_name('PreviewMov')
output_type_abc = gazu.files.get_output_type_by_name('Alembic')
output_type_fbx = gazu.files.get_output_type_by_name('FBX')

output_type_exr = gazu.files.get_output_type_by_name('EXR')
output_type_jpg = gazu.files.get_output_type_by_name('JPEG')


def make(proj, t=None, tt=None, sof=None, ot=None, rp=None):
    for shot in gazu.shot.all_shots_for_project(proj):
        for task in gazu.task.all_tasks_for_shot(shot):
            path = os.path.dirname(gazu.files.build_working_file_path(task)[1:])
            path2 = os.path.dirname(gazu.files.build_entity_output_file_path(shot, ot, tt))

            try:
                os.makedirs(os.sep + path)
            except OSError as exc:
                continue

            try:
                os.makedirs(os.sep + path2)
            except OSError as exc:
                continue
            
    for asset in gazu.asset.all_assets_for_project(proj):
        for task in gazu.task.all_tasks_for_asset(asset):
            path = os.path.dirname(gazu.files.build_working_file_path(task)[1:])
            try:
                os.makedirs(os.sep + path)
            except OSError as exc:
                continue

    gazu.task.get_task_by_entity(shot1, tt)
    gazu.task.add_comment(t, task_status, comment)
    w1 = gazu.files.new_working_file(t, software=sof, comment=comment)
    gazu.files.new_entity_output_file(shot1, ot, tt,
                                      comment, w1, representation=rp)

# task = gazu.task.get_task_by_entity(shot1, task_type_mm)
# make(project, task, task_type_mm, ot=output_type_ujpg, rp='jpg')
#
# task = gazu.task.get_task_by_entity(shot1, task_type_cam)
# make(project, task, task_type_cam, ot=output_type_abc, rp='abc')
#
# task = gazu.task.get_task_by_entity(shot1, task_type_cam)
# make(project, task, task_type_cam, ot=output_type_abc, rp='abc')




mountpoint = '/mnt/Project'
root = 'JS'
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

gazu.files.update_project_file_tree(project, tree)
