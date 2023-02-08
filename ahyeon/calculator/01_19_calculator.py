# 계산기 만들기
import os
import sys
from PySide2 import QtWidgets, QtCore, QtUiTools


class MyApp(QtWidgets.QMainWindow):
    """
    계산기 .ui 파일을 로드하고 실행하는 클래스

    Args:
        QtWidgets.QMainWindow(library) : Qt라이브러리를 상속받는다
    """
    def __init__(self):
        """
        Qt를 로드하고 매서드를 버튼과 연결하며, 클래스 변수를 설정하는 매서드
        """

        # UI 설정
        super().__init__()
        # 부모 클래스의 __init__을 그대로 받아온다
        ui_path = os.path.expanduser('~/TEST/Qt/01_18.ui')
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file)
        # 로드한 Qt를 self.ui에 저장
        ui_file.close()
        # Qt 로더 종료
        self.ui.show()
        # UI 시각화

        # 클래스 변수 설정
        self.number = ""
        # 현재 입력 중인 숫자 저장
        self.tmp_num = ""
        # 직전 입력 숫자 저장
        self.choice = ''
        # 연산자 저장
        self.value = None
        # 결과값 저장

        # 버튼과 매서드 연결
        self.connect_num_btn()
        self.connect_cal_btn()

    def num_control(self):
        """
        self.tmp_num에 self.number의 값을 옮겨놓고,
        self.number를 빈 문자열로 초기화하는 매서드

        self.value가 None이 아니고 저장된 값이 있을 경우,
        self.tmp_num에 self.number 대신 연산 결과값을 저장한다.
        이를 통해 결과값에서 바로 연산자를 눌렀을 때에도 정상적으로 연산이 진행된다.
        """
        if self.value != None:
            self.tmp_num = self.value
        else:
            self.tmp_num = self.number
        self.number = ""

    def btn_clicked(self, num):
        """
        숫자 버튼이 클릭되면 self.number에 입력한 숫자를 추가로 저장하고,
        디스플레이 윈도우 2개에 출력하는 매서드

        self.number에 저장된 것이 없고, 0을 입력했을 경우(처음 입력한 숫자가 0일 경우),
        self.number는 빈 문자열로 유지한다.

        self.number에 저장된 문자열이 있고, 0이 아닌 다른 것을 입력했을 경우,
        self.number에 num을 추가한다.

        그리고 self.value를 None으로 초기화한다.

        Args:
            num(str): 사용자가 클릭한 숫자
        """
        self.value = None
        if self.number == "" and num == '0':
            self.number = ""
            self.ui.lcdNumber.display(num)
            self.ui.textBrowser.setText(num)
        else:
            self.number += num
            self.ui.lcdNumber.display(self.number)
            # tmp_string = str(self.tmp_num) + self.choice + str(self.number)
            # self.ui.textBrowser.setText(tmp_string)
            self.ui.textBrowser.setText(self.number)

    def calc_clicked(self, calc):
        """
        연산자 버튼이 눌렸을 때, self.choice에 해당 연산자를
        문자열 형태로 저장하고, 디스플레이 윈도우에 출력하는 매서드

        함수 실행 전 self.num_control()함수를 먼저 실행한다.

        Args:
            calc(str): 사용자가 누른 연산자 버튼
        """
        self.num_control()
        if calc == '+':
            self.choice = '+'
            self.ui.textBrowser.append('+')
        elif calc == '-':
            self.choice = '-'
            self.ui.textBrowser.append('-')
        elif calc == '*':
            self.choice = '*'
            self.ui.textBrowser.append('x')
        elif calc == '/':
            self.choice = '/'
            self.ui.textBrowser.append('/')
        elif calc == '%':
            self.choice = '%'
            self.ui.textBrowser.append('%')

    def del_clicked(self):
        """
        del 버튼이 클릭되었을 때, self.number의 마지막 문자를 삭제하는 매서드

        self.number에 문자열이 저장되어 있지 않다면, 아무것도 동작하지 않는다.
        """
        if self.number != "":
            self.number = self.number[:-1]
            self.ui.lcdNumber.display(self.number)
            self.ui.textBrowser.setText(self.number)
        else:
            return

    def c_clicked(self):
        """
        C 버튼이 클릭되었을 때, self.number와 self.tmp_num,
        self.value에 저장된 값을 초기화하는 매서드

        숫자 디스플레이 윈도우에는 0을 출력한다.
        """
        self.number = ""
        self.tmp_num = ""
        self.choice = ""
        self.value = None
        self.ui.lcdNumber.display(0)
        self.ui.textBrowser.setText(None)

    def dot_clicked(self):
        """
        . 버튼이 클릭되었을 때, self.number에 .을 추가하고, 디스플레이 2개에 출력하는 매서드

        만약 이미 . 이 클릭된 상황이면, Error를 커맨드창에 출력하고 종료한다.
        또한, self.number에 숫자가 입력된 상황이라면 . 만 추가하고,
        self.number가 빈 문자열이면, 0.을 추가한다.
        """
        if '.' in self.number:
            print("Error")
            return
        elif self.number != "":
                self.number += '.'
        else:
            self.number += '0.'
        self.ui.lcdNumber.display(float(self.number))
        self.ui.textBrowser.append(self.number)

    def pl_min_clicked(self):
        """
        self.number를 음수 또는 양수로 바꾸고, 디스플레이에 출력하는 매서드

        만약 self.value가 None이 아닌 상태라면,
        결과값에 바로 매서드 실행을 시도하고 있다는 의미이며 해당 기능은 지원하지 않기 때문에,
        Error를 출력한 뒤 종료한다.

        self.number가 빈 문자열이 아니면 저장된 숫자에 -1을 곱하여 새로 저장하고,
        빈 문자열이면 -를 추가한다.
        self.number에 소수가 저장되어 있다면 소수로 출력하고,
        정수 형태라면 그냥 출력한다.
        """
        if self.value != None:
            print("Error")
            return
        if self.number != "":
            num = int(self.number) * -1
            self.number = str(num)
        else:
            self.number += '-'
        if float(self.number).is_integer():
            self.ui.lcdNumber.display(int(self.number))
            self.ui.textBrowser.setText(str(int(self.number)))
        else:
            self.ui.lcdNumber.display(float(self.number))
            self.ui.textBrowser.setText(self.number)

    def value_clicked(self):
        """
        self.choice에 따라 self.tmp_num과 self.number로 연산을 하고,
        연산 결과를 self.value에 저장한 뒤 디스플레이에 출력하는 매서드

        (1)
        최하단에서 self.number를 self.tmp_num에 저장하고,
        self.number는 빈 문자열로 초기화하여,
        사용자가 결과값을 보고 바로 숫자를 눌렀을 때 문자열이 새로 입력되지 않는 오류를 방지한다.

        (2)
        최상단에서 만약 self.value에 이미 저장된 값이 있을 경우를 판별하여,
        value가 None이 아닐 경우 self.number에 self.tmp_num 값을 저장하고,
        (이 때, self.tmp_num은 최하단에서 수행한 (1)에 의해 self.number와 같은 값을 가진 상태다.)
        self.tmp_num에는 self.value를 저장하여, 직전 결과값에 직전 연산을 수행할 수 있게 한다.
        이를 통해 = 를 두번 이상 연속으로 눌렀을 경우 정상적으로 직전 연산이 반복된다.

        (3)
        연산 실행 전, self.value를 다시 None으로 초기화하여 오류를 방지한다.
        /, % 연산 시 분모가 0 등의 오류가 발생하면 오류 메세지를 출력하고,
        self.value에 분자의 값을 저장한다.
        연산자 지정 없이 = 를 눌렀을 경우, self.number를 숫자로 변환이 가능한지 체크하고,
        오류가 발생할 경우 에러 메세지를 출력하고 종료한다.
        """
        if self.value != None:
            self.number = self.tmp_num
            self.tmp_num = self.value

        self.value = None
        if self.choice == '+':
            self.value = float(self.tmp_num) + float(self.number)
        elif self.choice == '-':
            self.value = float(self.tmp_num) - float(self.number)
        elif self.choice == '*':
            self.value = float(self.tmp_num) * float(self.number)
        elif self.choice == '/':
            try:
                self.value = float(self.tmp_num) / float(self.number)
            except Exception as err:
                print(f"Error: {err}")
                self.value = float(self.tmp_num)
        elif self.choice == '%':
            try:
                self.value = float(self.tmp_num) % float(self.number)
            except Exception as err:
                print(f"Error: {err}")
                self.value = float(self.tmp_num)
        else:
            try:
                self.value = float(self.number)
            except Exception as err:
                print(f"Error: {err}")
                return

        if self.value.is_integer():
            self.ui.lcdNumber.display(int(self.value))
            self.ui.textBrowser.append("= " + str(int(self.value)))
        else:
            self.ui.lcdNumber.display(self.value)
            self.ui.textBrowser.append("= " + str(self.value))

        self.tmp_num = self.number
        self.number = ""

    # 괄호는... 하지 말자.
    # def bracket1_clicked(self):
    #     self.number += '('
    #
    # def bracket2_clicked(self):
    #     self.number += ')'

    def connect_cal_btn(self):
        """
        숫자 외 버튼을 각각의 매서드와 연결해주는 매서드
        """
        self.ui.pushButton_sum.clicked.connect(lambda: self.calc_clicked('+'))
        self.ui.pushButton_min.clicked.connect(lambda: self.calc_clicked('-'))
        self.ui.pushButton_mul.clicked.connect(lambda: self.calc_clicked('*'))
        self.ui.pushButton_div.clicked.connect(lambda: self.calc_clicked('/'))
        self.ui.pushButton_remain.clicked.connect(lambda: self.calc_clicked('%'))
        self.ui.pushButton_del.clicked.connect(self.del_clicked)
        self.ui.pushButton_c.clicked.connect(self.c_clicked)
        self.ui.pushButton_dot.clicked.connect(self.dot_clicked)
        self.ui.pushButton_plmin.clicked.connect(self.pl_min_clicked)
        self.ui.pushButton_value.clicked.connect(self.value_clicked)
        # self.ui.pushButton_bracket1.clicked.connect(self.bracket1_clicked)
        # self.ui.pushButton_bracket2.clicked.connect(self.bracket2_clicked)
        return

    def connect_num_btn(self):
        """
        숫자 버튼을 각각의 매서드와 연결해주는 매서드
        """
        self.ui.pushButton_1.clicked.connect(lambda: self.btn_clicked('1'))
        self.ui.pushButton_2.clicked.connect(lambda: self.btn_clicked('2'))
        self.ui.pushButton_3.clicked.connect(lambda: self.btn_clicked('3'))
        self.ui.pushButton_4.clicked.connect(lambda: self.btn_clicked('4'))
        self.ui.pushButton_5.clicked.connect(lambda: self.btn_clicked('5'))
        self.ui.pushButton_6.clicked.connect(lambda: self.btn_clicked('6'))
        self.ui.pushButton_7.clicked.connect(lambda: self.btn_clicked('7'))
        self.ui.pushButton_8.clicked.connect(lambda: self.btn_clicked('8'))
        self.ui.pushButton_9.clicked.connect(lambda: self.btn_clicked('9'))
        self.ui.pushButton_0.clicked.connect(lambda: self.btn_clicked('0'))
        return


def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication()
    MyApp()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
