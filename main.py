# main function
import pygame as pg
import sys
import logging
import os
from scripts import entities, dialogue, ui, progress_bar, scoring
from clients import stable_diffusion
from clients import utils
import asyncio


class Game:
    def __init__(self) -> None:
        pg.mixer.pre_init(16000, -16, 2, 2048)
        pg.init()
        info = pg.display.Info()
        w = info.current_w
        h = info.current_h
        os.environ["SDL_VIDEO_CENTERED"] = '1'
        self.win = pg.display.set_mode((w, h-30), pg.RESIZABLE)
        self.clock = pg.time.Clock()
        self.fps = 60

        pg.display.set_caption("Game")

        self.playing = False

        self.click = pg.mixer.Sound("sounds/Click.mp3")
        self.wrong_answer = pg.mixer.Sound("sounds/WrongAnswerShake.mp3")
        self.right_answer = pg.mixer.Sound("sounds/GoodAnswerDing.mp3")

        # Create an instance of the Score class
        self.score = scoring.Score(1)

    def load(self):
        if self.playing == False:
            self.text_input = ui.TextInput((100, 100), "AI Game Jam Game")
            self.button = ui.Button((275, 200), (400, 50), "Start")
            pg.mixer.music.load('sounds/JeopardyTypeBeat.mp3')
            pg.mixer.music.play(-1)
            self.mute_button = ui.Button((800, 10), (100, 50), "Mute")
 

        if self.playing == True:
            self.text_input = ui.TextInput((100,100), "", True)
            self.button = ui.Button((10,10), (100, 50),"hey")
            self.image = pg.surface.Surface((512,512))

            pg.mixer.music.load('sounds/Suspense.mp3')
            pg.mixer.music.play(-1)

        self.word = utils.FileUtils.get_random_word()
        self.has_generated_image = False
        self.dialogue_sys = dialouge.DialougeSystem()


    def update(self):
        pg.display.update()
        self.clock.tick(self.fps)
        mouse_pos = pg.mouse.get_pos()
        mouse_buttons = pg.mouse.get_pressed()
        events = pg.event.get()
        for event in events:
            if event.type == pg.VIDEORESIZE:
                self.win = pg.display.set_mode(
                    (event.w, event.h), pg.RESIZABLE)

            if event.type == pg.QUIT:
                self.quit()

            if self.playing == True:
                preprompt = "Isometic art of "
                prompt = preprompt + self.word

                logging.info("Generating image...")
                image_bytes = stable_diffusion_client.run_new(
                    prompt=prompt,
                )

                # Pygame needs a name for the image file even if it's 
                # not going to be saved, so we just use a placeholder.
                self.image = pg.image.load(
                    image_bytes, "assets/placeholder.svg"
                )
                logging.info("Image generated!")

        self.text_input.update(events)
        self.button.update(mouse_buttons, mouse_pos)
        self.dialogue_sys.update(events)
        self.mute_button.update(mouse_buttons, mouse_pos)


        if self.text_input.shake == 30:
            self.wrong_answer.play()

        # load main game
        if self.button.clicked and self.playing == False:
            self.click.play()
            self.playing = True
            self.load()

        # mute audio
        if self.mute_button.clicked:
            pg.mixer.music.stop()

    def draw(self):
        self.win.fill((0, 200, 200))
        self.text_input.draw(self.win)
        self.dialogue_sys.draw(self.win)

        if self.playing == True:
            self.win.blit(pg.transform.scale(
                self.image,
                tuple(stable_diffusion_client.image_dimensions)),
                (0, 200),
            )

    #def draw_start_screen(self):
    #    self.win.fill((250, 248, 246))
     #   self.button.draw(self.win)
      #  self.mute_button.draw(self.win)


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
