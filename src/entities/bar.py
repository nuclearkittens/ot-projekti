import pygame as pg

from config import (
    HP_GREEN, HP_YELLOW, HP_RED, MP_BLUE, DARK_PURPLE,
    POWDER_ROSE, FONT, FONT_SIZE, SCREEN_W, SCREEN_H)

class Bar:
    '''General class for rectangular bars.

    attr:
        base: a Pygame surface, works as the base of the bar
        top: a Pygame surface
        rect: a Pygame object for storing coordinates
    '''
    def __init__(self, w, h):
        '''Class constructor.

        args:
            w: int; width of the bar
            h: int; height of the bar
        '''
        self._w = w
        self._h = h

        self._base = pg.Surface((self._w, self._h))
        self._top = pg.Surface((self._w, self._h))
        self.rect = self._base.get_rect()

    def draw(self, renderer):
        '''Blits the bar on the display.

        args:
            renderer: Renderer object
        '''
        renderer.blit(self._base, self.rect)
        renderer.blit(self._top, self.rect)

class HPBar(Bar):
    '''Class for drawing health bars in a battle screen.'''
    def __init__(self, w, h, character):
        '''Class constructor for HP bars.

        args:
            character: Character object; specifies the character associated with the bar
            colour: colour tuple; colour of the bar
        '''
        Bar.__init__(self, w, h)
        self.character = character
        self._colour = HP_GREEN

    def update(self):
        '''Updates the bar based on current HP and draws a new
        rectangle on the base surface.'''
        self._base.fill(DARK_PURPLE)
        ratio = self.character.curr_hp / self.character.max_hp
        if ratio > 0.5:
            self._colour = HP_GREEN
        elif ratio < 0.2:
            self._colour = HP_RED
        else:
            self._colour = HP_YELLOW
        new_w = int(ratio * self._w)
        if new_w < 0:
            new_w = 0
        self._top = pg.Surface((new_w, self._h))
        self._top.fill(self._colour)

class MPBar(Bar):
    '''Class for drawing party members' MP bars in battle.'''
    def __init__(self, w, h, character):
        '''Class constructor for MP bars.

        args:
            character: Character object; specifies the character associated with the bar
            colour: colour tuple; colour of the bar
        '''
        Bar.__init__(self, w, h)
        self.character = character
        self._colour = MP_BLUE

    def update(self):
        '''Updates the bar based on current MP and draws a new
        rectangle on the base surface.'''
        self._base.fill(DARK_PURPLE)
        ratio = self.character.curr_mp / self.character.max_mp
        new_w = int(ratio * self._w)
        self._top = pg.Surface((new_w, self._h))
        self._top.fill(self._colour)

class InfoBar(Bar):
    '''Class for displaying an info bar in battle.'''
    def __init__(self):
        margin = SCREEN_W // 64
        w = SCREEN_W - (2 * margin)
        h = SCREEN_H // 16
        Bar.__init__(self, w, h)

        self.rect.topleft = (margin, margin)
        self.update(' ')

    def update(self, text):
        '''Updates the info shown on info panel.

        args:
            text: str; info to be displayed
        '''
        self._base.fill(POWDER_ROSE)
        font = pg.font.Font(FONT, FONT_SIZE)
        self._top = font.render(text, False, DARK_PURPLE)
        if self._top.get_width() > self._w:
            self._top = pg.transform.scale(self._top, (self._w, self._h))
