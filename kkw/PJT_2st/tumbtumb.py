#coding:utf8

import gazu
import pprint as pp
# from login import LogIn

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
        data(png): main preview의 사진
    """
    url = gazu.files.get_preview_file_url(preview)
    data = gazu.client.get_file_data_from_url(url)

    return data


def thumbnail_control(task_list, task_num=None, casting_info_list=None, undi_info_list=None):
    """

    Args:
        task_list(list): 사용자가 필터링한 테스크 딕셔너리의 집합
        task_num(int): 사용자가 선택한 테스크의 번호
        casting_info_list:
        undi_info_list:

    Returns:

    """
    # undi_thumbnail_list = []
    if task_num is None:
        layout_asset = gazu.entity.get_entity(task_list[0]['entity_id'])
        preview = gazu.files.get_preview_file(layout_asset['preview_file_id'])
        png = _get_thumbnail(preview)

        return png
        # 테스크 선택 전에는 첫번째 테스크의 메인 썸네일을 띄운다
    # else:
    #     for info in casting_info_list:
    #         # 캐스팅 썸네일
    #         proj = gazu.project.get_project(task['project_id'])
    #         asset = gazu.asset.get_asset_by_name(proj, info[0])
    #         preview = gazu.files.get_preview_file(asset['preview_file_id'])
    #         _get_thumbnail(preview)
    #
    #     for info in undi_info_list:
    #         # 언디스토션 썸네일
    #         shot = gazu.shot.get_shot(info['entity_id'])
    #         preview = gazu.files.get_preview_file(shot['preview_file_id'])
    #         undi_thumbnail_list.append(_get_thumbnail(preview))


project = gazu.project.get_project_by_name('jeongtae')
asset = gazu.asset.get_asset_by_name(project, 'chair')
task_status = gazu.task.get_task_status_by_name('Todo')
pre = gazu.files.get_preview_file(asset['preview_file_id'])

project = gazu.project.get_project_by_name('jeongtae')
asset = gazu.asset.get_asset_by_name(project, 'chair')
task_type = gazu.task.get_task_type_by_name('Layout_asset')
task_ = gazu.task.get_task_by_entity(asset, task_type)
thumbnail_control([task_])