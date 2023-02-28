#coding:utf8
import gazu
import pprint as pp


class Filter:
    def __init__(self):
        self._task = None
        gazu.client.set_host("http://192.168.3.116/api")
        gazu.log_in("pipeline@rapa.org", "netflixacademy")

    def sort_names_task(self, num=0):
        """
        task에서 필터링에 필요한 정보들을 추출하여 리스트에 넣고,
        필터링 대상인 proj와 seq는 따로 리스트를 만들어 추가로 저장한다
        그리고 유저가 클릭한 테스크를 변수에 저장한다.

        Args:
            num:

        Returns:

        """
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
        """
        선택한 task가 속한 seq에 casting된 에셋들의 정보 중 필요한 내용을 추출하여 저장한다.

        Args:
            num:

        Returns:

        """
        seq = gazu.shot.get_sequence(self._task['sequence_id'])
        all_casts = gazu.casting.get_sequence_casting(seq)
        all_casting_list = all_casts.values()
        info_list = []
        for casting_list in all_casting_list:
            for cast in casting_list:
                info_list.append([cast['name'], cast['nb_occurences'], cast['output_type']])
        selected_info = info_list[num]

