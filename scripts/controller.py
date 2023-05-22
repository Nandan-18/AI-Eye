import pygame as pg
from .dialogue import DialogueSystem
from .scoring import Score
from .ui import TextInput
from .progress_bar import ProgressBar
from .img_gen import ImageGen
from clients import stable_diffusion


class GameController:
    def __init__(self) -> None:
        self.round = 0
        self.dialouge_sys = DialogueSystem()
        self.score = Score(self.round+1)
        self.timer = ProgressBar(200, 30, 60*20)
        self.text_input = TextInput((100, 100), "pizza")
        self.img_gen_client = ImageGen()
        #TODO: add a img generator class

    def update(self, events):
        self.dialouge_sys.update(events)
        self.timer.update()
        self.text_input.update(events)
        self.img_gen_client.update(events, self.text_input.get_cur_word())

    def draw(self, win : pg.Surface):
        self.dialouge_sys.draw(win)
        self.score.draw(win)
        self.timer.draw(win, win.get_width() // 2 - self.timer.width // 2, win.get_height() - 50)
        self.text_input.draw(win)
        self.img_gen_client.draw(win)