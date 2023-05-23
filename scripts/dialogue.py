
import pygame as pg
from .entities import Entity
import textwrap

HARD_CONSONANTS = ['q', 't', 'p', 'd', 'g', 'j', 'k', 'x', 'c', 'b']
SOFT_CONSONANTS = ['w', 'r', 'y', 's', 'f', 'h', 'l', 'z', 'v', 'n', 'm']

class DialogueSystem:
    def __init__(self,spacing=15, text_size=32) -> None:
        self.font = pg.font.Font('font/Cascadia.ttf', text_size)
        self.host_icon = Entity((0,0),["assets/robo_idle","assets/robo_talking"], 0.2, "robo_idle")
        self.dialogue_border = pg.image.load("assets/dialogue_border.png")
        self.dialogue_border = pg.transform.scale_by(self.dialogue_border, 0.2)
        self.talking = False
        self.text = ""
        self.visible = True
        self.spacing = spacing
        self.frame_count = 0
        self.frame_skip = 0
        self.font_surf = None
        self.key_surf = pg.image.load("assets/X_Key_Dark.png")
        self.key_sound = pg.mixer.Sound("assets/chungu.wav") 

    def reset(self):
        self.talking = False
        self.text = ""
        self.frame_count = 0
        self.frame_skip = 0
        self.font_surf = None

    def start_talking(self, text, frame_skip : int ):
        self.talking = True
        self.text = text
        self.frame_count = frame_skip*len(text)
        self.frame_skip = frame_skip

    def update(self, events):
        if self.visible:
            self.host_icon.update(events)

            if self.frame_count > 0:
                cur_letter_idx = int((self.frame_skip*len(self.text)-self.frame_count)/self.frame_skip)
                self.frame_count -= 1
                if self.frame_count % self.frame_skip == 0:
                    self.font_surf = self.render_text(self.text[:cur_letter_idx+1], self.font, 1000)
                    
                    if self.text[cur_letter_idx] in HARD_CONSONANTS:
                        pg.mixer.music.set_volume(0.05)
                    if self.text[cur_letter_idx] in SOFT_CONSONANTS:
                        pg.mixer.music.set_volume(0.03)
                        
                    self.key_sound.play()

            else:
                self.talking = False
            if self.talking:
                self.host_icon.anim.set_state("robo_talking")
            else:
                self.host_icon.anim.set_state("robo_idle")


    def wrap_text(self, text, font, width):
        """Wrap text to fit inside a given width when rendered.

        :param text: The text to be wrapped.
        :param font: The font the text will be rendered in.
        :param width: The width to wrap to.

        """
        text_lines = text.replace('\t', '    ').split('\n')
        if width is None or width == 0:
            return text_lines

        wrapped_lines = []
        for line in text_lines:
            line = line.rstrip() + ' '
            if line == ' ':
                wrapped_lines.append(line)
                continue

            # Get the leftmost space ignoring leading whitespace
            start = len(line) - len(line.lstrip())
            start = line.index(' ', start)
            while start + 1 < len(line):
                # Get the next potential splitting point
                next = line.index(' ', start + 1)
                if font.size(line[:next])[0] <= width:
                    start = next
                else:
                    wrapped_lines.append(line[:start])
                    line = line[start+1:]
                    start = line.index(' ')
            line = line[:-1]
            if line:
                wrapped_lines.append(line)
        return wrapped_lines


    def render_text_list(self,lines, font, colour=(255, 255, 255)):
        """Draw multiline text to a single surface with a transparent background.

        Draw multiple lines of text in the given font onto a single surface
        with no background colour, and return the result.

        :param lines: The lines of text to render.
        :param font: The font to render in.
        :param colour: The colour to render the font in, default is white.

        """
        rendered = [font.render(line, True, colour).convert_alpha()
                    for line in lines]

        line_height = font.get_linesize()
        width = max(line.get_width() for line in rendered)
        tops = [int(round(i * line_height)) for i in range(len(rendered))]
        height = tops[-1] + font.get_height()

        surface = pg.Surface((width, height)).convert_alpha()
        surface.fill((0, 0, 0, 0))
        for y, line in zip(tops, rendered):
            surface.blit(line, (0, y))

        return surface
    
    def render_text(self,text, font,  width):
        lines = self.wrap_text(text, font, width)
        return self.render_text_list(lines,font)

    def draw(self, win : pg.Surface):
        if self.visible:
            pos_border = (self.spacing, win.get_height() - self.spacing - self.dialogue_border.get_height())
            pos_icon = (pos_border[0] + self.dialogue_border.get_height()//2 - self.host_icon.get_width()//2, pos_border[1] +self.dialogue_border.get_height()//2 - self.host_icon.get_height()//2)
            # print(win.get_height(),self.host_icon.get_height(),self.spacing, pos)
            self.host_icon.pos = pos_icon
            win.blit(self.dialogue_border, pos_border)
            self.host_icon.draw(win)
            if self.font_surf:
                win.blit(self.font_surf, (pos_border[0] + self.dialogue_border.get_width(), pos_border[1] + self.dialogue_border.get_height()//6))
            if not self.talking:
                win.blit(self.key_surf, (win.get_width() - self.spacing - self.key_surf.get_width(), win.get_height() - self.spacing - self.key_surf.get_height()))

