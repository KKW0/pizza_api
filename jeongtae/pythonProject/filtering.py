import gazu

class Fillter:

    def __init__(self):
        self._project = None
        self._seq = None
        self._shot = None
        self._user = None

    @property
    def user_name(self):
        return self._user

    @user_name.setter
    def user_name(self, value):
        self._user = value

    def filtering_project(self, num=0):
        user_name = self._user
        person_name = gazu.person.get_person_by_full_name(user_name)
        task_list_user = gazu.user.all_tasks_to_do()
        all_project = gazu.project.all_projects()
        filtered_task_list = []
        project_list = []

        for task in task_list_user:
            if task['assignees'][0] != person_name['id']:
                continue
            if task['task_status_name'] not in 'Todo':
                continue
            filtered_task_list.append(task)

        for task, project in zip(filtered_task_list, all_project):
            if task.get['project_id'] != project['id']:
                continue
            if project not in project_list:
                continue
            project_list.append(project)
        if num == 0:
            select_project = project_list
        else:
            select_project = project_list[num - 1]
        self._project = select_project

    def filtering_seq(self, num=0):
        seq_list = []
        project_list = self._project
        for project in project_list:
            seq = gazu.shot.all_sequences_for_project(project)
            seq_list.append(seq)
        if num == 0:
            select_seq = seq_list
        else:
            select_seq = seq_list[num - 1]
        self._seq = select_seq

    def filtering_shot(self, num=0):
        shot_list = []
        sequence_list = self._seq
        for seq in sequence_list:
            shot = gazu.shot.all_shots_for_sequence(seq)
            shot_list.append(shot)
        if num == 0:
            select_shot = shot_list
        else:
            select_shot = shot_list[num - 1]
        self._shot = select_shot
