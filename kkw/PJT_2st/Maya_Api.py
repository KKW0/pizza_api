
import os
import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView

from PySide2 import QtWidgets, QtCore, QtUiTools
from PySide2.QtWidgets import QDialog, QHeaderView, QLineEdit, QTableView, QVBoxLayout, QMainWindow, QAction, QTableWidgetItem, QTableWidget
from PySide2.QtGui import QStandardItemModel, QStandardItem

from PySide2.QtWidgets import QApplication, QTableWidget, QTableWidgetItem

from Save import Save
from Load import Load
from main_widget import Widget
from main_widget import Widget2

from table_model import CustomTableModel

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

        self.widget = Widget(self.read_data())
        self.widget.setFixedSize(700, 615)
        self.widget.setGeometry(QtCore.QRect(0, 0, 700, 615))  # Set the position and size of the Widget

        self.ui.Main_QGrid.addWidget(self.widget, 0, 0)

        # self.widget.horizontalHeader().setDefaultSectionSize(100)
        self.widget.horizontalHeader().setMinimumSectionSize(100)
        # self.widget.verticalHeader().setDefaultSectionSize(35)
        self.widget.verticalHeader().setMinimumSectionSize(35)

        self.widget2 = Widget2(self.read_data2())
        self.widget2.setFixedSize(320, 300)
        self.widget2.setGeometry(QtCore.QRect(0, 0, 320, 300))  # Set the position and size of the Widget2
        self.ui.Main_QGrid.addWidget(self.widget2, 1, 2)

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


        # Event
        self.widget.clicked.connect(self.widget_clicked)
        # ----------------------------------------------------------------------------------------------

    def widget_clicked(self, event):
        selected_data = self.read_data()[event.row()]
        print(selected_data)

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
        data = [
            ['Avata', '1', '2023-03-02', '123', 'abcd'],
            ['TopGun', '2', '2023-03-03', '456', 'efgh'],
            ['DontLookUp', '3', '2023-03-04', '789', 'ijkl'],
            ['Flash', '4', '2023-03-05', '456', 'mnop'],
            ['DDong', '5', '2023-03-06', '123', 'qrstu'],
            ['DDong', '6', '2023-03-06', '123', 'qrstu'],
            ['DDong', '7', '2023-03-06', '123', 'qrstu'],
            ['DDong', '8', '2023-03-06', '123', 'qrstu'],
            ['DDong', '9', '2023-03-06', '123', 'qrstu'],
            ['DDong', '10', '2023-03-06', '123', 'qrstu'],
            ['DDong', '11', '2023-03-06', '123', 'qrstu'],
            ['DDong', '12', '2023-03-06', '123', 'qrstu'],
            ['DDong', '13', '2023-03-06', '123', 'qrstu'],
            ['DDong', '14', '2023-03-06', '123', 'qrstu'],
            ['DDong', '15', '2023-03-06', '123', 'qrstu'],
            ['DDong', '16', '2023-03-06', '123', 'qrstu'],
            ['DDong', '17', '2023-03-06', '123', 'qrstu'],
            ['DDong', '18', '2023-03-06', '123', 'qrstu'],
            ['DDong', '19', '2023-03-06', '123', 'qrstu'],
            ['DDong', '20', '2023-03-06', '123', 'qrstu']
        ]
        return data

# ----------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------

    @staticmethod
    def read_data2():
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
