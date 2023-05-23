import pygame as pg
from .animator import Animator

class Entity:
    def __init__(self, pos, folders, scale, init_state, dur=5) -> None:
        self.pos = pos
        self.anim = Animator(folders, dur, scale, init_state)
    
    def update(self, events):
        self.anim.update()
    
    def draw(self, win : pg.Surface):
        win.blit(self.anim.get_frame(), self.pos)
    
    def get_height(self):
        return self.anim.get_frame().get_height()

    def get_width(self):
        return self.anim.get_frame().get_width()