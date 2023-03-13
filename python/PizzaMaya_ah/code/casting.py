#coding:utf-8
import os
import gazu
import pprint as pp

class MyGazu:
    """

    Gazu API와 상호 작용하기 위한 클래스입니다.

    이 클래스는 활성 프로젝트, 샷, 시퀀스, 자산 및 작업을 설정하고 새 항목을 생성하는 방법을 제공합니다.
    작업을 수행하고 팀 구성원에게 할당합니다. Gazu Python 클라이언트 라이브러리를 설치해야 합니다.

    Attributes:
        project: 현재 프로젝트.
        shot: 액티브 샷.
        seq: 활성 시퀀스.
        asset: 활성 에셋.
        task: 활성 태스크.
        task_type: 생성하거나 검색할 태스크 유형.
        _person: 태스크를 할당할 사용자의 이름.

    """

    def __init__(self):
        """

        MyGazu 클래스의 새 인스턴스를 초기화합니다.

        """

        gazu.client.set_host("http://192.168.3.116/api")
        gazu.log_in("pipeline@rapa.org", "netflixacademy")
        self.project = None
        self.shot = None
        self.seq = None
        self.asset = None
        self.task = None
        self.task_type = None
        self._person = None

    def set_project(self, name):
        """

        현재 프로젝트를 지정된 이름의 프로젝트로 설정합니다.

        Args:
            name: 설정할 프로젝트의 이름

        """

        self.project = gazu.project.get_project_by_name(name)

    def set_shot(self, name):
        """

        현재 샷을 지정된 이름의 샷으로 설정합니다.

        Args:
            name: 설정할 샷의 이름입니다.

        """

        self.shot = gazu.shot.get_shot_by_name(self.seq, name)
        # pp.pprint(self.shot)

    def set_seq(self, name):
        """

        현재 시퀀스를 지정된 이름의 시퀀스로 설정합니다.

        Args:
            name: 설정할 시퀀스의 이름입니다.

        """

        self.seq = gazu.shot.get_sequence_by_name(self.project, name)
        # pp.pprint(self.seq)

    def set_asset(self, name):
        """

        현재 자산을 지정된 이름의 자산으로 설정합니다.

        Args:
            name: 설정할 자산의 이름입니다.

        """

        self.asset = gazu.asset.get_asset_by_name(self.project, name)

    def set_task_asset(self, name):
        """

        현재 작업을 현재 자산의 이름이 지정된 작업으로 설정합니다.

        Args:
            name: 설정할 작업 유형의 이름입니다.

        """

        self.task_type = gazu.task.get_task_type_by_name(name)
        tasks = gazu.task.all_tasks_for_asset(self.asset)
        a = []
        for task in tasks:
            if task['task_type_name'] == name:
                self.task = task
                a.append()

    def set_task_shot(self, name):
        """

        현재 작업을 현재 샷에 대해 지정된 이름을 가진 작업으로 설정합니다.

        Args:
            name: 설정할 작업 유형의 이름입니다.

        """

        self.task_type = gazu.task.get_task_type_by_name(name)
        tasks = gazu.task.all_tasks_for_shot(self.shot)
        for task in tasks:
            if task['task_type_name'] == name:
                self.task = task

    def set_preview(self, comment, img):
        """

        지정한 설명 및 이미지 파일을 사용하여 현재 작업에 새 미리 보기를 추가합니다.

        Args:
            comment: 미리보기에 추가할 설명입니다.
            img: 미리 보기로 추가할 이미지 파일의 경로입니다.

        """

        comment_dict = gazu.task.add_comment(self.task, {'id': self.task['task_status_id']}, comment)
        gazu.task.add_preview(self.task, comment_dict, preview_file_path=img)

    def new_task(self, name):
        """

        현재 자산에 대해 지정된 유형의 새 태스크를 생성합니다.

        Args:
            name: 만들 작업 유형의 이름입니다.

        """

        self.task_type = gazu.task.get_task_type_by_name(name)
        self.task = gazu.task.new_task(self.asset, self.task_type)
        pp.pprint(self.task)

    def assign_task(self):
        """

        현재 작업을 '_person' 속성에 지정된 사용자에게 할당합니다.

        """

        new_task = gazu.task.new_task(self.asset, self.task_type)
        person_name = gazu.person.get_person_by_full_name(self._person)
        gazu.task.assign_task(new_task, person_name)
        print(new_task)


    def update_file_tree(self):
        gazu.files.update_project_file_tree(self.project, {
            "working": {
                "mountpoint": "/mnt/project",
                "root": "pizza",
                "folder_path": {
                    "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>/working/v<Revision>",
                    "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>/working/v<Revision>",
                    "style": "lowercase"
                },
                "file_name": {
                    "shot": "<Project>_<Sequence>_<Shot>_<TaskType>_<Revision>",
                    "asset": "<Project>_<AssetType>_<Asset>_<TaskType>_<Revision>",
                    "style": "lowercase"
                }
            },
            "output": {
                "mountpoint": "/mnt/project",
                "root": "pizza",
                "folder_path": {
                    "shot": "<Project>/shots/<Sequence>/<Shot>/<TaskType>/output/<OutputType>/v<Revision>",
                    "asset": "<Project>/assets/<AssetType>/<Asset>/<TaskType>/output/<OutputType>/v<Revision>",
                    "style": "lowercase"
                },
                "file_name": {
                    "shot": "<Project>_<Sequence>_<Shot>_<OutputType>_v<Revision>",
                    "asset": "<Project>_<AssetType>_<Asset>_<OutputType>_v<Revision>",
                    "style": "lowercase"
                }
            }
        })

    def create_tree_dir(self):
        for shot in gazu.shot.all_shots_for_project(self.project):
            for task in gazu.task.all_tasks_for_shot(shot):
                path = os.path.dirname(
                    gazu.files.build_working_file_path(task)
                )
        os.makedirs(path)
        for asset in gazu.asset.all_assets_for_project(self.project):
            for task in gazu.task.all_tasks_for_asset(asset):
                path = os.path.dirname(
                    gazu.files.build_working_file_path(task)
                )
        os.makedirs(os.sep + path)

    def update_working(self):
        """

        Returns:

        """
        for shot in gazu.shot.all_shots_for_project(self.project):
            for task in gazu.task.all_tasks_for_shot(shot):
                working_file_path = os.path.dirname(
                    gazu.files.build_working_file_path(task)
                )
                if os.path.exists(working_file_path):
                    print("path exists Working_file_path :", working_file_path)
                    pass
                else:
                    print("Working_file_path :", working_file_path)
                    os.makedirs(working_file_path)

        for asset in gazu.asset.all_assets_for_project(self.project):
            for task in gazu.task.all_tasks_for_asset(asset):
                print("asset :", asset['name'])
                print("task :", task['task_type_name'])
                working_file_path = os.path.dirname(
                    gazu.files.build_working_file_path(task)
                )
                if os.path.exists(working_file_path):
                    print("path exists", working_file_path)
                    pass
                else:
                    print("Working_file_path :", working_file_path)
                    os.makedirs(working_file_path)

    def update_output(self, output_type):
        """

        Args:
            output_type:

        Returns:

        """

        output = gazu.files.get_output_type_by_name(output_type)
        for shot in gazu.shot.all_shots_for_project(self.project):
            for task in gazu.task.all_tasks_for_shot(shot):
                output_file_path = os.path.dirname(
                    gazu.files.build_entity_output_file_path(shot, output,
                                                             gazu.task.get_task_type_by_name(task['task_type_name']))
                )
                if os.path.exists(output_file_path):
                    print("path exists Output_file_path :", output_file_path)
                    pass
                else:
                    print("Output_file_path :", output_file_path)
                    os.makedirs(output_file_path)

        for asset in gazu.asset.all_assets_for_project(self.project):
            for task in gazu.task.all_tasks_for_asset(asset):
                output_file_path = os.path.dirname(
                    gazu.files.build_entity_output_file_path(asset, output_type,
                                                             gazu.task.get_task_type_by_name(task['task_type_name']))
                )
                if os.path.exists(output_file_path):
                    print("path exists", output_file_path)
                    pass
                else:
                    print("Output_file_path :", output_file_path)
                    os.makedirs(output_file_path)

        # update = gazu.files.update_output_file(output_file=, data)

    def working_publish_for_asset(self, asset, task_type):
        """

        Args:
            asset:
            task_type:

        Returns:

        """

        pick_asset = gazu.asset.get_asset_by_name(self.project, asset)
        tasks = gazu.task.all_tasks_for_asset(pick_asset)
        # print(task_type)
        for i in tasks:
            # print(i['task_type_name'])
            if task_type == i['task_type_name']:
                task = i
        new_working_file = gazu.files.new_working_file(task)
        working_file_path = os.path.dirname(new_working_file['path'])
        if os.path.exists(working_file_path):
            print("path exists :", working_file_path)
        else:
            print("create working file path :", working_file_path)
            os.makedirs(working_file_path)
        print(new_working_file['path'])

    def working_path_for_asset(self, asset, task_type):
        """

        Args:
            asset:
            task_type:

        Returns:

        """

        pick_asset = gazu.asset.get_asset_by_name(self.project, asset)
        tasks = gazu.task.all_tasks_for_asset(pick_asset)
        for i in tasks:
            if task_type == i['task_type_name']:
                task = i
        last_revision = gazu.files.get_last_working_file_revision(task)
        all_working_files = gazu.files.get_working_files_for_task(task)
        working_file_path = os.path.dirname(
            gazu.files.build_working_file_path(task, revision=last_revision['revision'] + 1)
        )
        for a in all_working_files:
            print 'revision : {} \npath : {}'.format(a['revision'], a['path'])
        print 'Saved working file path : {}'.format(working_file_path)

        all_working_files = gazu.files.get_working_files_for_task(task)
        working_file_path = os.path.dirname(
            gazu.files.build_working_file_path(task, revision=last_revision['revision']+1)
        )
        for a in all_working_files:
            print 'revision : {} \npath : {}'.format(a['revision'], a['path'])
        print 'Saved working file path : {}'.format(working_file_path)

    def get_working_publish_for_shot(self, sequence, shot, t_type):
        """

        Args:
            sequence:
            shot:
            t_type:

        Returns:

        """

        # sequence = gazu.shot.get_sequence_by_name(self.project, self.seq)
        pick_sequence = gazu.shot.get_sequence_by_name(self.project, sequence)
        pick_shot = gazu.shot.get_shot_by_name(pick_sequence, shot)
        tasks = gazu.task.all_tasks_for_shot(pick_shot)
        task = None
        for a in tasks:
            print(a['task_type_name'])
            if a['task_type_name'].lower() == t_type.lower():
                task = a
        new_working_file = gazu.files.new_working_file(task)
        # print(new_working_file)
        working_file_path = os.path.dirname(new_working_file['path'])
        if os.path.exists(working_file_path):
            print("path exists :", working_file_path)
        else:
            print("create working file path :", working_file_path)
            os.mkdir(working_file_path)
        print(new_working_file['path'])

    def get_output_publish_for_shot(self, sequence, shot, output_type, t_type):
        """

        Args:
            sequence:
            shot:
            output_type:
            t_type:

        Returns:

        """

        pick_sequence = gazu.shot.get_sequence_by_name(self.project, sequence)
        pick_shot = gazu.shot.get_shot_by_name(pick_sequence, shot)
        # output_type = gazu.files.new_output_type("OBJ", "obj")
        output = gazu.files.get_output_type_by_name("OBJ")
        task_types = gazu.task.all_task_types_for_shot(pick_shot)
        task_type = None
        for a in task_types:
            if a['name'].lower() == t_type.lower():
                task_type = a
        new_output_file = gazu.files.new_entity_output_file(pick_shot, output, task_type, "publish test")
        output_file_path = os.path.dirname(new_output_file['path'])
        if os.path.exists(output_file_path):
            print("path exists :", output_file_path)
        else:
            print("create output file path :", output_file_path)
            os.makedirs(output_file_path)
        print(new_output_file['path'])

        pick_shot = gazu.shot.get_shot_by_name(pick_sequence, shot)
        tasks = gazu.task.all_tasks_for_shot(pick_shot)
        task = None
        for a in tasks:
            if a['task_type_name'].lower() == t_type.lower():
                task = a
        last_revision = gazu.files.get_last_working_file_revision(task)
        all_working_files = gazu.files.get_working_files_for_task(task)
        working_file_path = os.path.dirname(
            gazu.files.build_working_file_path(task, revision=last_revision['revision']+1)
        )
        for a in all_working_files:
            print 'revision : %s \npath : %s' % (a["revision"], a["path"])
        print 'Saved working file path : %s' % working_file_path

    def get_working_path_for_shot(self, sequence, shot, t_type):
        """

        Args:
            sequence:
            shot:
            t_type:

        Returns:

        """

        pick_sequence = gazu.shot.get_sequence_by_name(self.project, sequence)
        pick_shot = gazu.shot.get_shot_by_name(pick_sequence, shot)
        tasks = gazu.task.all_tasks_for_shot(pick_shot)
        # pp.pprint(tasks)
        task2 = None
        for a in tasks:
            if a['task_type_name'].lower() == t_type.lower():
                task2 = a
        # print(task2)
        last_revision = gazu.files.get_last_working_file_revision(task2)
        return last_revision
        # all_working_files = gazu.files.get_working_files_for_task(task2)
        # working_file_path = os.path.dirname(
        #     gazu.files.build_working_file_path(task2, revision=last_revision['revision'] + 1)
        # )
        # for a in all_working_files:
        #     print(f'revision : {a["revision"]} \npath : {a["path"]}')
        # print(f'Saved working file path : {working_file_path}')

    def get_frame_padding(self):
        padding_info = self.shot.get('nb_frames')
        if not padding_info:
            padding_info = 4
        return '#' * padding_info

    def get_output_path_for_shot(self, sequence, shot, output_type, t_type):
        """

        Args:
            sequence:
            shot:
            output_type:
            t_type:

        Returns:

        """

        pick_sequence = gazu.shot.get_sequence_by_name(self.project, sequence)
        pick_shot = gazu.shot.get_shot_by_name(pick_sequence, shot)
        output = gazu.files.get_output_type_by_name(output_type)
        task_types = gazu.task.all_task_types_for_shot(pick_shot)
        task_type = None
        for a in task_types:
            if a['name'].lower() == t_type.lower():
                task_type = a

        output_ext = ""
        seq_ext = ["jpg", "png", "exr"]
        if output.get('name').lower() not in seq_ext:
            output_ext = ".%s" % output.get('name').lower()
        else:
            output_ext = ".%s.%s" % (self.get_frame_padding(), output.get('name').lower())
        last_revision = gazu.files.get_last_entity_output_revision(pick_shot, output, task_type, name='main')
        return gazu.files.build_entity_output_file_path(pick_shot, output, task_type, revision=last_revision) + output_ext

    def casting_create(self, asset, asset2):
        """

        Args:
            asset: asset name
            sequence: sequence name
            shot: shot name

        Returns:

        """
        pick_asset = gazu.asset.get_asset_by_name(self.project, asset)
        pick_asset2 = gazu.asset.get_asset_by_name(self.project, asset2)
        # pick_sequence = gazu.shot.get_sequence_by_name(self.project, sequence)
        # pick_shot = gazu.shot.get_shot_by_name(pick_sequence, shot)
        asset_castings = gazu.casting.get_asset_casting(pick_asset)
        # asset_castings = gazu.casting.get_shot_casting(pick_shot)
        new = {"asset_id": pick_asset2['id'], "nb_occurences": 3}
        asset_castings.append(new)
        gazu.casting.update_asset_casting(self.project, pick_asset, casting=asset_castings)




    def get_path_for_casting(self, asset):
        """

        Args:
            asset:

        Returns:

        """

        pick_asset = gazu.asset.get_asset_by_name(self.project_name, asset)
        cast_in = gazu.casting.get_asset_cast_in(pick_asset)
        for shot in cast_in:
            tasks = gazu.task.all_tasks_for_shot(shot['shot_id'])
            for task in tasks:
                all_working_files = gazu.files.get_working_files_for_task(task)
                for a in all_working_files:
                    basename = os.path.basename(a['path'])
                    print '%s : %s' % (basename, a['path'])







