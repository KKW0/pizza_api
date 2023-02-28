
import os
import sys
from PySide2 import QtWidgets, QtCore, QtUiTools



class Save(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.save = None
        self.user_list_start = None
        ui_path = os.path.expanduser('/home/rapa/git/pizza/kkw/PJT_2st/Save.ui')
        self.ui_file = QtCore.QFile(ui_path)
        self.ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(self.ui_file)
        self.ui_file.close()



        self.ui.Final_Save_Button.clicked.connect(self.Final_Save_Button)
        self.ui.Back_Button.clicked.connect(self.Back_Button)

    def Final_Save_Button(self):
        self.hide()  # 메인 윈도우 숨김
        print("저장했어 그만눌러")

    def Back_Button(self):
        self.hide()  # 메인 윈도우 숨김
        self.ui.close()

# ----------------------------------------------------------------------------------------------
def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication()
    myapp = Save()
    myapp.ui.show()
    sys.exit(app.exec_())


# ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
