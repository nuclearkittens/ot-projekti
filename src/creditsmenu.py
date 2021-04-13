import pygame
from menu import Menu

class CreditsMenu(Menu):

    def __init__(self, renderer, keys, gamestate, eventcheck):
        Menu.__init__(self, renderer, keys, gamestate, eventcheck)

    def display_menu(self):
        while self._gamestate.menu2:
            self._eventcheck.check()
            if self._keys.START_K or self._keys.BACK_K:
                self._gamestate.title = True
                self._gamestate.menu2 = False
            self._renderer.fill()
            self._renderer.draw_text('credits', 32, self.mid_w, self.mid_h - 20)
            self._renderer.draw_text('credit where credit is due', 16, self.mid_w, self.mid_h + 10)
            self.blit()