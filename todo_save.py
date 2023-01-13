import os
import argparse

class ToDoList():
    def __init__(self):
        self.todo_list = []

    def print_help(self):
        return '''
        To Do 리스트를 추가하고 .txt로 저장할 수 있는 툴입니다.
        올바른 명령어를 입력하시거나 헬프 페이지를 읽어주세요!
        ex) python 01_12.py -h
        '''  

    def open_list(self, path):
        '''
        To Do 리스트 파일을 열어서 내용을 볼 수 있는 함수
        파일이 없다면 생성한다.
        '''
        if os.path.exists(path) == False:
            with open(path, 'w') as f:
                print("파일이 생성되었습니다. \n")
        print("[ 저장된 To Do 리스트 목록 ] \n")
        with open(path, 'r') as f:
            lines = f.readlines()
            if lines:
                for i in range(len(lines)):
                    print(f'{i} : {lines[i]}')
            else:
                print("내용이 없습니다. \n")
        self.select_args(path)

    def print_list(self):
        print("[ 현재 To Do 리스트 목록 ] \n")
        if not self.todo_list :
            print('*** 해야 할 일 목록이 없습니다. ***')
            return 'none'
        else:
            for i, j in enumerate(self.todo_list):
                print(f"{i} : {self.todo_list[i]}")

    def add_list(self, path):
        '''
        리스트에 내용을 추가하는 함수
        '''
        self.print_list()
        do = input("더 해야하는 일을 입력해주세요 : ")
        self.todo_list.append(do)
        print("항목 추가가 완료되었습니다. \n")
        self.print_list()
        self.select_args(path)

    def edit_list(self, path):
        '''
        리스트 항목 하나의 내용을 수정하는 함수
        '''
        isnone = self.print_list()
        if isnone == 'none':
            print('수정할 내용이 없습니다.\n')
            self.select_args(path)
        else:
            number = int(input("수정을 원하는 번호를 입력해주세요 : "))
            do = input("새로 쓸 내용을 입력해주세요 : ")
            for i in range(len(self.todo_list)):
                    # enumerate 쓰면 i에는 인덱스, j에는 내용이 들어감
                    if i == number:
                        self.todo_list[i] = do
            print("항목 수정이 완료되었습니다. \n")
            self.select_args(path)
    
    def delete_list(self, path):
        '''
        리스트 항목 하나를 삭제하는 함수
        '''
        isnone = self.print_list()
        if isnone == 'none':
            print('삭제할 내용이 없습니다.\n')
            self.select_args(path)
        else:
            number = int(input("삭제를 원하는 번호를 입력해주세요 : "))
            for i in range(len(self.todo_list)):
                if i == number:
                    del self.todo_list[i]
            print("삭제가 완료되었습니다. \n")
            self.select_args(path)
    
    def list_done(self, path):
        '''
        리스트 항목 옆에 완료 체크를 하는 함수
        '''
        isnone = self.print_list()
        if isnone == 'none':
            print('완료할 내용이 없습니다.\n')
            self.select_args(path)
        else:
            number = int(input("완료한 번호를 입력해주세요 : "))
            for i, j in enumerate(self.todo_list):
                if i == number:
                    self.todo_list[i] = (j.strip('\n') + ' #완료')
            print(f"{number}번 항목이 완료되었습니다. \n")
            self.select_args(path)

    def save_text(self, path):
        '''
        텍스트 파일을 저장하고 종료하는 함수
        '''
        self.print_list()
        yn = input("To Do 리스트를 .txt 파일로 저장하시겠습니까? y/n : ")
        if yn == 'y':
            with open(path, 'w') as f:
                for i in self.todo_list:
                    f.write(i+'\n')
            print("저장이 완료되었습니다. 프로그램을 종료합니다. \n")
            return 'y'
        elif yn == 'n':
            return
        else:
            print('y 또는 n을 입력해주세요. \n')

    def arg_parse(self):
        parser = argparse.ArgumentParser(description="To Do 리스트 사용법", epilog="일을 잘 합시다")
        # 초기화, 우리가 만든 프로그램 설명 넣을 수 있음. -h 치면 나오는 헬프문의 시작과 끝.

        # 아규먼트 만들기. 별명, 풀네임, 스위치(써지면 true)로 설정, 필수로 써야하는 아규먼트는 아님, 헬프문 설정
        parser.add_argument("-o", "--open", action='store_true', help="Open my To_Do_List.txt file")   
        parser.add_argument("-a", "--add", action='store_true', help="Add a list to my To Do List")
        parser.add_argument("-e", "--edit", action='store_true', help="Edit a list in my To Do List")
        parser.add_argument("-d", "--delete", action='store_true', help="Delete a list in my To Do List")
        parser.add_argument("-f", "--finish", action='store_true', help="Finish a list in my To Do List")
        parser.add_argument("-s", "--save", action='store_true', help="Save my To Do List to .txt file and quit program")

        args = parser.parse_args()
        # 위에 추가해준 아규먼트들을 args에 넣어줌
        return args
    
    def select_args(self, path):
        '''
        다음에 할 일 물어보는 함수
        '''
        while True:
            print('''
            [ 사용 가능한 명령어 ]
            o : Open my To_Do_List.txt file
            a : Add a list to my To Do List
            e : Edit a list in my To Do List
            d : Delete a list in my To Do List
            f : Finish a list in my To Do List
            s : Save my To Do List to .txt file and quit program
            ''')
            do = input("\n무엇을 하시겠습니까? : ")
            if do == 'o':
                self.open_list(path)
                break
            elif do == 'a':
                self.add_list(path)
                break
            elif do == 'e':
                self.edit_list(path)
                break
            elif do == 'd':
                self.delete_list(path)
                break
            elif do == 'f':
                self.list_done(path)
                break
            elif do == 's':
                yn = self.save_text(path)
                if yn == 'y':
                    break
            else:
                print('명령어가 존재하지 않습니다. \n')

    def run_program(self, args, path):
            if args.open:
                self.open_list(path)
            elif args.add:
                self.add_list(path)
            elif args.edit:
                self.edit_list(path)
            elif args.delete:
                self.delete_list(path)
            elif args.finish:
                self.list_done(path)
            elif args.save:
                self.save_text(path)
                return
            else:
                print(self.print_help())
                return

def main():
    todo = ToDoList()
    args = todo.arg_parse()
    path = '/home/rapa/TEST/VScode/To_Do_List.txt'
    todo.run_program(args, path)

if __name__ == "__main__" :
    main()