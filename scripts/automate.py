

import os

folder_name = "assets/robo_idle"

for file in os.listdir(folder_name):
    if "animated_idle-" in file:
        os.rename(folder_name + "/"+file, folder_name + "/"+file.split("-")[-1][:-4] + ".png")