#coding:utf8

import pprint as pp
import sys
import gazu
from PySide2 import QtGui, QtWidgets

"""
Kitsu에 로그인 후 task의 메인 프리뷰의 프리뷰 파일 url을 구하고,
구한 url에서부터 데이터를 받아온다.
"""

def get_thumbnail(task):
    # Load image from URL
    url = gazu.files.get_preview_file_url(task['entity_preview_file_id'])
    data = gazu.client.get_file_data_from_url(url)

    return data


# Create application
app = QtWidgets.QApplication(sys.argv)

# Create pixmap from image data
pixmap = QtGui.QPixmap()
pixmap.loadFromData(data)

# Create label to display image
label = QtWidgets.QLabel()
label.setPixmap(pixmap)
label.show()

# Run application event loop
sys.exit(app.exec_())
