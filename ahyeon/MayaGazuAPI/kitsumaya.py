#coding:utf8
import gazu
from filter import Filter
from login import LogIn
from usemaya import MayaThings
from publish import PublishThings

 
class SetThings:
    def __init__(self):
        LogIn()
        self.filter = Filter()
        self.maya = MayaThings()
        self.pub = PublishThings()

    def run_program(self, comment, proj_num=0, seq_num=0, task_num=0):
        """
        프로그램을 구동하는 매서드

        Args:
            comment(str): working/output/preview file에 대한 커밋 내용
            proj_num(int): 선택할 프로젝트의 인덱스 번호
            seq_num(int): 선택할 시퀀스의 인덱스 번호
            task_num(int): 선택할 테스크의 인덱스 번호
        """
        task = self.filter.select_task(proj_num=proj_num, seq_num=seq_num, task_num=task_num)
        # 테스크 선택하고 테스크 에셋에 캐스팅된 샷으로부터 테스크 에셋이 사용되는 시퀀스, 프로젝트 정보 추출
        # 필터 적용할수도 있음

        if type(task) is list:
            # 테스크를 선택하기 전에는 메인 프리뷰를 띄우는 것 외에 아무 일도 하지 않는다.
            return
        else:
            seq = gazu.casting.get_asset_cast_in(task['entity_id'])
            shot_list = gazu.shot.all_shots_for_sequence(seq)
            for shot in shot_list:
                self.maya.import_casting_asset(shot)
                # 각 샷에 캐스팅된 에셋을 마야에 모두 import
                self.maya.import_cam_seq(shot)
                # 각 샷의 카메라와 언디스토션 이미지를 마야에 모두 import하고 둘을 연결

            self.pub.publish_file_data(task, comment=comment)
            # Kitsu에 저장한 working, output file 데이터 퍼블리싱
            self.pub.save_publish_real_data(task, comment=comment)
            self.pub.save_publish_previews(shot_list)
            # 폴더 트리에 working, output, preview 파일 저장하고 Kitsu에 업로드


pr = SetThings()
pr.run_program('my first test commit', 1, 1, 1)
