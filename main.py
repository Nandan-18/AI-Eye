# main function
import pygame as pg
import sys
import logging
import os
from scripts import entities, dialogue, ui, progress_bar, scoring
from clients import stable_diffusion
from clients import utils
from loguru import logger


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

    def main_menu(self):
        start_button = ui.Button((self.win.get_width()//2-200, self.win.get_height()//2-25), (400, 50), "Start")
        mute_button = ui.Button((self.win.get_width()//2-50, self.win.get_height()//40),  (100, 50), "Mute")
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
        self.image = pg.surface.Surface((512, 512))
        self.word = utils.FileUtils.get_random_word()
        self.has_generated_image = False

        pg.mixer.music.load('sounds/Suspense.mp3')
        pg.mixer.music.play(-1)
        
        if  self.playing == False:
            self.text_input = ui.TextInput((100,100), "AI Game Jam Game")
            self.button = ui.Button((275,200), (400, 50),"Start")

            pg.mixer.music.load('sounds/JeopardyTypeBeat.mp3')
            pg.mixer.music.play(-1)
            
        if self.playing == True:
            self.word = utils.FileUtils.get_random_word()
            self.text_input = ui.TextInput((100,100), self.word, True)
            self.button = ui.Button((10,10), (100, 50),"hey")
            self.image = pg.surface.Surface((512,512))

            pg.mixer.music.load('sounds/Suspense.mp3')
            pg.mixer.music.play(-1)

        self.has_generated_image = False
        self.dialogue_sys = dialogue.DialogueSystem()

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
                    logger.debug("Checking for new text...")
                    preprompt = "Isometic art of "
                    prompt = preprompt + self.word

                    logger.debug("Generating image...")
                    image_bytes = stable_diffusion_client.run(
                        prompt=prompt,
                    )
                    logger.debug("Image generated!")

                    # Pygame needs a name for the image file even if it's 
                    # not going to be saved, so we just use a placeholder.
                    self.image = pg.image.load(
                        image_bytes, "assets/placeholder.svg"
                    )
                    logger.debug("Image loaded!")
                    self.has_generated_image = True
                else:
                    if self.text_input.word_ans == self.word:
                        # update the score
                        # clear the text input
                        self.text_input.word_ans = ""
                        # get a new random word
                        self.word = utils.FileUtils.get_random_word()
                        pass
                    else:
                        self.wrong_answer.play()
                        # shake the screen?

        self.text_input.update(events)
        self.button.update(mouse_buttons, mouse_pos)
        self.dialogue_sys.update(events)

    def draw(self):
        self.win.fill((0, 200, 200))
        self.text_input.draw(self.win)
        self.dialogue_sys.draw(self.win)

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
