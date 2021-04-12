import pygame
from menu import Menu

class HelpMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_K or self.game.BACK_K:
                self.game.curr_menu = self.game.titlescreen
                self.run_display = False
            self.game.display.fill(self.game.DARK_PURPLE)
            self.game._renderer.draw_text('help stuffz be here', 32, self.mid_w, self.mid_h - 20)
            self.game._renderer.draw_text('controls and such', 16, self.mid_w, self.mid_h + 10)
            self.blit_screen()