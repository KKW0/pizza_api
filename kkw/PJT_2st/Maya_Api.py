
import os
import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView

from PySide2 import QtWidgets, QtCore, QtUiTools
from PySide2.QtWidgets import QDialog, QHeaderView, QLineEdit, QTableView, QVBoxLayout, QMainWindow, QAction, QTableWidgetItem, QTableWidget
from PySide2.QtGui import QStandardItemModel, QStandardItem

from Save import Save
from Load import Load
from main_widget import Widget
from main_widget import Widget2

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.save = None
        self.user_list_start = None
        ui_path = os.path.expanduser('/home/rapa/git/pizza/kkw/PJT_2st/Maya_Api.ui')
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)

        widget = Widget(self.read_data())
        widget.setFixedSize(600, 623)
        widget.setGeometry(QtCore.QRect(200, 10, 600, 623))  # Set the position and size of the Widget
        self.ui.Main_QGrid.addWidget(widget, 0, 0)

        widget2 = Widget2(self.read_data2())
        widget2.setFixedSize(320, 300)
        widget2.setGeometry(QtCore.QRect(0, 0, 320, 300))  # Set the position and size of the Widget2
        self.ui.Main_QGrid.addWidget(widget2, 1, 2)

        ui_file.close()

        '''
        # Save 클릭시 Save ui로 전환
        '''
        self.ui.Save_Button.clicked.connect(self.Save_Button)
        self.Save = Save()

        '''
        # Load 클릭시 Load ui로 전환
        '''
        self.ui.Load_Button.clicked.connect(self.Load_Button)
        self.Load = Load()

        # ----------------------------------------------------------------------------------------------

    class Table_widget(QMainWindow):
        def __init__(self, parent=None):
            super().__init__(parent)



    # ----------------------------------------------------------------------------------------------


    def Save_Button(self):
        self.hide()  # 메인 윈도우 숨김
        self.Save.ui.show()

    def Load_Button(self):
        self.hide()  # 메인 윈도우 숨김
        self.Load.ui.show()


    @staticmethod
    def read_data():
        data1 = {'country1': ('Avatar', 'Topgun', 'DontLookUp', 'Flash', 'Flash', 'Flash', 'Flash', 'Flash', 'Flash', 'Flash', 'Flash', 'Flash')}
        data2 = {'country2': ('Seq1', 'Seq2', 'Seq3', 'Seq4', 'Seq5', 'Seq6', 'Seq7', 'Seq8', 'Seq9', 'Seq10', 'Seq11', 'Seq12')}
        data3 = {'country3': ('Seq1', 'Seq2', 'Seq3', 'Seq4', 'Seq5', 'Seq6', 'Seq7', 'Seq8', 'Seq9', 'Seq10', 'Seq11', 'Seq12')}
        data4 = {'country4': ('Seq1', 'Seq2', 'Seq3', 'Seq4', 'Seq5', 'Seq6', 'Seq7', 'Seq8', 'Seq9', 'Seq10', 'Seq11', 'Seq12')}
        data5 = {'country5': ('Seq1', 'Seq2', 'Seq3', 'Seq4', 'Seq5', 'Seq6', 'Seq7', 'Seq8', 'Seq9', 'Seq10', 'Seq11', 'Seq12')}
        return data1, data2, data3, data4, data5

# ----------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------

    @staticmethod
    def read_data2():
        # data1 = {'country1': ('Avatar', 'Topgun', 'DontLookUp', 'Flash', 'Flash', 'Flash')}
        # data2 = {'country2': ('Seq1', 'Seq2', 'Seq3', 'Seq4', 'Seq5')}
        # data3 = {'country3': ('Seq1', 'Seq2', 'Seq3', 'Seq4', 'Seq5')}
        # data4 = {'country4': ('Seq1', 'Seq2', 'Seq3', 'Seq4', 'Seq5')}
        # data5 = {'country5': ('Seq1', 'Seq2', 'Seq3', 'Seq4', 'Seq5')}
        # return data1, data2, data3, data4, data5
        data = [
            ['/home/rapa/다운로드/1111.jpeg', 'Avata', '2023-03-02'],
            ['/home/rapa/다운로드/2222.jpeg', 'TopGun', '2023-03-03'],
            ['/home/rapa/다운로드/3333.jpeg', 'DontLookUp', '2023-03-04'],
            ['/home/rapa/다운로드/4444.jpeg', 'Flash', '2023-03-05'],
            ['/home/rapa/다운로드/1111.jpeg', 'DDong', '2023-03-06']
        ]
        return data



# ----------------------------------------------------------------------------------------------
def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    try:
        app = QtWidgets.QApplication().instance()
    except TypeError:
        app = QtWidgets.QApplication()
    myapp = MainWindow()
    myapp.ui.show()
    sys.exit(app.exec_())




# ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
