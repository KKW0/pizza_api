"""

**API 소개**
위 api는 Gazu를 활용하여 Asset 및 shot의 정보를 가져와 사용하는 것을 목표로 합니다.
샷의 카메라와 캐스팅 정보를 수집하고, 다음 정보를 활용하여 작업 파일과 출력 파일을 퍼블리싱하는 역할을 합니다.



**class : SetThings**

위 클래스는 샷에 있는 레이아웃 테스크에 캐스팅된 에셋경로를 추출하고 폴더 트리에 있는 working, output, preview 파일을 저장하며 Kitsu에 업로드하는 class이다.

    **def __init__:**
        프로덕션 데이터베이스에 대한 연결을 설정하고, 사용자 로그인 후 PublishThings사용자 정의 클래스인 의 인스턴스를 생성한다.

        .. doctest::
            self._project = None
            self._shot = None
            self._task = None

        Output >>
            self._project = project_dict
            self._shot = shot_dict
            self._task = task_dict

    **def project(self, value):**
        테스크가 있는 프로젝트를 선택하는 세터

        .. doctest::
            self._project = gazu.project.get_project_by_name(value)

        Output >>
            project_dict

    **def update_filetree(mountpoint, root):**
        지정된 mountpoint 및 root로 프로젝트의 파일 트리를 업데이트한다.

        .. doctest::
            gazu.files.update_project_file_tree(self.project, tree)

        Output >>
            shot_path = "/home/pizza/kitsu/<Project>/shots/<Sequence>/<Shot>/<TaskType>...

    **def select_task(self, num=0):**
        user에 assign되어 있으며 상태가 Todo인 task를 선택하고
        선택한 task에 기반하여 shot을 추출해 저장한다.

        .. doctest::
            self._task = task_list[num]
            self._shot = gazu.entity.get_entity(self._task['entity_id'])

        Output >>
            self._task = task_dict
            self._shot = shot_dict

    **def _get_kitsu_path(self, casting):**
        샷에 캐스팅된 에셋의 최신 output file들의 패스 리스트를 추출하는 매서드

        .. doctest::
            mm = SetThings()
            mm._get_kitsu_path(asset_dict)

        Output >>
            /home/pizza/<Project>/shots/<Sequence>/<Shot>/<TaskType>/output/<OutputType>/v<Revision>/pizza.fbx

    **def run_program(comment):**
        select_task()메소드를 실행시키고  폴더 트리에 working, output, preview 파일 저장하고 Kitsu에 업로드한다.

        .. doctest::
            mm = SetThings()
            mm.run_program("This is like commit")

        Output >>
            Kitsu에 데이터 퍼블리싱
            폴더 트리에 working, output, preview 파일 저장하고 Kitsu에 업로드



**class : PublishThings**

위 클래스는 working file과 output file을 저장하고 가져오기 위한 실제 폴더를 생성하며, Kitsu에 파일정보를 기록한 뒤 업로드하는 class 이다.

    **def __init__:**
        software 및 output type은 class에 대한 생성자 메서드를 정의하며, 이를 초기화 합니다.

        .. doctest::
            self._software = None
            self._output_type = None

            Output >>
            self._software는 software의 이름값을 가진다.
            self._output_type은 output_type의 이름값을 가진다.

    **def _select_software(self, num=0):**
        working file을 생성하기 위해 소프트웨어를 저장합니다.
        software_list를 출력하여 원하는 값을 반환한다.

        .. doctest::
            software_list = gazu.files.all_softwares()

            Output >>
            software_list[num] = {"name" : "None",
                                    "key": "value" }

    **def _select_output_type(self, shot, num=0):**
        output 파일을 생성하기 위하여 output types의 entity의 정보를 사용하여 초기 output type을 설정한다.
        output_type_list를 출력하여 원하는 값을 반환한다.

        .. doctest::
            output_type_list = gazu.files.all_output_types_for_entity(shot['id'])

            Output >>
            output_type_list[num] = {"name" : "main",
                                    "output_type": "value" }

    **def publish_file_data(self, shot, task, comment):**
        작업 파일과 출력 파일을 만들고 각 파일의 경로를 구축한다.
        shot, task, comment의 세 가지 인수를 사용하고, output_file, output_path, working_file, working_path 네 가지 값을 반환한다.

        주어진 task 및 shot 을 기반으로 작업 파일과 출력 파일을 만들어 먼저 task에 대한 기존 작업 파일이 있는지 확인하고, 없으면 새 작업 파일을 생성한다.
        그런 다음 지정된 샷 및 작업에 대한 기존 출력 파일이 있는지 확인하고, 없으면 새 출력 파일을 생성한다.

        .. doctest::
            publish = PublishThings()
            shot = gazu.shot.create_shot("Test Shot")
            task = gazu.task.create_task("Test Task")

           Output >>
            working_file = {"working_file_id": "1234"}
            working_path는 다음과 같이 출력됩니다 : "/path/to/working/file.v001.ma"
            output_file = {"output_file_id": "5678"}
            output_path는 다음과 같이 출력됩니다 : "/path/to/output/file.v001.exr"

    **def _make_folder_tree(self, path):**
        working file, output file을 저장 및 내보내기 위한 실제 폴더를 생성한다.

        .. doctest::
            parent = os.path.dirname(path)
            if parent != "/":
                self._make_folder_tree(parent)

            Output >>
            /mnt/project/pizza/<project_name>/<asset>/<asset_Type>/<Task>/<Task_Type>/<output>
            파일트리 구조에 맞게 폴더가 생성됩니다.

    **def _upload_files(self, task, path, comment, file_type):**
        작업한 working file과 task에 대한 prewiew file을 Kitsu에 업로드한다.
        working file의 경로와 software를 전체 경로로 지정하고,
        output file의 경로와 확장자명을 전체 경로로 지정한다.
        지정된 output file의 경로를 통해 preview file을 업로드한다.

        .. doctest::
            full_path = path + '.' + self._software['file_extension']
            gazu.files.upload_working_file(file_type, full_path)

            full_path = path + '_preview.mov'
            preview = gazu.task.create_preview(task, comment=comment)
            gazu.task.upload_preview_file(preview, full_path)

            Output >>
                작업한 working파일과 Task에 대한 preview file을 Kitsu에 업로드

    **def save_publish_real_data(self, shot, task, comment):**
        경로에 맞추어 폴더 트리를 생성하고, 파일을 저장하는 메소드 이후 working file과 preview file을 Kitsu에 업로드한다.
        working file, path 및 output file, path의 정보를 불러온 이후,
        각 build된 경로에 파일명을 잘라내는 경로를 지정하고 이에 대한 폴더를 생성
        생성된 폴더에 따른 working file, output file 업로드

        .. doctest::
            path_working = os.path.dirname(working_path)
            path_output = os.path.dirname(output_path)
            self._make_folder_tree(path_working)
            self._make_folder_tree(path_output)

            Output >>
                폴더 트리를 생성하고 working, output, preview 다음 파일을 저장 후 Kitsu에 업로드

"""