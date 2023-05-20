#main function
import pygame as pg
import sys
from scripts import ui

class Game:
    def __init__(self) -> None:
        pg.init()
        self.win = pg.display.set_mode(size=(1000,500))
        self.clock = pg.time.Clock()

        self.fps = 60

        pg.display.set_caption("Game")


    def load(self):
        self.text_input = ui.TextInput((100,100), "pizza")


    def update(self):
        for event in pg.event.get():
            self.text_input.update(event)

            if event.type == pg.QUIT:
                self.quit()
                
        
        pg.display.update()
        self.clock.tick(self.fps)
    
    def draw(self):
        self.win.fill((0,0,0))
        self.text_input.draw(self.win)

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
