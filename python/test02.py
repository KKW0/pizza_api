import gazu

startup_cameras = []
shot_name_list = []
shot_dict_list = []
all_cameras = mc.ls(type='camera', l=True)
for camera in all_cameras:
    if mc.camera(mc.listRelatives(camera, parent=True)[0], startupCamera=True, q=True):
        startup_cameras.append(camera)
custom_camera = list(set(all_cameras) - set(startup_cameras))

if custom_camera:
    for x in custom_camera:
        shot_name_list.append(x.split("_")[2])

for i in shot_name_list:
    shot_dict = gazu.shot.get_shot_by_name(i)
    seq=gazu.shot.get_sequence_by_name()
    gazu.shot.all_shots_for_sequence(seq)
    shot_dict_list.append(shot_dict)

for shot_dict in shot_dict_list:
    save_publish(shot_dict,coment=None)

