import maya.cmds as cmds
import os

srtfrm = cmds.getAttr('defaultRenderGlobals.startFrame')
endfrm = cmds.getAttr('defaultRenderGlobals.endFrame')
filePath = cmds.file(q=True, sn=True)
fileName = os.path.basename(filePath)
plbPath = filePath.replace(fileName,"")
cmds.lookThru('camera1')
cmds.playblast(f=plbPath+fileName[:-3], fo=True, fmt='qt', c='H.264',
               w=1280, h=720, p=100, qlt=100, orn=False, st=srtfrm,
               et=endfrm, v=False, os=True)