
import pygame as pg

class DialougeSystem:
    def __init__(self,spacing=15, text_size=12) -> None:
        self.font = pg.font.Font('font/Cascadia.ttf', text_size)
        self.host_icon = pg.image.load("assets/dialogue_host.png")
        self.host_icon = pg.transform.smoothscale_by(self.host_icon, 0.2)
        self.talking = False
        self.text = ""
        self.frame_count = 0
        self.visible = False
        self.spacing = spacing 

    def start_talking(self, text, duration):
        self.frame_count = int(duration*60)
        self.talking = True
        self.text = text

    def update(self):
        if self.visible:
            pass
            

    def draw(self, win : pg.Surface):
        pos = (self.spacing, win.get_height() - self.spacing - self.host_icon.get_height())
        # print(win.get_height(),self.host_icon.get_height(),self.spacing, pos)
        win.blit(self.host_icon, pos)
