import pygame
from menu import Menu

class TitleScreen(Menu):
    def __init__(self, renderer, keys, gamestate, eventcheck):
        Menu.__init__(self, renderer, keys, gamestate, eventcheck)

        self.state = 'start'
        self.start_x, self.start_y = self.mid_w, self.mid_h + 40
        self.help_x, self.help_y = self.mid_w, self.mid_h + 60
        self.credits_x, self.credits_y = self.mid_w, self.mid_h + 80
        self.cursor.rect.midtop = (self.start_x + self.offset, self.start_y)

    def display_menu(self):
        while self._gamestate.title:
            self._eventcheck.check()
            self.check_input()
            self._renderer.fill()
            self._renderer.draw_text('untitled rpg: battle demo', 48, self.mid_w, self.mid_h - 40)
            self._renderer.draw_text('start', 32, self.start_x, self.start_y)
            self._renderer.draw_text('help', 32, self.help_x, self.help_y)
            self._renderer.draw_text('credits', 32, self.credits_x, self.credits_y)
            self._renderer.draw_cursor(self.cursor)
            self.blit()

    def move_cursor(self):
        if self._keys.DOWN_K:
            if self.state == 'start':
                self.cursor.rect.midtop = (self.help_x + self.offset, self.help_y)
                self.state = 'help'
            elif self.state == 'help':
                self.cursor.rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = 'credits'
            elif self.state == 'credits':
                self.cursor.rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = 'start'
        elif self._keys.UP_K:
            if self.state == 'start':
                self.cursor.rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = 'credits'
            elif self.state == 'help':
                self.cursor.rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = 'start'
            elif self.state == 'credits':
                self.cursor.rect.midtop = (self.help_x + self.offset, self.help_y)
                self.state = 'help'

    def check_input(self):
        self.move_cursor()
        if self._keys.START_K:
            if self.state == 'start':
                self._gamestate.battle = True
            elif self.state == 'help':
                self._gamestate.menu1 = True
            elif self.state == 'credits':
                self._gamestate.menu2 = True
            self._gamestate.title = False