#coding:utf8
import gazu
import pprint as pp


class Filter:
    def __init__(self):
        self._task = None

    def sort_names_task(self, num=0):
        task_list = gazu.user.all_tasks_to_do()
        proj_list = []
        seq_list = []
        final_task_list = []
        for task in task_list:
            proj_list.append(task['project_name'])
            seq_list.append(task['sequence_name'])
            final_task_list.append([task['project_name'], task['sequence_name'], task['due_date'],
                                    task['description'], task['last_comment']])

        proj_set = list(set(proj_list))
        seq_set = list(set(seq_list))
        self._task = task_list[num]

    def sort_names_output(self, num=0):
        seq = gazu.shot.get_sequence(self._task['sequence_id'])
        all_casts = gazu.casting.get_sequence_casting(seq)
        casting_list = all_casts.values()
        info_list = []
        for casts in casting_list:
            for cast in casts:
                info_list.append([cast['name'], cast['nb_occurences'], cast['output_type']])