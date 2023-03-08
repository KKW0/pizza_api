from PySide2 import QtWidgets, QtCore, QtUiTools
from Maya_Api import MainWindow


def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    try:
        app = QtWidgets.QApplication().instance()
    except TypeError:
        app = QtWidgets.QApplication(sys.argv)
    myapp = MainWindow()
    # myapp.ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()