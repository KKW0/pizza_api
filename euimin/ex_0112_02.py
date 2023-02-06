
tasks = []

def add_task(task):
    """
    task 를 tasks 에 넣는 함수
    """
    tasks.append(task)
    return

def complete_task(index):
    """
    완료된 task를 tasks 에서 지우는 함수
    """
    index = int(index)
    del tasks[index]
    # tasks.remove(task)
    return

def list_tasks():
    """
    task들의 리스트를 출력 하는 함수
    """    
    for task in tasks:
        print(task)
    return
        
        
def main():
    """
    실행 함수
    """
    while True:
        add_task(task = input("오늘 할 일을 입력하시오: "))
        print ("오늘 할 일 은 : %s" %tasks + "입니다.")
        add_yn = input("추가할 목록이 있습니까? (y/n)")
        if add_yn == 'n':
            break
        #     add_task(task = input("할 일을 입력하시오: "))
        #     print ("오늘 할 일 들은 : %s" %tasks + "입니다.")
        # return

    while True:
        complete_yn = input("완료한 목록이 있습니까? (y/n)")
        if complete_yn == 'y':
            print ("현재 할일 목록은 다음과 같습니다 : ")
            for index, task in enumerate(tasks):
                print(index, task)
            complete_task(input("완료한 목록의 순번을 입력하시오 :" ))
        else: 
            break
            
    
    # yn = input("완료한 목록이 있습니까? (y/n)")
    
    # if yn == 'y':
    #     complete_task(task = input("완료한 목록을 적으시오: "))
    #     list_tasks()
    # #     else:
    # #     yn == 'n'
    # return
    # # return

   

if __name__ == "__main__":
    main()




