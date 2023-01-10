import maya.cmds as mc

mesh=mc.ls(sl=1)
meshShape=mc.listRelatives(mesh,s=1)[0]
skin=mc.listConnections(meshShape,type="skinCluister")[0]
skinJNT=mc.listConnections(skin+'.matrix')
