#coding:utf8
import os
import gazu
import maya.cmds as mc


class MayaThings:
    def __init__(self):
        pass

    def load_working(self, task):
        """
        마야에서 선택한 테스크에 working file이 이미 있을 경우,
        해당 파일을 import 하는 매서드

        Args:
            task(dict): 사용자가 선택한 task의 딕셔너리
        """
        working = gazu.files.get_last_working_file_revision(task)

        if working is None:
            raise ValueError("working file이 존재하지 않습니다")
        else:
            path = gazu.files.build_working_file_path(task, software=working['software_id'],
                                                      revision=working['revision'])
            path = path + '.' + working['representation']
            mc.file(path, i=True)

    def load_output(self, path):
        """
        마야에서 샷에 캐스팅된 에셋의 output file들을 import하는 매서드
        입력된 패스가 언디스토션 이미지의 폴더라면 시퀀스 길이를 패딩에 맞게 재설정한다.

        Args:
            path(str): 파일명까지 포함된 아웃풋 파일의 패스
        """
        if 'Undistortion_img' in path:
            file_list = os.listdir(path)
            file_num = len(file_list)
            mc.playbackOptions(min=False, max=file_num)

        mc.file(
            path, i=True, ignoreVersion=True,
            # 아웃풋 파일의 패스를 import 하는데, 이 때 fbx파일의 버전 번호를 무시한다.
            mergeNamespacesOnClash=False, importTimeRange="combine",
            ### 파라미터 설명 필요함
            loadReferenceDepth="all",
            returnNewNodes=True
        )

    def _get_frame_padding(self, shot):
        """
        샷에 프레임 정보가 있을 경우 패딩을 생성해주는 매서드
        프레임 정보가 없으면 4자리로 생성한다.

        Args:
            shot(dict): 선택한 테스크가 속한 샷
        """
        padding_info = shot.get('nb_frames')
        if not padding_info:
            padding_info = 4
        padding = '_' + ('0' * padding_info)

        return padding

    def _get_undistortion_img(self, shot):
        """
        _shot에 소속된 task type이 Matchmove고,
        ouput type이 Undistortion_img인 output file을 찾는 매서드

        Args:
            shot(dict): 선택한 테스크가 속한 샷
        Returns:
            str: 마지막 언디스토션 이미지가 저장된 path.
        """
        padding = self._get_frame_padding(shot)
        undi_path = gazu.files.build_entity_output_file_path(shot, 'Undistortion_img', 'Matchmove')
        self._get_frame_padding(shot)
        path = undi_path + padding
        full_path = path + '.jpg'

        return full_path

    def _get_camera(self, shot):
        """
        _shot에 소속된 task type이 Matchmove고,
        ouput type이 Camera인 output file을 찾는 매서드

        Args:
            shot(dict): 선택한 테스크가 속한 샷
        Returns:
            str: 카메라(fbx 등) 아웃풋 파일이 저장된 path
        """
        camera_files = gazu.files.get_last_output_files_for_entity(shot, 'Camera', 'Matchmove')
        camera_path = gazu.files.build_entity_output_file_path(shot, 'Camera', 'Matchmove')
        full_path = camera_path + '.' + camera_files[0]['representation']

        return full_path

    def _connect_image(self, undi_path, camera_path):
        """
        import한 언디스토션 이미지(아웃풋 파일) 시퀀스와 camera를 연결시켜주는 매서드
        카메라가 바라보는 방향에 언디스토션 이미지가 뜨고,
        카메라의 움직임에 따라 감
        카메라에 이미지 연결 후 시퀀스 옵션을 True로 해서 이미지가 영상처럼 넘어가게 함

        Args:
            undi_path(str): 확장자까지 포함된 마지막 언디스토션 이미지의 파일경로
            camera_path(str): 카메라 파일의 경로
        """
        image_plane = mc.imagePlane(c=camera_path)
        mc.setAttr(image_plane[0] + '.imageName', undi_path, type='string')
        mc.setAttr(image_plane[0] + '.useFrameExtension', True)

    def import_cam_seq(self, shot):
        """
        샷에 소속된 언디스토션 시퀀스를 찾고(get_undistort_img)
        샷에 소속된 카메라 output file도 찾아서(get_camera)
        모두 import한 뒤(_load_output), 언디스토션 시퀀스를 카메라와 연결시키는(connect_image) 매서드

        Args:
            shot(dict): 선택한 테스크가 있는 시퀀스에 속한 샷
        """
        undi_seq_path = self._get_undistortion_img(shot)
        camera_path = self._get_camera(shot)
        self.load_output(undi_seq_path)
        self.load_output(camera_path)
        ### connect_image에서 import도 해주면 로드할 필요 없을 듯
        self._connect_image(undi_seq_path, camera_path)

    def save_working_file(self, path, representation):
        """
        마야 내에서 저장 경로와 저장 형식을 선택해 작업한 씬 파일을 저장하는 매서드

        Args:
            path(str): 저장할 경로 + 이름
            representation(str): "ma"또는 "mb"
        """
        if representation == "ma":
            mc.file(rename=path + ".ma")
        elif representation == "mb":
            mc.file(rename=path + ".mb")
        mc.file(save=True, type=representation)

    def export_output_file(self, path):
        """
        작업한 파일을 플레이블라스트 시퀀스로 저장하는 매서드
        저용량 preview 파일도 저장한다.

        Args:
            path(str): output file 시퀀스를 저장할 경로 + 이름
        """
        # 디폴트 카메라 필터링
        startup_cameras = []
        all_cameras = mc.ls(type='camera', l=True)
        for camera in all_cameras:
            if mc.camera(mc.listRelatives(camera, parent=True)[0], startupCamera=True, q=True):
                startup_cameras.append(camera)
        custom_camera = list(set(all_cameras) - set(startup_cameras))

        path = path + '_0000'

        # 카메라가 바라보는 플레이블라스트 저장
        ### 저용량으로 mov 하나 더 저장하는 기능 필요
        mc.lookThru(custom_camera[0])
        mc.playblast(
            format='image',
            filename=path,
            sequenceTime=False,
            clearCache=True, viewer=True,
            showOrnaments=True,
            fp=4, percent=50,
            compression="jpg",
            quality=100
        )
        