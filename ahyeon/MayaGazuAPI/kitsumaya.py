#coding:utf8
import gazu
from filter import Filter
from login import LogIn
from usemaya import MayaThings
from publish import PublishThings


class SetThings(object):
    def __init__(self):
        LogIn()
        self.filter = Filter()
        self.maya = MayaThings()
        self.pub = PublishThings()

    def run_program(self, comment):
        """
        프로그램을 구동하는 매서드

        Args:
            comment(str): working/output/preview file에 대한 커밋 내용
        """
        task = self.filter.select_task()
        # 테스크 선택하고 테스크가 속한 샷, 시퀀스, 프로젝트 정보 추출
        # 필터 적용할수도 있음

        seq = task['sequence_id']
        shot_list = gazu.shot.all_shots_for_sequence(seq)
        for shot in shot_list:
            self.maya.import_casting_asset(shot)
            # 각 샷에 캐스팅된 에셋을 마야에 모두 import
            self.maya.import_cam_seq(shot)
            # 각 샷의 카메라와 언디스토션 이미지를 마야에 모두 import하고 둘을 연결

        self.pub.publish_file_data(task, comment=comment)
        # Kitsu에 저장한 working, output file 데이터 퍼블리싱
        self.pub.save_publish_real_data(task, comment=comment)
        # 폴더 트리에 working, output, preview 파일 저장하고 Kitsu에 업로드


# def main():
#     mm = SetThings()
#     mm.project = "jeongtae"
#     mm.run_program("This is like commit")
#
#
# main()

