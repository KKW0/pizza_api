#coding:utf8

'''
호키 : 345kcal / 100g -> 16g 이하 (조단백 37, 조지방 10, 수분 12)
트라이벌 : 388.6kcal / 100g (조단백 20.5, 조지방 14.5, 수분 10)
지위픽 : 125kcal / 100g (조단백 9, 조지방 5.5, 수분 78)
'''

import gazu
from login import LogIn

"""
Kitsu에 로그인한 상태에서 task entity(레이아웃 에셋)의 메인 프리뷰 url을 구하고,
구한 url에서부터 데이터를 받아오는 모듈
"""

gazu.client.set_host("http://192.168.3.116/api")
gazu.log_in("pipeline@rapa.org", "netflixacademy")


def _get_thumbnail(preview):
    """
    Kitsu에서 썸네일 데이터를 받아오는 매서드

    Args:
        preview(dict): main preview의 딕셔너리

    Returns:
        data(dict): main preview의 정보값
    """
    url = gazu.files.get_preview_file_url(preview)
    data = gazu.client.get_file_data_from_url(url)

    return data


# def thumbnail_control(task, task_num, casting_info_list, undi_info_list):
#     undi_thumbnail_list = []
#     if task_num is 0:
#         entity = gazu.entity.get_entity[task[0]['entity_id']]
#         preview = gazu.files.get_preview_file(entity['preview_file_id'])
#         _get_thumbnail(preview)
#         # 테스크 선택 전에는 첫번째 테스크의 메인 썸네일을 띄운다
#     else:
#         for info in casting_info_list:
#             # 캐스팅 썸네일
#             proj = gazu.project.get_project(task['project_id'])
#             asset = gazu.asset.get_asset_by_name(proj, info[0])
#             preview = gazu.files.get_preview_file(asset['preview_file_id'])
#             _get_thumbnail(preview)
#
#         for info in undi_info_list:
#             # 언디스토션 썸네일
#             shot = gazu.shot.get_shot(info['entity_id'])
#             preview = gazu.files.get_preview_file(shot['preview_file_id'])
#             undi_thumbnail_list.append(_get_thumbnail(preview))

project = gazu.project.get_project_by_name('jeongtae')
asset = gazu.asset.get_asset_by_name(project, 'chair')
task_status = gazu.task.get_task_status_by_name('Todo')
task_type = gazu.task.get_task_type_by_name('Layout_asset')
task = gazu.task.get_task_by_entity(asset, task_type)
# pp.pprint(asset)
pre = gazu.files.get_preview_file(asset['preview_file_id'])
# pp.pprint(pre)

_get_thumbnail(pre)
