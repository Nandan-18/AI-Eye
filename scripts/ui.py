import pygame as pg
import random

class UI_Container:
    def __init__(self, pos : tuple = (0,0), size : tuple = (0,0), surf : pg = None, visible=True) -> None:
        self.pos = pos
        self.size = size
        self.surf = surf
        self.visible = visible
        self.hover = False
        # its a datatype with pos and size together and used for collision detection
        self.rect = pg.Rect(*self.pos, *self.size)

        # if clicked pos will be assigned if left mouse button pressed 
        self.clicked : tuple = None 
    
    #NOTE: look at pygame docs for get_pressed for mouse button under pygame.mouse
    def update(self, mouse_buttons : tuple , mouse_pos : tuple):
        
        # update rect
        self.rect.x, self.rect.y = self.pos
        
        # update clicked 
        if mouse_buttons[0]:
            self.clicked = mouse_pos
        else:
            self.clicked = None

        if self.rect.collidepoint(mouse_pos):
            self.hover = True


class TextInput:
    def __init__(self, pos : tuple,  word_ans : str, visible : bool = False, box_size : int = 50, spacing : int = 10, ) -> None:
        self.pos = pos
        self.word_ans = word_ans
        self.length = len(word_ans)
        self.box_size = box_size
        self.spacing = spacing
        self.shake = 0


        # current guess
        self.boxes = [LetterBox(pos, i, box_size, spacing) for i in range(self.length)]

        self.cursor = 0

    def get_cur_word(self):
        return "".join([box.letter for box in self.boxes])

    # call only on key down press
    def update(self, event : pg.event.Event):
            if self.shake > 0:
                self.shake -= 1

            if event.type == pg.KEYDOWN and event.unicode.isalpha() and self.cursor != self.length:
                self.boxes[self.cursor].update(event.unicode, True)
                if self.cursor:
                    self.boxes[self.cursor-1].active = False
                self.cursor += 1
            elif event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE and self.cursor != 0:
                self.cursor -= 1 
                self.boxes[self.cursor].delete_char()
                if self.cursor != 0:
                    self.boxes[self.cursor-1].active = True
            
            if self.get_cur_word() != self.word_ans and self.cursor == self.length:
                self.shake = 30

    def draw(self, win : pg.Surface):
        for box in self.boxes:
            box.draw(win)

class LetterBox:
    def __init__(self, start_pos : tuple, letter_no : int, size : int, spacing : int, letter : str = "", active : bool = False) -> None:
        self.pos =  (start_pos[0] + (size+spacing)*letter_no, start_pos[1]) 
        self.letter = letter
        self.active = active
        self.size = size
        self.font = pg.font.Font('font/Anonymous.ttf', 32)

    def shake(self, shake_amt):
        pass

    def delete_char(self):
        self.letter = ""
        self.active = False

    def update(self, letter, active):
        self.letter = letter
        self.active = active


    def draw(self, win : pg.Surface):
        rect = pg.Rect(*self.pos, self.size, self.size)
        if self.letter == "":
            color = pg.color.Color(255,0,0)
        else:
            color = pg.color.Color(0,255,0)
        
        if self.active:
            color = pg.color.Color(255,255,0)
            
        pg.draw.rect(win, color, rect, border_radius=5)
        if self.letter != "":
            text = self.font.render(self.letter.capitalize(),True, pg.color.Color(255,255,255))
            text_pos = (self.pos[0] + (self.size-text.get_width())/2, self.pos[1]  + (self.size-text.get_height())/2)
            win.blit(text, text_pos)
        

# class Button(UI_Container):
    # def __init__(self, pos: tuple = (0, 0), size: tuple = (0, 0), surf: tuple = None, visible=True) -> None:
    #     super().__init__(pos, size, surf, visible)
    #     self.size = (50,100)
    #     self.surf = pg.surface.Surface(size)
    #     self.surf.fill(pg.Color(255,0,0))

    # def update(self, mouse_buttons: tuple, mouse_pos: tuple):
    #     super().update(mouse_buttons, mouse_pos)


    