"""
**SetThings**

:class:
샷에 있는 레이아웃 테스크에 캐스팅된 에셋경로를 추출하고 폴더 트리에 있는 working, output, preview 파일을 저장하고 Kitsu에 업로드하는 class이다.

    **def __init__:**
        프로덕션 데이터베이스에 대한 연결을 설정하고, 사용자 로그인 후 PublishThings사용자 정의 클래스인 의 인스턴스를 생성합니다.

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
        지정된 mountpoint 및 root로 프로젝트의 파일 트리를 업데이트합니다.

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

"""