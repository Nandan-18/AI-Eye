#main function
import pygame as pg
import sys
import os
from scripts import ui, dialouge

class Game:
    def __init__(self) -> None:
        pg.init()
        info = pg.display.Info()
        w = info.current_w
        h = info.current_h
        os.environ["SDL_VIDEO_CENTERED"] = '1'
        self.win  = pg.display.set_mode((w, h-30), pg.RESIZABLE)
        self.clock = pg.time.Clock()
        self.fps = 60


        pg.display.set_caption("Game")


    def load(self):
        self.text_input = ui.TextInput((100,100), "pizza")
        self.button = ui.Button((10,10), (100, 50),"hey")

        self.dialogue_sys = dialouge.DialougeSystem()


    def update(self):
        pg.display.update()
        self.clock.tick(self.fps)
        mouse_pos = pg.mouse.get_pos()
        mouse_buttons = pg.mouse.get_pressed()
        events = pg.event.get()
        for event in events:
            if event.type == pg.VIDEORESIZE:
                self.win = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
            if event.type == pg.QUIT:
                self.quit()
                
        self.text_input.update(events)
        self.button.update(mouse_buttons, mouse_pos)
        self.dialogue_sys.update()


        
    
    def draw(self):
        self.win.fill((0,0,0))
        self.text_input.draw(self.win)
        self.button.draw(self.win)
        self.dialogue_sys.draw(self.win)


    def run(self):
        self.load()
        while True:
            self.update()
            self.draw()
    
    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
