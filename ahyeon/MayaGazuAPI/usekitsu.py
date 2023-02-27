#coding:utf8
import gazu


class KitsuThings:
    def __init__(self):
        pass

    def _get_frame_padding(self, shot):
        """
        샷에 프레임 정보가 있을 경우 패딩을 생성해주는 매서드
        프레임 정보가 없으면 4자리로 생성한다.

        Args:
            shot(dict): 선택한 테스크가 속한 시퀀스의 샷
        """
        padding_info = shot.get('nb_frames') - 1
        if not padding_info:
            padding_info = 3
        padding = '_' + ('0' * padding_info) + '1'

        return padding

    def get_undistortion_img(self, shot):
        """
        shot에 소속된 task type이 Matchmove고,
        ouput type이 Undistortion_img인 output file을 찾는 매서드

        Args:
            shot(dict): 선택한 테스크가 속한 시퀀스의 샷
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

        Args:
            shot(dict): 선택한 테스크가 속한 시퀀스의 샷
        Returns:
            str: 카메라(fbx 등) 아웃풋 파일이 저장된 path
        """
        camera_files = gazu.files.get_last_output_files_for_entity(shot, 'Camera', 'Matchmove')
        camera_path = gazu.files.build_entity_output_file_path(shot, 'Camera', 'Matchmove')
        full_path = camera_path + '.' + camera_files[0]['representation']

        return full_path

    def get_kitsu_path(self, casting):
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
