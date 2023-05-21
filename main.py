#main function
import pygame as pg
import sys
import logging
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
            self.image = pg.surface.Surface((512,512))
            self.word = utils.FileUtils.get_random_word()

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
            if self.playing == True:
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
                        logging.info("Generating image...")
                        image_bytes = loop.run_until_complete(coroutine)
                        logging.info("Image generated!")

                        # Pygame needs a name for the image file even if it's 
                        # not going to be saved, so we just use a placeholder.
                        self.image = pg.image.load(
                            image_bytes, "assets/placeholder.svg"
                        )

                        # Get a new word for the next round
                        self.word = utils.FileUtils.get_random_word()

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

        if self.playing == True:
            self.win.blit(pg.transform.scale(
                self.image, 
                tuple(stable_diffusion_client.image_dimensions)), 
                (0,200),
            )

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
