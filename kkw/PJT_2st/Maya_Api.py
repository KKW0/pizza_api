
import os
import sys

from PySide2 import QtWidgets, QtCore, QtUiTools
from PySide2.QtWidgets import QDialog, QHeaderView, QLineEdit, QTableView, QVBoxLayout, QMainWindow, QAction, QTableWidgetItem, QTableWidget
from PySide2.QtGui import QStandardItemModel, QStandardItem

from Save import Save
from Load import Load
from main_widget import Widget


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



        self.ui.Main_QGrid.addWidget(Widget(self.read_data()), 0, 0)

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


    # ----------------------------------------------------------------------------------------------


    def Save_Button(self):
        self.hide()  # 메인 윈도우 숨김
        self.Save.ui.exec()

    def Load_Button(self):
        self.hide()  # 메인 윈도우 숨김
        self.Load.ui.exec()

    def read_data(self):
        data1 = {'country1': ('Avatar', 'Topgun', 'DontLookUp', 'Flash', 'Flash', 'Flash', 'Flash', 'Flash', 'Flash', 'Flash', 'Flash', 'Flash')}
        data2 = {'country2': ('Seq1', 'Seq2', 'Seq3', 'Seq4', 'Seq5', 'Seq6', 'Seq7', 'Seq8', 'Seq9', 'Seq10', 'Seq11', 'Seq12')}
        data3 = {'country2': ('Seq1', 'Seq2', 'Seq3', 'Seq4', 'Seq5', 'Seq6', 'Seq7', 'Seq8', 'Seq9', 'Seq10', 'Seq11', 'Seq12')}
        data4 = {'country2': ('Seq1', 'Seq2', 'Seq3', 'Seq4', 'Seq5', 'Seq6', 'Seq7', 'Seq8', 'Seq9', 'Seq10', 'Seq11', 'Seq12')}
        data5 = {'country2': ('Seq1', 'Seq2', 'Seq3', 'Seq4', 'Seq5', 'Seq6', 'Seq7', 'Seq8', 'Seq9', 'Seq10', 'Seq11', 'Seq12')}
        return data1, data2, data3, data4, data5

# ----------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------
def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication()
    myapp = MainWindow()
    myapp.ui.show()
    sys.exit(app.exec_())


# ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
