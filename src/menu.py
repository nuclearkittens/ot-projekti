import pygame
from cursor import Cursor

class Menu:
    def __init__(self, game, w=512, h=448, offset=-100):
        self._game = game
        self._renderer = self._game._renderer
        self.mid_w = w // 2
        self.mid_h = h // 2
        self.offset = offset

        self.cursor = Cursor('>')

        self.run_menu = True

    def blit(self):
        self._renderer.blit_screen()
        self._renderer.update()
        self._game.reset_keys()

