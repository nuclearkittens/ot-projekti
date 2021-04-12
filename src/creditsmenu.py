import pygame
from menu import Menu

class CreditsMenu(Menu):
    # def __init__(self, game):
    #     Menu.__init__(self, game)

    # def display_menu(self):
    #     self.run_display = True
    #     while self.run_display:
    #         self.game.check_events()
    #         if self.game.START_K or self.game.BACK_K:
    #             self.game.current = self.game.titlescreen
    #             self.run_display = False
    #         self.game.display.fill(self.game.DARK_PURPLE)
    #         self.game._renderer.draw_text('credits', 32, self.mid_w, self.mid_h - 20)
    #         self.game._renderer.draw_text('list all them tutorials etc', 16, self.mid_w, self.mid_h + 10)
    #         self.blit_screen()

    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        # self.run_menu = True
        while self.run_menu:
            self._game.check_events()
            if self._game.START_K or self._game.BACK_K:
                self._game.current = self._game._titlescreen
                self.run_menu = False
            self._renderer.fill()
            self._renderer.draw_text('credits', 32, self.mid_w, self.mid_h - 20)
            self._renderer.draw_text('list all them tutorials etc', 16, self.mid_w, self.mid_h + 10)
            self.blit()