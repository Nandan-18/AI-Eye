#main function
import pygame as pg
import sys
from scripts import ui
from clients.stable_diffusion import stable_diffusion_client
from clients import utils
import asyncio

class Game:
    def __init__(self) -> None:
        pg.init()
        self.win = pg.display.set_mode(size=(1000,1000))
        self.clock = pg.time.Clock()

        self.fps = 60

        pg.display.set_caption("Game")


    def load(self):
        self.text_input = ui.TextInput((100,100), "pizza")
        self.image = pg.surface.Surface((512,512))
        self.word = utils.FileUtils.get_random_word()


    def update(self):
        for event in pg.event.get():
            self.text_input.update(event)

            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                # If you press RIGHT arrow key, run synchronously
                if event.key == pg.K_RIGHT:
                    image_bytes = stable_diffusion_client.run(
                        prompt="A dog holding a gameboy console",
                    )
                    self.image = pg.image.load(
                        image_bytes, "assets/placeholder.svg"
                    )
                # If you press LEFT arrow key, run asynchronously
                elif event.key == pg.K_LEFT:
                    # Change this to change the style of the art
                    preprompt = "Isometic art of "

                    prompt = preprompt + self.word

                    # Load placeholder while the image is generating
                    self.image = pg.image.load(
                        "assets/placeholder.svg"
                    )

                    loop = asyncio.get_event_loop()
                    coroutine = stable_diffusion_client.arun(
                        prompt=prompt
                    )
                    image_bytes = loop.run_until_complete(coroutine)

                    # Pygame needs a name for the image file even if it's 
                    # not going to be saved, so we just use a placeholder.
                    self.image = pg.image.load(
                        image_bytes, "assets/placeholder.svg"
                    )

                    # Get a new word for the next round
                    self.word = utils.FileUtils.get_random_word()
        
        pg.display.update()
        self.clock.tick(self.fps)
    
    def draw(self):
        self.win.fill((0,0,0))
        self.text_input.draw(self.win)

        self.win.blit(pg.transform.scale(
            self.image, 
            tuple(stable_diffusion_client.image_dimensions)), 
            (0,200),
        )

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
