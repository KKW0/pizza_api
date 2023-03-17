import maya.cmds as mc
import sys

sys.path.append('/home/rapa/git/pizza/python')

if mc.menu('pizzaMenu',exists=True):
    mc.menu('pizzaMenu', e=True, dai=True)
else:
    mc.setParent('MayaWindow')
    mc.menu('pizzaMenu', l="Pizza", p='MayaWindow', to=True)
    
mc.setParent(menu=True)
    
mc.menuItem(l="Pizza", sm=True, to=True)
mc.menuItem(l="Pizza_API", c="import Maya_Api; app = UI_controller.MainWindow();", ann="Open the Pizza.", image="pizza_API.jpg")
mc.setParent(menu=True)
reload(Maya_Api)
