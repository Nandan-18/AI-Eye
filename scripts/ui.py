import pygame as pg
import random

class UI_Container:
    def __init__(self, pos : tuple = (0,0), size : tuple = (0,0), surfs = None, visible=True) -> None:
        self.pos = pos
        self.size = size
        self.surfs = surfs
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
        if self.rect.collidepoint(mouse_pos):
            self.hover = True
            if mouse_buttons[0]:
                self.clicked = mouse_pos
            else:
                self.clicked = None
        else:
            self.hover = False



class Button(UI_Container):
    def __init__(self, pos: tuple = (0, 0), size: tuple = (0, 0), text="",img=None, surfs: tuple = None, visible=True, text_size=16, text_color= pg.color.Color(255,255,255), box_color= pg.Color(100, 0, 32), hover_color = pg.Color(60, 0, 32), clicked_color = pg.Color(200, 0, 32)) -> None:
        super().__init__(pos, size, surfs, visible)
        self.size = size
        self.surf = pg.surface.Surface(size)
        self.surf.fill(pg.Color(255,0,0))
        self.visible = visible
        self.font = pg.font.Font('font/Cascadia.ttf', 32)
        self.text= text
        self.hover_color = hover_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.box_color = box_color
        self.clicked_color = clicked_color
        self.img = img


    def update(self, mouse_buttons: tuple, mouse_pos: tuple):
        super().update(mouse_buttons, mouse_pos)
    
    def draw(self, win : pg.Surface):
        if self.visible:
            color = None
            if self.hover:
                color = self.hover_color
            else:
                color = self.box_color
            if self.clicked:
                color = self.clicked_color
            if self.img:
                win.blit(self.img, self.pos)
            else:
                pg.draw.rect(win, color, self.rect)
            if self.text:
                text_surf = self.font.render(self.text, True, self.text_color)
                text_pos =(self.pos[0] + (self.size[0]-text_surf.get_width())/2, self.pos[1]+ (self.size[1]-text_surf.get_height())/2)
                win.blit(text_surf, text_pos)


class TextInput:
    def __init__(self, height : int,  word_ans : str, win_size, visible : bool = False, box_size : int = 50, spacing : int = 10, ) -> None:
        self.height = height
        self.box_size = box_size
        self.spacing = spacing
        self.visible = visible
        self.win_size = win_size



        self.reset_input(word_ans)

    def is_completed(self):
        return self.length == len(self.get_cur_word())

    def get_cur_word(self):
        return "".join([box.letter for box in self.boxes])

    def is_correct_answer(self):
        return self.get_cur_word() == self.word_ans
    
    def reset_input(self, new_word_ans : str):
        self.word_ans = new_word_ans
        self.length = len(self.word_ans)
        self.pos = (self.win_size[0]//2 - (self.spacing+self.box_size)*self.length/2, self.height)
        self.shake = 0
        self.frame_count = 0
        # current guess
        self.boxes = [LetterBox(self.pos, i, self.box_size, self.spacing) for i in range(self.length)]

        self.cursor = 0


    def update(self, events : list):
            if self.visible:
                if self.shake > 0:
                    self.shake -= 1
                    for box in self.boxes:
                        box.shake = True  
                else:
                    for box in self.boxes:
                        box.shake = False

                for event in events:
                    if event.type == pg.KEYDOWN and event.unicode.isalpha() and self.cursor != self.length:
                        isactive = self.cursor+1 != self.length 
                        self.boxes[self.cursor].update_key(event.unicode, isactive)
                        if self.cursor:
                            self.boxes[self.cursor-1].active = False
                        self.cursor += 1
                        if self.get_cur_word() != self.word_ans and self.cursor == self.length:
                            self.shake = 30
                    elif event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE and self.cursor != 0:
                        self.cursor -= 1 
                        self.boxes[self.cursor].delete_char()
                        if self.cursor != 0:
                            self.boxes[self.cursor-1].active = True

            

    def draw(self, win : pg.Surface):
        # print(self.shake)
        if self.visible:
            for box in self.boxes:
                box.draw(win)

class LetterBox:
    def __init__(self, start_pos : tuple, letter_no : int, size : int, spacing : int, letter : str = "", active : bool = False) -> None:
        self.pos =  (start_pos[0] + (size+spacing)*letter_no, start_pos[1]) 
        self.letter = letter
        self.active = active
        self.size = size
        self.font = pg.font.Font('font/Cascadia.ttf', 32)
        self.offset = (0, 0)
        self.shake = False

    def delete_char(self):
        self.letter = ""
        self.active = False

    def update_key(self, letter, active):
        self.letter = letter
        self.active = active


    def draw(self, win : pg.Surface):
        self.offset = (0, 0)
        if self.shake:
            self.offset = (random.randint(0,8), random.randint(0,8))

        # shakepos = self.pos
        shakepos = (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1])
        rect = pg.Rect(*shakepos, self.size, self.size)
        if self.letter == "":
            color = pg.color.Color(128,0,32)
        else:
            color = pg.color.Color(157, 193, 131)
        
        if self.active:
            color = pg.color.Color(200, 157, 71)
            
        pg.draw.rect(win, color, rect, border_radius=5)
        if self.letter != "":
            text = self.font.render(self.letter.capitalize(),True, pg.color.Color(255,255,255))
            text_pos = (self.pos[0] + (self.size-text.get_width())/2 + self.offset[0] , self.pos[1]  + (self.size-text.get_height())/2 + self.offset[1])

            text_pos += (text_pos[0]+self.offset[0], text_pos[1]+self.offset[1])
            win.blit(text, text_pos)
        



    
