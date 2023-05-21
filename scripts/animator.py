import pygame as pg
import os

class Animator:
    def __init__(self, folder : str, duration : int, scale) -> None:
        self.images_filenames = [file for file in os.listdir(folder)]
        self.images = [pg.image.load(os.path.join(folder, filename)) for filename in self.images_filenames]
        self.images = [pg.transform.smoothscale_by(img, 0.2) for img in self.images]

        self.duration = duration # in frames not seconds

        self.frame_count = 0
        self.img_frame = 0
    
    def next_frame(self):
        self.img_frame = (self.img_frame + 1) % len(self.images)
    
    def update(self):
        self.frame_count += 1
        if self.frame_count >= self.duration:
            self.next_frame()
            self.frame_count = 0

    def get_frame(self):
        return self.images[self.img_frame]
    
    def get_size(self):
        return self.images[self.img_frame].get_size()
