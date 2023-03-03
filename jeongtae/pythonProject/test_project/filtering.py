import gazu


class Filter:

    def __init__(self):
        self.proj_set = None
        self.seq_set = None
        self.todo_list = None

    def select_task(self):
        """
        status가 'todo'인 모든 테스크를 출력하여 이름이 중복되지 않은 프로젝트,시퀀스 리스트와
        project_name,sequence_name,due_date,description,last_comment 정보가 있는 todo_list를 리턴하는 매서드

        Returns:
            proj_set_list(list) : 프로젝트 목록 리스트
            seq_set_list(list) : 시퀀스 목록 리스트
            todo_list(list) : project_name, sequence_name, due_date, description, last_comment 리스트

        """
        task_list = gazu.user.all_tasks_to_do()
        proj_list = []
        seq_list = []
        task_final_list = []
        for task in task_list:
            proj_list.append(task['project_name'])
            seq_list.append(task['sequence_name'])
            task_final_list.append([task['project_name'], task['sequence_name'], task['due_date'], task['description'],
                                    task['last_comment']])

        self.proj_set = list(set(proj_list))
        self.seq_set = list(set(seq_list))
        self.todo_list = task_final_list

    def filter_check(self, task_list, selected_list, num):
        """
        task_list안에 들어있는 리스트에 selected_list의 'num'번째 인덱스 값이 포함된다면 filtered_task_list에 리스트를 추가하는 메서드

        Args:
            task_list(list): status가 'todo'인 테스크 리스트
            selected_list(list): 필터체크 목록 리스트
            num(int): 필터체크 목록 인덱스 값

        Returns:
            filtered_task_list(list): 필터가 완료된 리스트

        """
        filtered_task_list = []
        for task in task_list:
            if selected_list[num] not in task:
                continue
            filtered_task_list.append(task)
        return filtered_task_list

    def filter_project(self, num=0):
        """
        project_list[num]와 일치하는 todo 리스트를 필터체크하여 필터가 완료된 새로운 리스트를 리턴하는 매서드

        Args:
            num(int): 프로젝트 목록을 선택할 인덱스 값

        Returns:
            filtered_project_list(list): 선택한 프로젝트로 필터가 완료된 todo 리스트

        """
        final_task_list = self.todo_list
        project_list = self.proj_set
        filtered_project_list = self.filter_check(final_task_list, project_list, num)
        return filtered_project_list

    def filter_seq(self, selected_list, num=0):
        """
        seq_list[num]와 일치하는 선택한 todo 리스트를 필터체크하여 필터가 완료된 새로운 리스트를 리턴하는 매서드

        Args:
            selected_list: 선택한 todo 리스트
            num: 시퀀스 목록을 선택할 인덱스 값

        Returns:
            filtered_seq_list(list): 선택한 시퀀스로 필터가 완료된 todo 리스트

        """
        seq_list = self.seq_set
        filtered_seq_list = self.filter_check(selected_list, seq_list, num)
        return filtered_seq_list
