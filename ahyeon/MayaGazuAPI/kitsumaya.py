#coding:utf8
import gazu
import pprint as pp
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
        self._project = None
        self._shot = None
        self._task = None

    def _get_kitsu_path(self, casting):
        """
        샷에 캐스팅된 에셋의 최신 output file들의 패스 리스트를 추출하는 매서드

        Args:
            casting(dict): 샷에 캐스팅된 에셋의 간략한 정보가 담긴 dict

        Returns:
            list: 아웃풋 파일들의 패스(확장자 포함), 개수, 확장자가 담긴 dict를 수집한 리스트
        """
        file_list = []
        file_dict = {
            'path': "",
            'nb_elements': 0,
        }
        asset = gazu.asset.get_asset(casting['id'])
        output_file_list = gazu.files.get_last_output_files_for_entity(asset)
        for out_file in output_file_list:
            # 각 output file의 패스를 생성하고, 리스트에 append
            out_path = gazu.files.build_entity_output_file_path(asset,
                                                                out_file['output_type_id'],
                                                                out_file['task_type_id'],
                                                                revision=out_file['revision'])
            path = out_path + '.' + out_file['representation']
            file_dict['path'] = path
            file_dict['nb_elements'] = out_file['nb_elements']
            file_list.append(file_dict)

        return file_list

    def import_casting_asset(self):
        """
        수행중인 테스크(샷)에 캐스팅된 에셋의 저장위치를 모두 추출하여 마야에 import 하는 매서드
        output file의 각각의 확장자 포함된 패스를 추출하고(get_kitsu_path),
        추출한 패스를 기반으로 마야에 import 한다.(load_output)

        file_dict_list: 에셋에 있는 각 output file들(최신버전)의
                        path, nb_elements가 기록된 dict를 모은 리스트
        casting_list: 캐스팅된 에셋의 asset_id와 nb_elements가 기록된 dict가 모인 리스트
        """
        file_dict_list = []
        casting_list = gazu.casting.get_shot_casting(self._shot)
        for casting in casting_list:
            file_dict_list = self._get_kitsu_path(casting)
            for file_dict in file_dict_list:
                self.maya.load_output(file_dict['path'])

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
            self.import_casting_asset()
            # 샷에 캐스팅된 에셋을 마야에 모두 import
            self.maya.import_cam_seq(self._shot)
            # 샷의 카메라와 언디스토션 이미지를 마야에 import하고 둘을 연결

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

