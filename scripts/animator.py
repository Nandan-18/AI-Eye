import pygame as pg
import os

class Animator:
    # states is a list of state foldernames 
    def __init__(self, states : list, duration : int, scale, init_state) -> None:
        self.images_filenames = {folder : sorted([file for file in os.listdir(folder)], key=lambda x : int(x[:-4])) for folder in states}

        self.images = {folder.split("/")[-1] :[pg.image.load(os.path.join(folder, filename)) for filename in filenames] for folder, filenames in self.images_filenames.items()}
        self.images = {state :[pg.transform.smoothscale_by(img, 0.2) for img in imgs] for state, imgs in self.images.items()}
        self.cur_state = init_state
        self.duration = duration # in frames not seconds

        self.frame_count = 0
        self.img_frame = 0
    
    def next_frame(self):
        self.img_frame = (self.img_frame + 1) % len(self.images[self.cur_state])
    
    def update(self):
        self.frame_count += 1
        if self.frame_count >= self.duration:
            self.next_frame()
            self.frame_count = 0

    def set_state(self, state):
        self.cur_state = state

    def get_frame(self):
        
        return self.images[self.cur_state][self.img_frame  % len(self.images[self.cur_state])]
    
    def get_size(self):
        return self.images[self.cur_state][self.img_frame].get_size()
