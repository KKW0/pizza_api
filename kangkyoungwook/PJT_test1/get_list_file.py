import os
import sys
from PySide2 import QtWidgets, QtCore, QtUiTools

class App5(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.combo = None
        self.combo2 = None
        self.save = None
        self.user_list_start = None
        ui_path = os.path.expanduser('/home/rapa/git/pizza/kangkyoungwook/PJT_test1/get_list_file.ui')
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.Yes_Button()
        self.No_Button()

        self.ui.Yes_Button.clicked.connect(self.Yes_Button)
        self.ui.No_Button.clicked.connect(self.No_Button)

    # ----------------------------------------------------------------------------------------------

    '''
    # 통과시키는 버튼
    '''
    def Yes_Button(self):
        pass

    '''
    # 취소시키는 버튼
    '''
    def No_Button(self):
        pass



# ----------------------------------------------------------------------------------------------
def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)
    myapp = App5()
    myapp.ui.show()
    sys.exit(app.exec_())


# ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
