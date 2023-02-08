import maya.cmds as mc

class MayaLayout:

    def __init__(self):
        pass

    def import_out_file(self):
        path = '임시경로'
        oupput_camera = []
        mc.file(path, i=1, ignoreVersion=1, options = "mo=0", mergeNamespacesOnClash=0, importTimeRange="combine",loadReferenceDepth  = "all")
        perspCameras = mc.listCameras(p=True)
        for x in perspCameras:
            if x not in 'persp':
                oupput_camera.append(x)
        return oupput_camera

    def connect_image(self):
        path = '임시경로'
        cam_list = self.import_out_file()
        image_plane = mc.imagePlane(c=cam_list[0])
        mc.setAttr('%s.imageName' % image_plane[0], path, type='string')
        mc.setAttr("%s.useFrameExtension" % image_plane[0], 1)
        return cam_list

    def export_playblast(self):
        cam_list = self.connect_image()
        output_path = '플레이블라스트 저장할 파일경로'
        mc.lookThru(cam_list[0])
        mc.playblast(
            format='image',
            filename=output_path,
            sequenceTime=0,
            clearCache=1, viewer=1,
            showOrnaments=1,
            fp=4, percent=50,
            compression="jpg",
            quality=100
        )

def main():
    ml = MayaLayout()
    ml.export_playblast()

if __name__ == "__main__":
    main()