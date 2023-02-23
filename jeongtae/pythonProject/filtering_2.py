import gazu


class Filter:

    def __init__(self):
        self._project = None
        self._seq = None
        self._shot = None

    def select_task(self, num=0):
        task_list_user = gazu.user.all_tasks_to_do()

    def filtering_project(self, num=0):
        all_project = gazu.user.all_open_projects()

        if num == 0:
            select_project = all_project
        else:
            select_project = all_project[num - 1]
        self._project = select_project
        print("all proj")
        pp.pprint(self._project)

    def filtering_seq(self, num=0):
        seq_list = []
        if type(self._project) == list:
            project_list = self._project
            for project in project_list:
                seq = gazu.shot.all_sequences_for_project(project)
                seq_list.append(seq)
                gazu.shot.all_sequences_for_project
                gazu.entity.get_entity
        if num == 0:
            select_seq = seq_list
        else:
            select_seq = seq_list[num - 1]
        self._seq = select_seq