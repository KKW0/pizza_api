import gazu
import pprint as pp
import json


class Filter:

    def __init__(self):
        self.proj_set = None
        self.seq_set = None
        self.task = None

    def select_task(self):
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
        self.task = task_final_list
        # # ----------------- QT -------------
        # proj = proj_set[num]    # user clicked
        # seq = seq_set[num]
        # if proj == task_final_list['project_name']:

    def filter_check(self, task_list, value_list, num):
        filtered_task_list = []
        for task in task_list:
            if value_list[num] not in task:
                continue
            filtered_task_list.append(task)
        return filtered_task_list

    def filter_project(self, num=0):
        task_list = self.task
        project_list = self.proj_set
        filtered_project_list = self.filter_check(task_list, project_list, num)
        return filtered_project_list

    def filter_seq(self, value_list, num=0):
        seq_list = self.seq_set
        filtered_seq_list = self.filter_check(value_list, seq_list, num)
        return filtered_seq_list

