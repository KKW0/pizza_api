import os
import gazu
import pprint as pp


gazu.client.set_host("http://192.168.3.116/api")
gazu.set_event_host("http://192.168.3.116")
gazu.log_in("pipeline@rapa.org", "netflixacademy")

project = gazu.project.get_project_by_name("NetflixAcademy")
hulk = gazu.asset.get_asset_by_name(project, "Hulkbuster")
print("\n### asset info ###")
pp.pprint(hulk)
# 에셋 정보

preview_dict = gazu.files.get_preview_file(hulk['preview_file_id'])
print("\n### preview info ###")
pp.pprint(preview_dict)
# 대표 프리뷰 파일 하나의 정보

task_type_list = gazu.task.all_task_types_for_asset(hulk['id'])
print("\n### all task type info ###")
pp.pprint(task_type_list)
modeling = task_type_list[1]
# 에셋에 있는 모든 테스크 타입 정보

modeling_dict = gazu.task.get_task_by_name(hulk, modeling['id'])
print("\n### modeling task info ###")
pp.pprint(modeling_dict)
# 에셋에 있는 모델링 테스크의 인포

previews = gazu.files.get_all_preview_files_for_task(modeling_dict['id'])
print("\n### all preview files ###")
pp.pprint(previews)
# 에셋에 있는 모델링 테스크 안에 있는 프리뷰 파일들의 인포

path = os.getcwd()
# 현재 작업중인 py 파일 위치
for preview_item in previews:
    if preview_item['extension'] == 'obj':
        gazu.files.download_preview_file(preview_item['id'], path + "/hulk.obj")