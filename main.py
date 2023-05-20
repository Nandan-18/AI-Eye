#main function
import pygame as pg
import sys

class Game:
    def __init__(self) -> None:
        pg.init()
        self.win = pg.display.set_mode(size=(500,500))
        self.clock = pg.time.Clock()

        self.fps = 60

        pg.display.set_caption("Game")


    def load(self):
        pass

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
                
        
        pg.display.update()
        self.clock.tick(self.fps)

    def run(self):
        self.load()
        while True:
            self.update()
    
    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
