# main functionality

import pygame as pg
import sys
import logging
import os
from scripts import entities, dialogue, ui, progress_bar, scoring
from clients.stable_diffusion import stable_diffusion_client
from clients import utils
import asyncio


class Game:
    def __init__(self) -> None:
        pg.init()
        info = pg.display.Info()
        w = info.current_w
        h = info.current_h
        os.environ["SDL_VIDEO_CENTERED"] = '1'
        self.win = pg.display.set_mode((w, h-30), pg.RESIZABLE)
        self.clock = pg.time.Clock()
        self.fps = 60
        self.has_generated_image = False

        # Change this to change the style of art generated.
        self.preprompt = "Isometic voxel art of "

        pg.display.set_caption("Game")

        self.playing = False

        self.click = pg.mixer.Sound("sounds/Click.mp3")
        self.wrong_answer = pg.mixer.Sound("sounds/WrongAnswerShake.mp3")

        self.score = None
        self.progress_bar = None

    def main_menu(self):
        start_button = ui.Button(
            (self.win.get_width()//2-200, self.win.get_height()//2-25), (400, 50), "Start")
        mute_button = ui.Button(
            (self.win.get_width()//2-50, self.win.get_height()//40),  (100, 50), "Mute")
        pg.mixer.music.load('sounds/JeopardyTypeBeat.mp3')
        pg.mixer.music.play(-1)
        menu_playing = True
        while menu_playing:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()

            if start_button.clicked:
                self.click.play()
                menu_playing = False
                self.playing = True

            start_button.update(pg.mouse.get_pressed(), pg.mouse.get_pos())
            mute_button.update(pg.mouse.get_pressed(), pg.mouse.get_pos())

            # mute audio
            if mute_button.clicked:
                pg.mixer.music.stop()

            pg.display.update()
            self.win.fill((250, 248, 246))
            start_button.draw(self.win)
            mute_button.draw(self.win)

    def load(self):
        self.text_input = ui.TextInput((100, 100), "pizza")
        self.button = ui.Button((10, 10), (100, 50), "hey")
        self.score = scoring.Score(1)
        self.image = pg.surface.Surface((512, 512))
        self.word = utils.FileUtils.get_random_word()
        self.has_generated_image = False

        pg.mixer.music.load('sounds/Suspense.mp3')
        pg.mixer.music.play(-1)

        if self.playing == False:
            self.text_input = ui.TextInput((100, 100), "AI Game Jam Game")
            self.button = ui.Button((275, 200), (400, 50), "Start")

            pg.mixer.music.load('sounds/JeopardyTypeBeat.mp3')
            pg.mixer.music.play(-1)

        if self.playing == True:
            self.text_input = ui.TextInput((100, 100), "", True)
            self.button = ui.Button((10, 10), (100, 50), "hey")
            self.progress_bar = progress_bar.ProgressBar(200, 30, 1000)

            # Still need to make this transparent
            # self.image = pg.surface.Surface((512,512)).set_colorkey((0,0,0))
            self.image = pg.surface.Surface((512, 512))

            pg.mixer.music.load('sounds/Suspense.mp3')
            pg.mixer.music.play(-1)

        self.has_generated_image = False
        self.dialogue_sys = dialogue.DialogueSystem()
        self.word = utils.FileUtils.get_random_word()

    def update(self):
        pg.display.update()
        self.clock.tick(self.fps)
        mouse_pos = pg.mouse.get_pos()
        mouse_buttons = pg.mouse.get_pressed()

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.quit()

            if event.type == pg.VIDEORESIZE:
                self.win = pg.display.set_mode(
                    (event.w, event.h), pg.RESIZABLE)

            if self.playing == True:
                if self.has_generated_image == False:
                    prompt = self.preprompt + self.word

                    logging.info("Generating image...")
                    image_bytes = stable_diffusion_client.run(
                        prompt=prompt,
                    )

                    # Pygame needs a name for the image file even if it's
                    # not going to be saved, so we just use a placeholder.
                    self.image = pg.image.load(
                        image_bytes, "assets/placeholder.svg"
                    )
                    logging.info("Image generated!")
                    self.has_generated_image = True
                else:
                    user_input = self.text_input.get_cur_word()
                    if user_input == self.word:

                        # Add points to score
                        # Add success dialogue here

                        self.word = utils.FileUtils.get_random_word()
                        prompt = self.preprompt + self.word
                        image_bytes = stable_diffusion_client.run(
                            prompt=prompt,
                        )
                        self.image = pg.image.load(
                            image_bytes, "assets/placeholder.svg"
                        )

        self.progress_bar.update()
        self.text_input.update(events)
        self.button.update(mouse_buttons, mouse_pos)
        self.dialogue_sys.update(events)

    def draw(self):
        self.win.fill((0, 200, 200))

        self.text_input.draw(self.win)
        self.dialogue_sys.draw(self.win)
        self.score.draw(self.win)

        if self.playing:
            self.progress_bar.draw(self.win, self.win.get_width() // 2 - self.progress_bar.width // 2,
                                   self.win.get_height() - 50)

        self.win.blit(pg.transform.scale(
            self.image,
            tuple(stable_diffusion_client.image_dimensions)),
            (self.win.get_width()/2 - self.image.get_width()//2,
             self.win.get_height()/3 - self.image.get_height()//2),
        )

    def run(self):
        self.main_menu()
        self.load()

        while True:
            self.update()
            self.draw()
            pg.display.update()
            self.clock.tick(60)

    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
