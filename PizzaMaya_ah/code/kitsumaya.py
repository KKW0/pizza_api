#coding:utf8
import gazu
from filter import Filter
from login import LogIn
from usemaya import MayaThings
from publish import PublishThings

 
class SetThings:
    """
    서버에 로그인하고, 프로그램을 동작하는 클래스
    """
    def __init__(self):
        """
        서버에 로그인하고 모듈의 인스턴스를 생성하는 매서드
        """
        lo = LogIn()
        lo.connect_host()
        lo.log_in()
        self.filter = Filter()
        self.maya = MayaThings()
        self.pub = PublishThings()

    def run_program(self, comment, proj_num=0, seq_num=0, task_num=None, shot_num=None,
                    asset_index_list=None, do="Load"):
        """
        프로그램을 구동하는 매서드

        필요 시 필터를 적용하여 사용자가 수행할 테스크를 선택하고,
        해당 테스크가 사용되는 샷을 모두 추출한다.
        추출한 각 샷에 캐스팅된 에셋/카메라/언디스토션 이미지를 마야 씬에 import 하거나,
        작업한 결과물을 저장 및 퍼블리시 할 수 있다.

        Args:
            comment(str): working/output/preview file에 대한 커밋 내용
            proj_num(int): 선택할 프로젝트의 인덱스 번호. 0은 All을 의미한다.
            seq_num(int): 선택할 시퀀스의 인덱스 번호. 0은 All을 의미한다.
            task_num(int): 선택할 테스크의 인덱스 번호. task 선택 전에는 None
            shot_num(int): 작업할 샷의 인덱스 번호. shot 선택 전에는 None
            asset_index_list(list): 사용자가 import 하길 선택한 에셋의 인덱스 리스트. None은 [0]이며, All을 의미한다.
            do(str): 사용자가 동작시킬 기능. Save 또는 Load
        """
        task = self.filter.select_task(proj_num=proj_num, seq_num=seq_num, task_num=task_num)
        # 테스크 선택하고 테스크 에셋에 캐스팅된 샷으로부터 테스크 에셋이 사용되는 시퀀스, 프로젝트 정보 추출


        if type(task) is list:
            # 테스크를 선택하기 전에는 아무 일도 하지 않는다.
            return
        else:
            # 레이아웃 테스크가 주어진 에셋과 그 에셋이 캐스팅된 시퀀스를 구하고, 시퀀스의 샷 리스트를 추출한다.
            casted_list = gazu.casting.get_asset_cast_in(task['entity_id'])
            for cast in casted_list:
                if 'SEQ' in cast['name']:
                    seq = cast
                else:
                    continue
            shot_list = gazu.shot.all_shots_for_sequence(seq)

        if asset_index_list is None:
            asset_index_list = [0]
        if do is 'Load':
            if shot_num is not None:
                # 샷을 선택하고 그 안에서 에셋을 선택하거나, 샷 선택 없이 에셋만 선택할 수 있다.
                shot = self.filter.select_shot(shot_list, shot_num)
                self.maya.import_casting_asset(shot, asset_index_list)
                # 선택한 샷에 캐스팅된 에셋 중 index를 선택한 것을 마야에 모두 import
                self.maya.import_cam_seq(shot)
                # 선택한 샷의 카메라와 언디스토션 이미지를 마야에 import하고 둘을 연결
            else:
                for shot in shot_list:
                    self.maya.import_casting_asset(shot, asset_index_list)
                    # 시퀀스에 속한 각 샷에 캐스팅된 에셋을 마야에 모두 import
                    self.maya.import_cam_seq(shot)
                    # 각 샷의 카메라와 언디스토션 이미지를 마야에 import하고 둘을 연결
        elif do is 'Save':
            self.pub.save_publish_real_data(task, comment)
            self.pub.save_publish_previews(shot_list, comment)
            # Kitsu에 퍼블리싱하기 위해 모델 생성 후
            # 폴더 트리에 working, output, preview 파일 저장하고 Kitsu에 업로드
        else:
            raise ValueError("지원하지 않는 기능입니다.")


pr = SetThings()
pr.run_program('my first test commit', 1, 1, 1)
