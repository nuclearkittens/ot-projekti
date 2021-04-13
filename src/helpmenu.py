import pygame
from menu import Menu

class HelpMenu(Menu):
    def __init__(self, renderer, keys, gamestate, eventcheck):
        Menu.__init__(self, renderer, keys, gamestate, eventcheck)

    def display_menu(self):
        while self._gamestate.menu1:
            self._eventcheck.check()
            if self._keys.START_K or self._keys.BACK_K:
                self._gamestate.title = True
                self._gamestate.menu1 = False
            self._renderer.fill()
            self._renderer.draw_text('help stuffz be here', 32, self.mid_w, self.mid_h - 20)
            self._renderer.draw_text('controls and such', 16, self.mid_w, self.mid_h + 10)
            self.blit()