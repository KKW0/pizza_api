import os
import sys
from PySide2 import QtWidgets, QtCore, QtUiTools

class App3(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.combo = None
        self.combo2 = None
        self.save = None
        self.user_list_start = None
        ui_path = os.path.expanduser('/home/rapa/git/pizza/kangkyoungwook/PJT_test1/load_windows.ui')
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.File_ListBox()
        self.File_ListBox_2()

    # ----------------------------------------------------------------------------------------------
    def File_ListBox(self):
        self.combo = QtWidgets.QComboBox(self.ui)
        self.combo.addItem("1")
        self.combo.addItem("2")
        self.combo.addItem("3")
        self.combo.setGeometry(QtCore.QRect(215, 204, 90, 28))

    def File_ListBox_2(self):
        self.combo2 = QtWidgets.QComboBox(self.ui)
        self.combo2.addItem("4")
        self.combo2.addItem("5")
        self.combo2.addItem("6")
        self.combo2.setGeometry(QtCore.QRect(215, 238, 90, 28))


# ----------------------------------------------------------------------------------------------
def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)
    myapp = App3()
    myapp.ui.show()
    sys.exit(app.exec_())


# ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
