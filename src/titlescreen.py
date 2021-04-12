import pygame
from menu import Menu

class TitleScreen(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'start'
        self.start_x, self.start_y = self.mid_w, self.mid_h + 30
        self.help_x, self.help_y = self.mid_w, self.mid_h + 50
        self.credits_x, self.credits_y = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.DARK_PURPLE)
            self.game._renderer.draw_text('untitled rpg: battle demo', 48, self.mid_w, self.mid_h - 20)
            self.game._renderer.draw_text('start', 32, self.start_x, self.start_y)
            self.game._renderer.draw_text('help', 32, self.help_x, self.help_y)
            self.game._renderer.draw_text('credits', 32, self.credits_x, self.credits_y)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_K:
            if self.state == 'start':
                self.cursor_rect.midtop = (self.help_x + self.offset, self.help_y)
                self.state = 'help'
            elif self.state == 'help':
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = 'credits'
            elif self.state == 'credits':
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = 'start'
        elif self.game.UP_K:
            if self.state == 'start':
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = 'credits'
            elif self.state == 'help':
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = 'start'
            elif self.state == 'credits':
                self.cursor_rect.midtop = (self.help_x + self.offset, self.help_y)
                self.state = 'help'

    def check_input(self):
        self.move_cursor()
        if self.game.START_K:
            if self.state == 'start':
                self.game.battle = True
            elif self.state == 'help':
                self.game.curr_menu = self.game.help
            elif self.state == 'credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False