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
                self.button = ui.Button((200,50), (400, 50),"AI Game Jam Game")
            if self.playing == True:
                self.text_input = ui.TextInput((100,100), "pizza")
                self.button = ui.Button((10,10), (100, 50),"hey")


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
        if self.button.clicked == mouse_pos and self.playing == False:
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
