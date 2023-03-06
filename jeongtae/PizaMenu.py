import maya.cmds as mc

if mc.menu('pizzaMenu',exists=True):
    mc.menu('pizzaMenu', e=True, dai=True)
else:
    mc.setParent('MayaWindow')
    mc.menu('pizzaMenu', l="Pizza", p='MayaWindow', to=True)
    
mc.setParent(menu=True)
    
mc.menuItem(l="Pizza", sm=True, to=True)
mc.menuItem(l="Pizza_API", c="source \"/home/rapa/maya/2020/scripts/PJT_2st/Maya_Api.py\"; main();", ann="Open the Pizza.", image="pizza_API.png")
mc.setParent(menu=True)
