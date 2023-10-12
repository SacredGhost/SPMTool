from watches import *

# Hook Python to Dolphin.
dme.hook()

# Set Watch Variables.
cutescene_count = get_watch("Cutscene Count")
cam_target_x = get_watch("Camera Target X")
cam_target_y = get_watch("Camera Target Y")
cam_target_z = get_watch("Camera Target Z")
cam_pos_x = get_watch("Camera Position X")
cam_pos_y = get_watch("Camera Position Y")
cam_pos_z = get_watch("Camera Position Z")
mario_x = get_watch("Mario_X")
mario_y = get_watch("Mario_Y")
mario_z = get_watch("Mario_Z")
fov_y = get_watch("FOV Y")


# Rest of the code...
print(cam_target_x.read())
print(cam_target_y.read())
print(cam_target_z.read())
print()
print(cam_pos_x.read())
print(cam_pos_y.read())
print(cam_pos_z.read())
print()
print(mario_x.read())
print(mario_y.read())
print(mario_z.read())
