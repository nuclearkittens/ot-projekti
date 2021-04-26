import pygame as pg
from config import FONT, CURSOR

class Button(pg.sprite.Sprite):
    def __init__(self, text, text_size, text_colour):
        pg.sprite.Sprite.__init__(self)
        self.name = None
        self.image = self._create_button(text, text_size, text_colour)
        self.rect = self.image.get_rect()

    def set_position(self, x, y):
        self.rect.midleft = (x, y)

    def _create_button(self, text, size, colour):
        font = pg.font.Font(FONT, size)
        return font.render(text, False, colour)

class Cursor(Button):
    def __init__(self, size, colour):
        Button.__init__(self, CURSOR, size, colour)

class MenuButton(Button):
    def __init__(self, name, text, text_size, text_colour):
        Button.__init__(self, text, text_size, text_colour)
        self.name = name
        self.text = text
        self.text_size = text_size
        self.text_colour = text_colour

        self.pressed = False
        self.frames = []

    def add_frame(self, text):
        img = self._create_button(text, self.text_size, self.text_colour)
        self.frames.append(img)

    def update(self):
        if self.pressed and len(self.frames) > 0:
            self.image = self.frames.pop()
