#coding:utf8
import gazu
import maya.cmds as mc
from kitsumaya import SetThings as sett


class MayaThings:
    def __init__(self):
        self._task, self._shot = sett.select_task()

    def load_working(self):
        """
        마야에서 선택한 테스크에 working file이 이미 있을 경우,
        해당 파일을 import 하는 매서드
        """
        pass

    def load_output(self, path):
        """
        마야에서 샷에 캐스팅된 에셋의 output file들을 import하는 매서드

        Args:
            path(str): 파일명까지 포함된 에셋의 아웃풋 파일의 패스
        """
        mc.file(
            path, i=True, ignoreVersion=True,
            mergeNamespacesOnClash=False, importTimeRange="combine",
            loadReferenceDepth="all",
            returnNewNodes=True
        )

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
            file_dict_list = sett.get_kitsu_path(casting)
            for file_dict in file_dict_list:
                self.load_output(file_dict['path'])

    def get_undistortion_img(self):
        """
        _shot에 소속된 task type이 Matchmove고,
        ouput type이 Undistortion_img인 output file을 찾는 매서드

        Returns:
            str: 마지막 언디스토션 이미지가 저장된 path. ## padding을 여기서 추출해야 하려나 싶다.
        """
        undi_path = gazu.files.build_entity_output_file_path(self._shot, 'Undistortion_img', 'Matchmove')
        full_path = undi_path + '.jpg'

        return full_path

    def get_camera(self):
        """
        _shot에 소속된 task type이 Matchmove고,
        ouput type이 Camera인 output file을 찾는 매서드

        Returns:
            str: 카메라(fbx) 아웃풋 파일이 저장된 path
        """
        camera_files = gazu.files.get_last_output_files_for_entity(self._shot, 'Camera', 'Matchmove')
        camera_path = gazu.files.build_entity_output_file_path(self._shot, 'Camera', 'Matchmove')
        full_path = camera_path + '.' + camera_files[0]['representation']

        return full_path

    def connect_image(self, undi_path, camera):
        """
        import한 언디스토션 이미지(아웃풋 파일) 시퀀스와 camera를 연결시켜주는 매서드
        카메라가 바라보는 방향에 언디스토션 이미지가 뜨고,
        카메라의 움직임에 따라 감
        카메라에 이미지 연결 후 시퀀스 옵션을 True로 해서 이미지가 영상처럼 넘어가게 함

        Args:
            undi_path(str): 확장자까지 포함된 마지막 언디스토션 이미지의 파일경로
            camera(str): 카메라 파일의 경로
        """
        image_plane = mc.imagePlane(c=camera)
        mc.setAttr(image_plane[0] + '.imageName', undi_path, type='string')
        mc.setAttr(image_plane[0] + '.useFrameExtension', True)

    def import_cam_seq(self):
        """
        샷에 소속된 언디스토션 시퀀스를 찾고(get_undistort_img)
        샷에 소속된 카메라 output file도 찾아서(get_camera)
        모두 import한 뒤, 언디스토션 시퀀스를 카메라와 연결시키는(connect_image) 매서드
        """
        undi_seq_path = self.get_undistortion_img()
        camera_path = self.get_camera()
        self.connect_image(undi_seq_path, camera_path)

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

    def export_preview(self, path, comment):
        """
        output file의 용량을 줄여서 preview file을 저장하는 매서드

        Args:
            path(str): _preview와 확장자를 붙인 전체 경로
            comment(str): 프리뷰 파일에 대한 comment
        """
        # preview = gazu.task.create_preview(self._task, comment=comment)
        # gazu.task.upload_preview_file(preview, path)
        pass

    def export_output_file(self, path):
        """
        작업한 파일을 플레이블라스트 시퀀스로 저장하는 매서드

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

        # 카메라가 바라보는 플레이블라스트 저장 (패딩이 자동으로 붙는지 확인 필요)
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
