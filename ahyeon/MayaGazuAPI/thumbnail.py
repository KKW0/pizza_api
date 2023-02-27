#coding:utf8

import sys
import gazu
import urllib
from PySide2 import QtGui, QtWidgets

# Create application
app = QtWidgets.QApplication(sys.argv)

# Load image from URL
url = gazu.files.get_preview_file_url(main_preview)

data = gazu.client.get_file_data_from_url(url)

# Create pixmap from image data
pixmap = QtGui.QPixmap()
pixmap.loadFromData(data)

# Create label to display image
label = QtWidgets.QLabel()
label.setPixmap(pixmap)
label.show()

# Run application event loop
sys.exit(app.exec_())