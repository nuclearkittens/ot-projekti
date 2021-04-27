import pygame as pg
from config import FONT, FONT_SIZE, CURSOR, DARK_ROSE, POWDER_ROSE

class Button(pg.sprite.Sprite):
    def __init__(self, text, text_size, text_colour):
        pg.sprite.Sprite.__init__(self)
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

class BattleMenuButton(Button):
    def __init__(self, text):
        self._name = text
        self._text_size = FONT_SIZE
        Button.__init__(self, text, self._text_size, POWDER_ROSE)
        
        self.active = False
        self.pressed = False

        self._passive_img = self.image
        self._active_img = self._create_button(text, self._text_size, DARK_ROSE)
        self._frames = [self._passive_img, self._active_img]

    def set_position(self, x, y):
        self.rect.topleft = (x, y)

    def update(self):
        if self.active or self.pressed:
            self.image = self._frames[1]
        else:
            self.image = self._frames[0]

    @property
    def action(self):
        return self._name

class ActionButton(BattleMenuButton):
    def __init__(self, name, cost):
        self._name = name
        self._text = f'{name}{cost:2}'

        BattleMenuButton.__init__(self, self._text)

class ItemButton(BattleMenuButton):
    def __init__(self, name, qty):
        self._name = name
        self._qty = qty
        self._text = self._update_text()
        
        BattleMenuButton.__init__(self, self._text)

    def _update_text(self):
        return f'{self._name}{self._qty:2}'

    def update(self):
        # figure out how to handle target selection/not actually using item
        if self.pressed or self.active:
            if self.pressed and self._qty > 0:
                self._text = self._update_text()
                self._passive_img = self._create_button(self._text, self._text_size, POWDER_ROSE)
                self._active_img = self._create_button(self._text, self._text_size, DARK_ROSE)
            self.image = self._frames[1]
        else:
            self.image = self._frames[0]


