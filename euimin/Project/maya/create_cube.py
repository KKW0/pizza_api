import maya.cmds as cmds

# 큐브의 높이와 너비 값을 설정
def CreateSmoothedCube(user_chosen_name='pCube1', height=1):
    if not cmds.objExists(user_chosen_name):
        cub = cmds.polyCube(name=user_chosen_name, h=height)
        var = cub[1]
    else:
        var = [i for i in cmds.listHistory(user_chosen_name) if cmds.nodeType(user_chosen_name)=='polyCube']
        cmds.setAttr("{}.height".format(var[0]), height)
    return [user_chosen_name, var]


def CreateSmoothedCube(user_chosen_name, **kwargs):
    cub = cmds.polyCube(name=user_chosen_name, **kwargs)
    return cub


cub = CreateSmoothedCube('my_name', h=5, w=10)
print(cub)