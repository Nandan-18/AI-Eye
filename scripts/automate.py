

import os

folder_name = "assets/robo_talking"

for file in os.listdir(folder_name):
    if "reallllly_rough_animation-" in file:
        os.rename(folder_name + "/"+file, folder_name + "/"+file.split("-")[-1][:-4] + ".png")