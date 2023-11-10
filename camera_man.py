from watches import *
from teleport import *
import pyautogui

# Hook Python to Dolphin.
dme.hook()

# Set Watch Variables.
cutscene_count = get_watch("Cutscene Count")
cam_target_x = get_watch("Camera Target X")
cam_target_y = get_watch("Camera Target Y")
cam_target_z = get_watch("Camera Target Z")
cam_pos_x = get_watch("Camera Position X")
cam_pos_y = get_watch("Camera Position Y")
cam_pos_z = get_watch("Camera Position Z")
cam_mode = get_watch("Camera Mode")
mario_x = get_watch("Mario_X")
mario_y = get_watch("Mario_Y")
mario_z = get_watch("Mario_Z")
fov_y = get_watch("FOV Y")

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
print(fov_y.read())

for map in description:
    teleport(map)
    time.sleep(5)

    cam_mode.write(3)
    cutscene_count.write(1)

    cam_target_x.write(0)
    cam_target_y.write(0)
    cam_target_z.write(0)

    cam_pos_x.write(0)
    cam_pos_y.write(100)
    cam_pos_z.write(1000)
    fov_y.write(100)
    time.sleep(1)

    mario_x.write(0)
    mario_y.write(-1000)
    mario_z.write(-1000)

    pyautogui.leftClick()
    time.sleep(5)
