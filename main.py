#main function
import pygame as pg
import sys
import logging
from scripts import ui

class Game:
    def __init__(self) -> None:
        pg.mixer.pre_init(16000, -16, 2, 2048)
        pg.init()
        self.win = pg.display.set_mode(size=(1000,500))
        self.clock = pg.time.Clock()

        self.fps = 60

        pg.display.set_caption("Game")

        self.playing = False

        self.click = pg.mixer.Sound("sounds/Click.mp3")
        self.wrong_answer = pg.mixer.Sound("sounds/WrongAnswerShake.mp3")
        self.right_answer = pg.mixer.Sound("sounds/GoodAnswerDing.mp3")


    def load(self):
        
            self.mute_button = ui.Button((800, 10), (100, 50),"Mute")

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
        self.mute_button.update(mouse_buttons, mouse_pos)

        if self.text_input.shake == 30:
            self.wrong_answer.play()

        if self.text_input.get_cur_word() == self.text_input.word_ans and self.text_input.cursor == self.text_input.length:
            self.right_answer.play()
        
        #load main game
        if self.button.clicked and self.playing == False:
            self.click.play()
            self.playing = True
            self.load()

        #mute audio
        if self.mute_button.clicked:
            pg.mixer.music.stop()
        
    
    def draw(self):
        self.win.fill((0,0,0))
        self.text_input.draw(self.win)
        self.button.draw(self.win)
        self.mute_button.draw(self.win)

    def draw_start_screen(self):
        self.win.fill((250,248,246))
        self.button.draw(self.win)
        self.mute_button.draw(self.win)

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
