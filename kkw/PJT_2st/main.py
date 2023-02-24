import os
import sys
from PySide2 import QtWidgets, QtCore, QtUiTools

# from task_windows import App2

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.save = None
        self.user_list_start = None
        ui_path = os.path.expanduser('/home/rapa/git/pizza/kangkyoungwook/PJT_2st/Maya_Api.ui')
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.ui.show()

        # (sort 부분 pyside2에서 sort부분 체크해줘야함)

        # 아이템의 리스트 1 2 3 을 정의하고 item_list라는 목록으로 결합
        item1 = ['Rabbit', '2023-02-23', 'todo', '1']
        item2 = ['Dog', '2023-02-22', 'done', '2']
        item3 = ['Cat', '2023-02-21', 'ing', '3']
        item_list = [item1, item2, item3]

        # 'tableWidget' 객체에서 'setRowCount()' 메서드를 호출하여 테이블의 행 수를 'item_list'의 길이와 같게 설정합니다.
        self.ui.tableWidget.setRowCount(len(item_list))

        # 바깥쪽 루프는 'item_list' 내 각 목록을 반복하고, 안쪽 루프는 각 목록 내 각 값을 반복합니다.
        # 'setItem()' 메서드가 'tableWidget' 객체에서 호출되어 현재 셀의 값을 'item'의 현재 값으로 설정합니다.
        for row, item in enumerate(item_list):
            for col in range(4):
                self.ui.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(item[col]))

# ----------------------------------------------------------------------------------------------
def main():
    app = QtWidgets.QApplication(sys.argv)
    myapp = App()
    myapp.ui.show()
    sys.exit(app.exec_())


# ----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
