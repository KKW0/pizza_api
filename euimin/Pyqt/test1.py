#coding:utf8
import sys
from PySide2.QtWidgets import QApplication, QWidget


class MyApp(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My First Application')
        self.move(300, 300)
        self.resize(400, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())