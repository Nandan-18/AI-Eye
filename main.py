# main functionality

import pygame as pg
import sys
import os
from scripts import entities, dialogue, ui, progress_bar, scoring, controller
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

        self.bg_img = pg.image.load("assets/screen.png")

        pg.display.set_caption("Game")

        self.playing = False

        self.click = pg.mixer.Sound("sounds/Click.mp3")
        self.wrong_answer = pg.mixer.Sound("sounds/WrongAnswerShake.mp3")
        pg.mixer.music.set_volume(0.5)

        self.score = None
        self.progress_bar = None

    def main_menu(self):
        bg_img = pg.image.load("assets/Title_screen.png")
        bg_img = pg.transform.scale(bg_img, self.win.get_size())
        start_button = ui.Button(
            (self.win.get_width()//2-200, self.win.get_height()*3//5), (400, 50), "Start")
        mute_button = ui.Button(
            (self.win.get_width()//2-50, self.win.get_height()*4//5),  (100, 50), "Mute")
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
            self.win.blit(bg_img, (0,0))
            start_button.draw(self.win)
            mute_button.draw(self.win)

    def load(self):
        self.game_conroller = controller.GameController(self.win.get_size())
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

            if event.type == pg.VIDEORESIZE:
                self.win = pg.display.set_mode(
                    (event.w, event.h), pg.RESIZABLE)


        self.game_conroller.update(events)

    def draw(self):
        self.win.blit(self.bg_img, (0,0))

        self.game_conroller.draw(self.win)

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
