import maya.cmds as mc
import gazu
import os

class MayaLayout:
    def __init__(self):
        pass

    @staticmethod
    def import_out_file(path):
        """

        Args:
            path: 입력한 project, sequence, shot과 관련된 캐스팅 파일 패스

        Returns: import한 리스트

        """
        output_files = mc.file(
            path, i = 1, ignoreVersion = 1,
            mergeNamespacesOnClash=0,importTimeRange="combine",
            loadReferenceDepth  = "all",
            returnNewNodes=True
        )
        return output_files

    def get_casting_path(self, project, sequence, shot):
        """

        Args:
            project: project_dict
            sequence: sequence_dict
            shot: shot_dict

        Returns: 입력한 project, sequence, shot과 관련된 캐스팅 안 어셋 패스리스트

        """
        pick_sequence = gazu.shot.get_sequence_by_name(project, sequence)
        pick_shot = gazu.shot.get_shot_by_name(pick_sequence, shot)
        casting_shot = gazu.casting.get_shot_casting(pick_shot)
        full_path_list = []

        for asset in casting_shot:
            print(f'asset name      : {asset.get("asset_name")} \n'
                  f'asset type      : {asset.get("asset_type_name")}')
            tasks = gazu.task.all_tasks_for_asset(asset.get('asset_id'))
            for task in tasks:
                last_revision = gazu.files.get_last_working_file_revision(task)

            basename_list = os.path.basename(last_revision.get("path"))
            path = os.path.dirname(last_revision.get("path"))
            for basename in basename_list:
                full_path = path + "/" + basename
                full_path_list.append(full_path)

        return full_path_list

    def get_output_file_for_shot(self, project, sequence, shot, output_type, task_type):
        """

        Args:
            project: project_dict
            sequence: sequence_dict
            shot: shot_dict
            output_type: output_type_dict
            task_type: task_type_dict

        Returns: 원하는 shot에 관련한 아웃풋 파일 패스리스트

        """
        pick_sequence = gazu.shot.get_sequence_by_name(project, sequence)
        pick_shot = gazu.shot.get_shot_by_name(pick_sequence, shot)
        output = gazu.files.get_output_type_by_name(output_type)
        task_types = gazu.task.all_task_types_for_shot(pick_shot)
        undistortion_list = []
        for a in task_types:
            if a.get('name') == task_type:
                task_type = a
        get_output_file = gazu.files.all_output_files_for_entity(pick_shot, output, task_type)
        output_file_path = get_output_file.get('path')
        for file_path in output_file_path:
            if file_path.split("/")[-1][-3:] == "jpg":
                undistortion_list.append(file_path)
        return undistortion_list

    def get_working_path_for_shot(self, project, sequence, shot, task_type):
        """

        Args:
            project: project_dict
            sequence: sequence_dict
            shot: shot_dict
            task_type: task_type_dict

        Returns: 씬파일을 내보낼 워킹 파일패스

        """
        pick_sequence = gazu.shot.get_sequence_by_name(project, sequence)
        pick_shot = gazu.shot.get_shot_by_name(pick_sequence, shot)
        tasks = gazu.task.all_tasks_for_shot(pick_shot)
        for a in tasks:
            if a.get('task_type_name') == task_type:
                task = a
        last_revision = gazu.files.get_last_working_file_revision(task)
        working_file_path = os.path.dirname(
            gazu.files.build_working_file_path(task, revision=last_revision.get('revision')+1)
        )
        return working_file_path

    def setting_scene(self, project, sequence, shot, output_type, task_type):
        """

        Args:
            project: project_dict
            sequence: sequence_dict
            shot: shot_dict
            output_type: output_type_dict
            task_type: task_type_dice

        Returns: 캐스팅파일 임포트 > 카메라에 이미지연결 > 플레이블라스트 출력 > 워킹파저장일

        """
        casting_asset_path_list = self.get_casting_path(project, sequence, shot)
        undistortion_path_list = self.get_output_file_for_shot(project, sequence, shot, output_type, task_type)
        working_file_path_list = self.get_working_path_for_shot(project, sequence, shot, task_type)
        cam_list = []
        mesh_list = []
        maya_format = ""
        for p in casting_asset_path_list:
            output_file = self.import_out_file(p)
            if mc.objectType(output_file) == "camera":
                cam = mc.listRelatives(output_file, p=1)
                cam_list.append(cam)

            elif mc.objectType(output_file) == "mesh":
                mesh = mc.listRelatives(output_file, p=1)
                mesh_list.append(mesh)
        mc.group(cam_list, n="cam_GRP")
        mc.group(mesh_list, n="asset_GRP")
        self.connect_image(undistortion_path_list[0], cam_list[0])
        self.export_playblast(working_file_path_list, cam_list[0])
        self.save_working_file("플레이블라스트 저장할패스",maya_format)

    @staticmethod
    def connect_image(path, camera):
        """

        Args:
            path: undistortion이미지 파일경로
            camera: 캐스팅에 있는 카메라

        Returns: 카메라에 이미지 연결 후 시퀀스 옵션체크

        """
        image_plane = mc.imagePlane(c=camera)
        mc.setAttr('%s.imageName' % image_plane[0], path, type='string')
        mc.setAttr("%s.useFrameExtension" % image_plane[0], 1)

    @staticmethod
    def export_playblast(path, camera):
        """

        Args:
            path: 플레이블라스 내보낼 파일경로
            camera: 뷰포트 카메라

        Returns: 아웃풋파일에다가 플레이블라스트 시퀀스 출력

        """
        output_path = path
        mc.lookThru(camera)
        mc.playblast(
            format='image',
            filename='%s'%output_path,
            sequenceTime=0,
            clearCache=1, viewer=1,
            showOrnaments=1,
            fp=4, percent=50,
            compression="jpg",
            quality=100
        )

    @staticmethod
    def save_working_file(path, format):
        """

        Args:
            path: 저장할 경로 + 이름
            format: "mayaAscii","mayaBinary" 둘중하나

        Returns: 포맷을 받아서 원하는 형식으로 저장한.

        """
        if format == "mayaAscii":다
            mc.file(rename = "%s"%path + ".ma")
        elif format == "mayaBinary":
            mc.file(rename = "%s"%path + ".mb")
        mc.file(save = True, type = format)

def main():
    ml = MayaLayout()
    # ml.setting_scene(project, sequence, shot, output_type, task_type)

if __name__ == "__main__":
    main()