def main():
    project = 'Test_Euimin'
    shot = 'My_shot'
    seq = 'My_seq'
    asset = 'Rabbit'
    task_type = 'Layout'
    person = 'euimin Lee'

    gz = MyGazu()
    gz.set_project('Test_Euimin')
    gz.set_seq('My_seq')
    gz.set_shot('My_shot')
    gz.set_task_shot('Layout')
    gz.set_asset('Rabbit')
    # gz.new_task("Layout")
    # gz.new_task("Layout")
    # gz.assign_task()
    # dd = gazu.person.all_persons()
    # pp.pprint(dd)

    # gz.update_file_tree()
    # gz.create_tree_dir()
    # test.get_path_for_casting("rocket")
    # gz.new_task('modeling')
    # gz.new_task2('Layout')
    # print(gz.new_task2())
    # gz.set_task('modeling')
    # preview_file = '/home/rapa/다운로드/cow.jpg'
    # gz.set_preview('New preview file', preview_file)
    # gz.get_working_publish_for_shot('seq_01', 'shot_01', 'layout')
    # gz.get_working_path_for_shot('seq_01', 'shot_01', 'layout')
    # gz.get_output_publish_for_shot('seq_01', 'shot_01', 'OBJ', 'layout')
    # gz.get_output_path_for_shot('seq_01', 'shot_01', 'OBJ', 'layout')
    # gz.working_publish_for_asset('Cow', 'modeling')
    # gz.working_path_for_asset('Cow', 'modeling')
    # gz.casting_create('Cow', 'seq_01', 'shot_01')
    # gz.casting_create('Mouse', 'seq_01', 'shot_01')
    # gz.casting_create('Desk', 'seq_01', 'shot_01')
    # gz.casting_create('Desk', 'Mouse')

    # aaa = gazu.casting.get_shot_casting(gz.shot)
    # print(aaa)


    # matchmove가 camera와 undistort images를 output file로 publish
    # seq01 seq, shot01 shot에서 작업




    # working_files = gz.get_working_path_for_shot('seq_01', 'shot_01', 'Layout')
    # print(working_files)


    # last = gz.get_output_path_for_shot('seq_01', 'shot_01', 'jpg', 'Layout')
    # print(last)

if __name__ == "__main__":
    main()