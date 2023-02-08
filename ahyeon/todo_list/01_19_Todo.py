import os
import sys
from PySide2 import QtWidgets, QtCore, QtUiTools


class InputDialog(QtWidgets.QDialog):
    text = ""

    def __init__(self):
        super().__init__()
        ui_path = os.path.expanduser('~/TEST/Qt/01_19_input_popup.ui')
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.ui.btn_cancel.clicked.connect(self.close)
        self.ui.btn_ok.clicked.connect(self.save)

    def close(self):
        self.ui.lineEdit.setText("")
        self.ui.close()

    def save(self):
        InputDialog.text = self.ui.lineEdit.text()
        if InputDialog.text == "":
            QtWidgets.QMessageBox.warning(self, "오류", "내용을 입력해주세요.")
        else:
            QtWidgets.QMessageBox.information(self, "완료", "저장되었습니다.")
            self.ui.lineEdit.setText("")
            self.ui.close()


class MyApp(QtWidgets.QMainWindow, InputDialog):
    def __init__(self):
        super().__init__()
        # InputDialog는 super 적용 안됨
        ui_path = os.path.expanduser('~/TEST/Qt/01_19.ui')
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.ui.show()

        self.path = os.path.expanduser('~/To_Do_list.txt')
        self.todo_list = []
        self.open_list()

        self.connect_button()
        self.dialog = InputDialog()

    def call_dialog(self):
        clicked = int(self.ui.listWidget.currentRow())
        self.dialog.ui.exec()
        text = InputDialog.text

        return clicked, text

    def open_list(self):
        """
        To Do 리스트 파일을 열어서 기존 내용을 불러오는 함수
        파일이 없다면 생성한다.
        todo_list에 불러온 내용을 저장하고, listWidget에도 표시한다.
        """
        self.ui.listWidget.clear()
        if os.path.exists(self.path) is False:
            with open(self.path, 'w') as f:
                print("* 파일이 생성되었습니다. \n")
        with open(self.path, 'r') as f:
            lines = f.readlines()
            if lines:
                for index, item in enumerate(lines):
                    self.todo_list.append(lines[index].strip('\n'))
                    self.ui.listWidget.addItem(item)
            else:
                print("* 내용이 없습니다. \n")

    def btn_add(self):
        """
        리스트에 내용을 추가하는 함수
        """
        _, text = self.call_dialog()
        self.ui.listWidget.addItem(text)

    def btn_edit(self):
        """
        리스트 항목 하나의 내용을 수정하는 함수
        """
        clicked, text = self.call_dialog()
        self.ui.listWidget.insertItem(clicked, text)
        self.ui.listWidget.takeItem(clicked + 1)

    def btn_del(self):
        """
        리스트 항목 하나를 삭제하는 함수
        """
        clicked = int(self.ui.listWidget.currentRow())
        self.ui.listWidget.takeItem(clicked)

    def btn_finish(self):
        """
        리스트 항목 옆에 완료 체크를 하는 함수
        """
        clicked = int(self.ui.listWidget.currentRow())
        item = self.ui.listWidget.takeItem(clicked)
        text = item.text()
        if ' #완료' in text:
            text = text.strip(' #완료')
            self.ui.listWidget.insertItem(clicked, text)
        else:
            self.ui.listWidget.insertItem(clicked, text + ' #완료')

    def btn_up(self):
        """
        리스트 인덱스 순서를 올리는 함수
        """
        clicked = self.ui.listWidget.currentRow()
        if clicked == 0:
            pass
        else:
            item = self.ui.listWidget.takeItem(clicked)
            self.ui.listWidget.insertItem(clicked-1, item)
            current = self.ui.listWidget.item(clicked-1)
            self.ui.listWidget.setCurrentItem(current)

    def btn_down(self):
        """
        리스트 인덱스 순서를 내리는 함수
        """
        clicked = self.ui.listWidget.currentRow()
        if clicked == self.ui.listWidget.count():
            pass
        else:
            item = self.ui.listWidget.takeItem(clicked)
            self.ui.listWidget.insertItem(clicked+1, item)
            current = self.ui.listWidget.item(clicked+1)
            self.ui.listWidget.setCurrentItem(current)

    def btn_save(self):
        """
        텍스트 파일을 저장하는 함수
        """
        for index in range(self.ui.listWidget.count()):
            text = self.ui.listWidget.item(index)
            self.todo_list.append(text.text())

        with open(self.path, 'w') as f:
            for item in self.todo_list:
                f.write(item + '\n')
        QtWidgets.QMessageBox.information(self,
                                          "home/rapa/To_Do_list.txt",
                                          "저장이 완료되었습니다.")

    def connect_button(self):
        self.ui.btn_add.clicked.connect(self.btn_add)
        self.ui.btn_edit.clicked.connect(self.btn_edit)
        self.ui.btn_del.clicked.connect(self.btn_del)
        self.ui.btn_finish.clicked.connect(self.btn_finish)
        self.ui.btn_save.clicked.connect(self.btn_save)
        self.ui.btn_up.clicked.connect(self.btn_up)
        self.ui.btn_down.clicked.connect(self.btn_down)


def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication()
    myapp = MyApp()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
