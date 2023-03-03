#coding:utf8

import gazu
# from PySide2 import QtGui, QtWidgets

"""
Kitsu에 로그인 후 task entity의 메인 프리뷰의 url을 구하고,
구한 url에서부터 데이터를 받아온다.
"""


def _get_thumbnail(preview):
    # Load image from URL
    url = gazu.files.get_preview_file_url(preview)
    data = gazu.client.get_file_data_from_url(url)

    return data


def thumbnail_control(task, task_num, task_type, casting_info_list, undi_info_list):
    undi_thumbnail_list = []
    if task_num is 0:
        _get_thumbnail(task[0]['entity_preview_file_id'])
        # 테스크 선택 전에는 첫번째 테스크의 메인 썸네일을 띄운다
    else:
        for info in casting_info_list:
            # 캐스팅 썸네일
            proj = gazu.project.get_project(task['project_id'])
            asset = gazu.asset.get_asset_by_name(proj, info[0])
            preview = gazu.files.get_preview_file(asset['preview_file_id'])
            _get_thumbnail(preview)

        for info in undi_info_list:
            # 언디스토션 썸네일
            shot = gazu.shot.get_shot(info['entity_id'])
            task_for_shot = gazu.task.get_task_by_entity(shot, task_type)
            preview = gazu.files.get_preview_file(task_for_shot['entity_preview_file_id'])
            undi_thumbnail_list.append(_get_thumbnail(preview))


# # Create application
# app = QtWidgets.QApplication.instance(sys.argv)
#
# # Create pixmap from image data
# pixmap = QtGui.QPixmap()
# pixmap.loadFromData(data)
#
# # Create label to display image
# label = QtWidgets.QLabel()
# label.setPixmap(pixmap)
# label.show()
#
# # Run application event loop
# sys.exit(app.exec_())
