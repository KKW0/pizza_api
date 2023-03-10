#coding:utf8
import gazu


class KitsuThings:
    """
    Kitsu에 접근하여 필요한 정보들을 추출하는 매서드
    """
    def __init__(self):
        pass

    def _get_frame_padding(self, shot):
        """
        샷에 프레임 정보가 있을 경우 패딩을 생성해주는 매서드

        프레임 정보가 없으면 4자리로 생성한다.

        Args:
            shot(dict): 선택한 테스크가 속한 에셋에 캐스팅된 샷
        """
        padding_info = shot.get('nb_frames') - 1
        if padding_info is False:
            padding_info = 3
        padding = '_' + ('0' * padding_info) + '1'

        return padding

    def get_undistortion_img(self, shot):
        """
        shot에 소속된 task type이 Matchmove고,
        ouput type이 Undistortion_img인 output file을 찾는 매서드

        샷에 대한 패딩을 얻어(get_frame_padding) 첫번째 언디스토션 시퀀스 이미지의 경로를 추출한다.

        Args:
            shot(dict): 선택한 테스크가 속한 에셋에 캐스팅된 샷
        Returns:
            str: 첫번째 언디스토션 이미지의 path
        """
        padding = self._get_frame_padding(shot)
        undi_path = gazu.files.build_entity_output_file_path(shot, 'Undistortion_img', 'Matchmove')
        full_path = undi_path + padding + '.jpg'

        return full_path

    def get_camera(self, shot):
        """
        shot에 소속된 task type이 Matchmove고,
        ouput type이 Camera인 output file을 찾는 매서드

        output file의 저장된 정보로부터 확장자를 추출하고,
        path와 이어붙여 샷에 해당하는 가상 카메라의 전체 경로를 구한다.

        Args:
            shot(dict): 선택한 테스크가 속한 에셋에 캐스팅된 샷
        Returns:
            str: 카메라(fbx 등) 아웃풋 파일이 저장된 path
        """
        camera_files = gazu.files.get_last_output_files_for_entity(shot, 'Camera', 'Matchmove')
        camera_path = gazu.files.build_entity_output_file_path(shot, 'Camera', 'Matchmove')
        full_path = camera_path + '.' + camera_files[0]['representation']

        return full_path

    def get_kitsu_path(self, casting):
        """
        레이아웃 에셋에 캐스팅된 에셋들의 최신 output file들의 패스 리스트를 추출하는 매서드

        캐스팅된 에셋 하나에 아웃풋 파일이 여러개일 경우를 가정한다.

        file_list: 아래의 딕셔너리를 모은 리스트
        file_dict: 캐스팅된 에셋에서 필요한 정보들(path, nb_elements)만 정제한 딕셔너리

        Args:
            casting(dict): task에 캐스팅된 에셋의 간략한 정보가 담긴 dict

        Returns:
            list: 아웃풋 파일들의 패스(확장자 포함), 개수가 담긴 dict를 수집한 리스트
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
