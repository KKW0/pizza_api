import maya.cmds as cmds

# cmds.polySphere()

path = "/home/rapa/test.fbx"
cmds.file(path, i=1, type="FBX", ignoreVersion=1, ra=1,
        mergeNamespacesOnClash=0, rpr="cam", options="fbx",
        pr=1, importTimeRange="combine"
)

image_plane = cmds.imagePlane(camera="cameraShape1")
path2 = "/home/rapa/test.jpeg"
cmds.setAttr('%s.imageName'%image_plane[0], path2, type='string')
cmds.setAttr("%s.useFrameExtension"%image_plane[0], 1)


cmds.playblast(format='image',
               filename="/home/rapa/git/pizza/euimin/Project/maya/playblast_test/playblast_test",
               sequenceTime=0, clearCache=1, viewer=1,
               showOrnaments=1, fp=4, percent=50,
               compression="jpg", quality=100)

# import sys
# sys.path.append('/home/rapa/git/pizza/euimin/Project/maya')
# import maya_test
# reload(maya_test)