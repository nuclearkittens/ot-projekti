import pygame
from cursor import Cursor
from constants import *

class Menu:
    def __init__(self, renderer, keys, gamestate, eventcheck, offset=-100):
        self._renderer = renderer
        self._keys = keys
        self._gamestate = gamestate
        self._eventcheck = eventcheck
        self.mid_w = SCREEN_W // 2
        self.mid_h = SCREEN_H // 2
        self.offset = offset

        self.cursor = Cursor('>')


    def blit(self):
        self._renderer.blit_screen()
        self._renderer.update()
        self._keys.reset_keys()

