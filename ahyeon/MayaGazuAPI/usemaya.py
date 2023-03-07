#coding:utf8
import os
import gazu
import maya.cmds as mc
from usekitsu import KitsuThings


class MayaThings:
    """
    마야에서 working, output, preview 파일을 import, export하는 클래스
    """
    def __init__(self):
        """
        모듈의 인스턴스를 생성한다.
        """
        self.kit = KitsuThings()

    def load_working(self, task, num=0):
        """
        마야에서 선택한 테스크에 working file이 있을 경우, 해당 파일을 import 하는 매서드

        Args:
            task(dict): 사용자가 선택한 task의 딕셔너리
            num(int): 사용자가 선택한 working file의 revision
        """
        working = gazu.files.get_last_working_file_revision(task)

        if working is None:
            raise ValueError("working file이 존재하지 않습니다")
        elif num != 0:
            path = gazu.files.build_working_file_path(task, revision=num)
        else:
            path = gazu.files.build_working_file_path(task, revision=working['revision'])
        path = path + '.' + working['representation']
        mc.file(path, i=True)

    def _load_output(self, path, asset=None):
        """
        마야에서 task asset에 캐스팅된 에셋들의 output file들을 import하는 매서드

        입력된 패스가 언디스토션 이미지라면 시퀀스 길이를 패딩에 맞게 재설정하되, 최대값에 맞춘다.
        입력된 패스가 에셋(fbx, obj 등)이라면 nb_elements의 값에 맞게 인스턴스를 생성한다.

        Args:
            path(str): 확장자를 포함한 아웃풋 파일의 패스
            asset(dict): 로드하고자 하는 에셋의 nb_elements, path 정보가 담긴 딕셔너리
        """
        # 시퀀스 길이(씬의 프레임레인지) 를 가장 길게 설정
        if 'Undistortion_img' in path:
            file_list = os.listdir(path)
            frame_range = len(file_list)
            end_frame = mc.playbackOptions(query=True, max=True)
            if end_frame < frame_range:
                mc.playbackOptions(min=False, max=frame_range)

        mc.file(
            path, i=True, ignoreVersion=True,
            # path의 아웃풋 파일을 import 하는데, 이 때 fbx파일의 버전 번호를 무시한다.
            mergeNamespacesOnClash=False, importTimeRange="combine",
            # 네임스페이스 충돌이 발생하면 병합하지 않도록 지정
            # fbx 애니메이션 데이터를 씬의 기존 애니메이션과 결합하도록 지정
            loadReferenceDepth="all",
            returnNewNodes=True
        )

        if asset is not None:
            # 에셋이라면 nb_elements에 맞게 인스턴싱 진행
            for index in range(asset['nb_elements']-1):
                full_filename = os.path.basename(asset['path'])
                filename = full_filename.split('.')[0]
                mc.instance(filename)
                # 파일명과 마야에 import한 에셋의 이름이 같다는 전제 하에

    def _connect_image(self, undi_path, camera_path):
        """
        import한 언디스토션 이미지(아웃풋 파일) 시퀀스와 camera를 연결시켜주는 매서드

        카메라가 바라보는 방향에 언디스토션 이미지가 뜨고, 카메라와 이미지 플레인을 연결하여
        이미지가 카메라의 움직임에 따라 움직이며, 시퀀스 옵션을 True로 하여 이미지가 영상처럼 넘어가게 한다.
        그리고 노드로 둘을 연결해 visibility를 한번에 컨트롤할 수 있게 한다.

        Args:
            undi_path(str): 확장자까지 포함된 첫번째 언디스토션 이미지의 파일경로
            camera_path(str): 카메라 파일의 전체 경로
        """
        camera_name = (os.path.basename(camera_path)).split('.')
        image_plane = mc.imagePlane(camera=camera_name[0])
        mc.setAttr(image_plane[0]+'.imageName', undi_path, type='string')
        mc.setAttr(image_plane[0]+'.useFrameExtension', True)
        mc.connectAttr('%s.visibility' % camera_name, '%s.visibility' % image_plane)

    def import_cam_seq(self, shot):
        """
        샷에 소속된 언디스토션 시퀀스를 찾고(kit.get_undistort_img)
        샷에 소속된 카메라 output file도 찾아서(kit.get_camera)
        모두 import한 뒤(load_output), 언디스토션 시퀀스를 카메라와 연결시키는(connect_image) 매서드

        Args:
            shot(dict): 선택한 테스크가 속한 에셋에 캐스팅된 샷
        """
        undi_seq_path = self.kit.get_undistortion_img(shot)
        camera_path = self.kit.get_camera(shot)
        self._load_output(undi_seq_path)
        self._load_output(camera_path)
        self._connect_image(undi_seq_path, camera_path)

    def import_casting_asset(self, shot, num=None):
        """
        샷에 캐스팅된 에셋의 저장위치를 추출하여 마야에 import 하는 매서드

        shot에 캐스팅된 에셋의 중 import 할 파일을 고른 뒤,
        각각의 확장자 포함된 패스를 추출하고(kit.get_kitsu_path),
        추출한 패스를 기반으로 마야에 import 한다.(load_output)

        file_dict_list: 에셋에 있는 각 output file들(최신버전)의
                        path, nb_elements가 기록된 dict를 모은 리스트
        casting_list: 캐스팅된 에셋의 asset_id와 nb_elements가 기록된 dict가 모인 리스트

        Args:
            shot(dict): 선택한 테스크가 속한 에셋이 캐스팅된 샷
            num(list): import 하기를 선택한 에셋의 인덱스 번호의 집합
        """
        file_dict_list = []
        casting_list = gazu.casting.get_shot_casting(shot)
        layout_id = gazu.files.get_output_type_by_name('Layout_mb')['id']
        for casting in casting_list:
            if casting['output_type_id'] is not layout_id:
                # shot에 레이아웃팀이 작업하는 에셋도 캐스팅되어있기 때문에, 해당 파일을 제외한다.
                file_dict_list = self.kit.get_kitsu_path(casting)
        if num is [0]:
            num = range(len(casting_list))
        for index in num:
            file_dict = file_dict_list[index]
            self._load_output(file_dict['path'], file_dict)

    def save_scene_file(self, path, representation):
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

    def _make_main_preview_mov(self, path):
        """
        레이아웃의 main preview용 파일을 만드는 매서드

        카메라 그룹을 생성하고, 동일한 파일명이 있는지 확인한다.
        그리고 다른 카메라와 언디스토션 이미지를 모두 보이지 않게 설정한 뒤,
        플레이블라스트를 지정된 path에 저장하고

        Args:
            path: mov파일을 저장할 확장자를 제외한 이름까지의 경로
        """
        cam = mc.camera(
            centerOfInterest=5, focalLength=35,
            lensSqueezeRatio=1, cameraScale=1,
            horizontalFilmAperture=1.41732,
            horizontalFilmOffset=0,
            verticalFilmAperture=0.94488,
            verticalFilmOffset=0, filmFit='Fill',
            overscan=1, motionBlur=0, shutterAngle=144,
            nearClipPlane=0.1, farClipPlane=100000,
            orthographic=0, orthographicWidth=30,
            panZoomEnabled=0, horizontalPan=0,
            verticalPan=0, zoom=1
        )
        # 시퀀스 프리뷰 카메라 생성
        mc.setAttr("%s.rotateX" % cam[0], -35)
        mc.lookThru(cam[0])
        mc.viewFit(cam[1], all=True)
        # 35도 all frame view 만들기
        group_name = '%s_GRP' % cam[0]
        cam_group = mc.group(em=1, n=group_name)
        # 카메라 그룹 만들기
        mc.parent(cam, cam_group)
        # 위치가 (0,0,0)인 그룹에 카메라 페런트
        mc.currentTime(1)
        mc.setKeyframe("%s.ry" % cam_group)
        mc.currentTime(120)
        mc.setAttr("%s.rotateY" % cam_group, 360)
        mc.setKeyframe("%s.ry" % cam_group)
        # 1~120프레임 카메라그룹 rotateY값에 360도 키설정

        # 동일한 파일명 있는지 확인 후 존재하면 file name의 suffix 올림
        filename = '_main'
        extension = 'mov'
        if os.path.exists(path + filename + '.' + extension):
            i = 1
            while os.path.exists(path + filename + '_%02d.' % i + extension):
                i += 1
            filename = filename + '_%02d' % i

        # 모든 카메라와 언디img를 안 보이게 꺼줌
        all_cameras = mc.ls(type='camera', l=True)
        for camera in all_cameras:
            mc.setAttr("%s.visibility" % camera, False)

        # 플레이블라스트 mov출력
        mc.playblast(
            format='movie',
            filename=path+filename,
            sequenceTime=False,
            clearCache=True, viewer=True,
            showOrnaments=True,
            fp=4, percent=50,
            compression=extension,
            quality=50,
            startTime=0,
            endTime=300
        )
        mc.delete(cam_group)
        # 프리뷰용 카메라 그룹지우기

    def export_output_n_main_preview_file(self, path, preview_path):
        """
        작업한 파일을 output file로 저장하는 매서드(.mb)
        각 카메라 별 저용량 preview 파일도 mov로 저장한다.

        Args:
            path(str): output file을 저장할 확장자를 제외한 경로
            preview_path(str): preview file을 저장할 확장자를 제외한 경로
        """
        # output file 저장
        self.save_scene_file(path, 'mb')

        # main preview file 저장
        self._make_main_preview_mov(preview_path)
        
    def export_shot_previews(self, path, shot):
        """
        각 샷에 해당하는 preview 영상을 저장하는 매서드

        Args:
            path(str): preview 파일의 확장자를 뺀 전체 경로
            shot(dict): preview 파일을 저장할 shot의 딕셔너리
        """
        # 디폴트 카메라 필터링 후 사용자가 커스텀한 카메라 목록을 추출
        startup_cameras = []
        all_cameras = mc.ls(type='camera', l=True)
        for camera in all_cameras:
            if mc.camera(mc.listRelatives(camera, parent=True)[0], startupCamera=True, q=True):
                startup_cameras.append(camera)
        custom_camera = list(set(all_cameras) - set(startup_cameras))

        # shot의 언디스토션 이미지들을 저장한 폴더로부터 프레임 레인지를 추출
        undi_seq_path = self.kit.get_undistortion_img(shot)
        file_list = os.listdir(os.path.dirname(undi_seq_path))
        frame_range = len(file_list)

        # 다른 카메라랑 이미지플레인 다 끄고, 샷에 해당하는 카메라만 켜서 플레이블라스트 프리뷰 저장
        shot_name = shot['name']
        for camera in custom_camera:
            if shot_name not in camera:
                mc.setAttr("%s.visibility" % camera, False)
                continue
            else:
                mc.setAttr("%s.visibility" % camera, True)
                mc.lookThru(camera)
                mc.playblast(
                    format='movie',
                    filename=path,
                    sequenceTime=False,
                    clearCache=True, viewer=True,
                    showOrnaments=True,
                    percent=50,
                    compression="mov",
                    quality=50,
                    startTime=0,
                    endTime=frame_range
                )
                mc.setAttr("%s.visibility" % camera, False)
                # 켰던 카메라 다시 꺼줌
