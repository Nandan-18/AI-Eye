#main function
import pygame as pg
import sys
import logging
from scripts import ui

class Game:
    def __init__(self) -> None:
        pg.init()
        self.win = pg.display.set_mode(size=(1000,500))
        self.clock = pg.time.Clock()

        self.fps = 60

        pg.display.set_caption("Game")

        self.playing = False


    def load(self):
            if  self.playing == False:
                self.text_input = ui.TextInput((100,100), "AI Game Jam Game")
                self.button = ui.Button((275,200), (400, 50),"Start")

                pg.mixer.music.load('sounds/JeopardyTypeBeat.mp3')
                pg.mixer.music.play(-1)
                
            if self.playing == True:
                self.text_input = ui.TextInput((100,100), "pizza")
                self.button = ui.Button((10,10), (100, 50),"hey")

                pg.mixer.music.load('sounds/Suspense.mp3')
                pg.mixer.music.play(-1)


    def update(self):
        pg.display.update()
        self.clock.tick(self.fps)
        mouse_pos = pg.mouse.get_pos()
        mouse_buttons = pg.mouse.get_pressed()
        events = pg.event.get()
        for event in events:

            if event.type == pg.QUIT:
                self.quit()
                
        self.text_input.update(events)
        self.button.update(mouse_buttons, mouse_pos)

        #load main game
        if self.button.clicked and self.playing == False:
            self.playing = True
            self.load()
        
    
    def draw(self):
        self.win.fill((0,0,0))
        self.text_input.draw(self.win)
        self.button.draw(self.win)

    def draw_start_screen(self):
        self.win.fill((250,248,246))
        self.button.draw(self.win)

    def run(self):
        self.load()

        while True:
            self.update()

            if self.playing == False:
                self.draw_start_screen()
            if self.playing == True:
                self.draw()
    
    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
