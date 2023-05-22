

import os

folder_name = "assets/avatar_neutral"

for file in os.listdir(folder_name):
    if "neutral_left-" in file:
        os.rename(folder_name + "/"+file, folder_name + "/"+file.split("-")[-1][:-4] + ".png")