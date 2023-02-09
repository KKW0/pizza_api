#coding:utf8
import os
import sys
import csv
from PySide2 import QtWidgets, QtCore, QtUiTools

'''
# save_windows_yes_or_no
'''
from save_windows_yes_or_no import App4

class App2(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.combo = None
        self.combo2 = None
        self.save = None
        self.user_list_start = None
        ui_path = os.path.expanduser('/home/rapa/git/pizza/kangkyoungwook/PJT_test1/save_windows.ui')
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.File_ListBox()
        self.File_ListBox_2()

        '''
        # save 클릭시 save_windows_yes_or_no ui로 전환
        '''
        self.ui.Save_Button.clicked.connect(self.Save_Button)
        self.app4 = App4()

    # ----------------------------------------------------------------------------------------------

    '''
    # Working_File이 적용 되야하는부분
    '''
    def Working_File_CheckBox(self):
        pass

    '''
    # OutPut_File이 적용 되야하는부분
    '''
    def OutPut_File_CheckBox(self):
        pass

    '''
    # Working_File의 리스트가 적용 되야하는부분
    '''
    def File_ListBox(self):
        self.combo = QtWidgets.QComboBox(self.ui)
        self.combo.addItem("1")
        self.combo.addItem("2")
        self.combo.addItem("3")
        self.combo.setGeometry(QtCore.QRect(215, 204, 90, 28))

    '''
    # OutPut_File의 리스트가 적용 되야하는부분
    '''
    def File_ListBox_2(self):
        self.combo2 = QtWidgets.QComboBox(self.ui)
        self.combo2.addItem("4")
        self.combo2.addItem("5")
        self.combo2.addItem("6")
        self.combo2.setGeometry(QtCore.QRect(215, 238, 90, 28))


    '''
    # 주어진 저장 경로에 저장되며 키츄에 업데이트 할 부분
    '''
    def Save_Button(self):
        with open('/home/rapa/git/pizza/kangkyoungwook/PJT_test1/test.csv', 'w', encoding='utf-8', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([1, "a"])
            writer.writerow([2, "b"])
        f.close()
        f = open('/home/rapa/git/pizza/kangkyoungwook/PJT_test1/test.csv', 'r', encoding='utf-8')
        rdr = csv.reader(f)
        for line in rdr:
            print(line)
        f.close()

        self.app4.ui.exec()

# ----------------------------------------------------------------------------------------------
def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)
    myapp = App2()
    myapp.ui.show()
    sys.exit(app.exec_())


# ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
