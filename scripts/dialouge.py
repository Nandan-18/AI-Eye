
import pygame as pg

HARD_CONSONANTS = ['q', 't', 'p', 'd', 'g', 'j', 'k', 'x', 'c', 'b']
SOFT_CONSONANTS = ['w', 'r', 'y', 's', 'f', 'h', 'l', 'z', 'v', 'n', 'm']

class DialougeSystem:
    def __init__(self,spacing=15, text_size=32) -> None:
        self.font = pg.font.Font('font/Cascadia.ttf', text_size)
        self.host_icon = pg.image.load("assets/dialogue_host.png")
        self.host_icon = pg.transform.smoothscale_by(self.host_icon, 0.2)
        self.talking = False
        self.text = ""
        self.visible = True
        self.spacing = spacing
        self.frame_count = 0
        self.frame_skip = 0
        self.font_surf = None
        self.key_surf = pg.image.load("assets/X_Key_Dark.png")
        self.key_sound = pg.mixer.Sound("assets/chungu.wav") 

    def start_talking(self, text, frame_skip : int ):
        self.talking = True
        self.text = text
        self.frame_count = frame_skip*len(text)
        self.frame_skip = frame_skip

    def update(self, events):
        if self.visible:
            for event in events:
                if event.type == pg.KEYDOWN and event.key == pg.K_x:
                    self.start_talking("hello this is me the host", 5)

            if self.frame_count > 0:
                cur_letter_idx = int((self.frame_skip*len(self.text)-self.frame_count)/self.frame_skip)
                self.frame_count -= 1
                if self.frame_count % self.frame_skip == 0:
                    self.font_surf = self.font.render(self.text[:cur_letter_idx+1], True, [255,255,255])
                    
                    if self.text[cur_letter_idx] in HARD_CONSONANTS:
                        pg.mixer.music.set_volume(0.5)
                    if self.text[cur_letter_idx] in SOFT_CONSONANTS:
                        pg.mixer.music.set_volume(0.3)
                    self.key_sound.play()

            else:
                self.talking = False
            
    def draw(self, win : pg.Surface):
        if self.visible:
            pos = (self.spacing, win.get_height() - self.spacing - self.host_icon.get_height())
            # print(win.get_height(),self.host_icon.get_height(),self.spacing, pos)
            win.blit(self.host_icon, pos)
            if self.font_surf:
                win.blit(self.font_surf, (pos[0] + self.host_icon.get_width(), pos[1] + self.host_icon.get_height()//3))
            if not self.talking:
                win.blit(self.key_surf, (win.get_width() - self.spacing - self.key_surf.get_width(), win.get_height() - self.spacing - self.key_surf.get_height()))

