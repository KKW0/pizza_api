#coding:utf8

import gazu
import pprint as pp

"""
Kitsu에 로그인한 상태에서 task entity(레이아웃 에셋)의 메인 프리뷰 url을 구하고,
구한 url에서부터 데이터를 받아오는 모듈
"""


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


def thumbnail_control(task_dict, task_num=None, casting_info_list=None, undi_info_list=None):
    """

    Args:
        task_dict(dict): 사용자가 선택한 테스크, 또는 필터링한 테스크 딕셔너리의 집합
                                      task_num의 타입이 int면 딕셔너리, None이면 리스트 타입이다.
        task_num(int): 사용자가 선택한 테스크의 인덱스 번호. 사용자가 task를 선택하기 전에는 None
        casting_info_list(list): 사용자가 task를 선택하기 전에는 None
                                [asset_name, description, asset_type_name, nb_occurences]
        undi_info_list(list): 사용자가 task를 선택하기 전에는 None
                             [output file name, output type name, comment, description, entity_id]

    Returns:
        png: 메인 썸네일의 png
        list: 캐스팅된 에셋들의 썸네일 png의 집합
        png: 언디스토션 이미지의 썸네일

    """
    if task_num is None:
        # 테스크 선택 전에는 아무것도 하지 않는다.
        return None
    else:
        # 테스크 선택 시 선택한 테스크의 메인 썸네일과 캐스팅 목록의 썸네일들을 return 한다.
        asset_thumbnail_list = []
        undi_thumbnail_list = []
        layout_asset = gazu.entity.get_entity(task_dict['entity_id'])
        preview = gazu.files.get_preview_file(layout_asset['preview_file_id'])
        png = _get_thumbnail(preview)
        for info in casting_info_list:
            # 캐스팅된 에셋들의 썸네일
            proj = gazu.project.get_project(task_dict['project_id'])
            asset = gazu.asset.get_asset_by_name(proj, info['asset_name'])
            if asset['preview_file_id']:
                preview_cast = gazu.files.get_preview_file(asset['preview_file_id'])
                data = _get_thumbnail(preview_cast)
            else:
                data = None
            asset_thumbnail_list.append(data)
        # 언디스토션 이미지의 프리뷰. Matchmove 팀이 올린 프리뷰들 중 가장 최근 것.
        if len(undi_info_list) == 0:
            return png, asset_thumbnail_list, undi_thumbnail_list, None
        else:
            task_type = gazu.task.get_task_type_by_name('Matchmove')
            shot_list = gazu.casting.get_asset_cast_in(layout_asset)
            for shot in shot_list:
                task = gazu.task.get_task_by_entity(shot['shot_id'], task_type)
                previews = gazu.files.get_all_preview_files_for_task(task)
                png = _get_thumbnail(previews[0])
                undi_thumbnail_list.append(png)
            return png, asset_thumbnail_list, undi_thumbnail_list, shot_list

        # 카메라는 썸네일 없음

