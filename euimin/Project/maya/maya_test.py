import maya.cmds as cmds

# cmds.polySphere()
#
# path = "/home/rapa/test.fbx"
# cmds.file(path, i=1, type="FBX", ignoreVersion=1, ra=1,
#         mergeNamespacesOnClash=0, rpr="cam", options="fbx",
#         pr=1, importTimeRange="combine"
# )
#
# image_plane = cmds.imagePlane(camera="camera1")
# path2 = "/home/rapa/test.jpeg"
# cmds.setAttr('%s.imageName'%image_plane[0], path2, type='string')
# cmds.setAttr("%s.useFrameExtension"%image_plane[0], 1)
#
# cmds.lookThru('camera1')
#
# cmds.playblast(format='image',
#                filename="/home/rapa/git/pizza/euimin/Project/maya/playblast_test/playblast_test",
#                sequenceTime=0, clearCache=1, viewer=1,
#                showOrnaments=1, fp=4, percent=50,
#                compression="jpg", quality=100)

class Playblast:
    def __init__(self):
        self._fbx_path = None
        self._img_path = None
        self._playblast_path = None

    def cma_path(self):
        cmds.file(self._fbx_path, i=1, type="FBX", ignoreVersion=1,
                  mergeNamespacesOnclash=0, rpr="cam", options="FBX",
                  pr=1, importTimeRange="combine")

    def set_imageplan(self):
        image_plane = cmds.imagePlane(c="camera1")
        cmds.setAttr("%s.imageName" % image_plane[0], self._img_path, type="string")
        cmds.setAttr("%s.useFrameExtension" % image_plane[0], 1)

    def look_thru_camera(self):
        cmds.lookThru('camera1')

    def playblast(self):
        path = self._playblast_path
        cmds.playblast(format='image', filename='%s'%path,
                       sequenceTime=0, clearCache=1, viewer=1,
                       showOrnaments=1, fp=4, percent=50,
                       compression="jpg", quality=100)

def main():
    pb = Playblast()
    pb._fbx_path = "/home/rapa/test.fbx"
    pb._img_path = "/home/rapa/test.jpeg"
    pb._playblast_path = "/home/rapa/git/pizza/euimin/Project/maya/playblast_test/playblast_test"

    pb.cma_path()
    pb.set_imageplan()
    pb.look_thru_camera()
    pb.playblast()


if __name__ == "__main__":
    main()
# import sys
# sys.path.append('/home/rapa/git/pizza/euimin/Project/maya')
# import maya_test
# reload(maya_test)