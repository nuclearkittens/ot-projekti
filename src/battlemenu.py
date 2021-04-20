import pygame
from menu import Menu
from constants import *

class BattleMenu(Menu):
    def __init__(self, renderer, keys, gamestate, eventcheck, offset, w, h):
        Menu.__init__(self, renderer, keys, gamestate, eventcheck, 10)

        self.state = 'attack'
        self.attack_x, self.attack_y = 30, self.mid_h + 100
        self.skill_x, self.skill_y = 30, self.mid_h + 120
        self.item_x, self.item_y = 30, self.mid_h + 140

        self.cursor.rect.midtop = (self.attack_x + offset, self.attack_y)
        self.bg = load_img('battlebg1', 'background')
        self.bg_rect = self.bg.get_rect()

    def display_menu(self):
            self._eventcheck.check()
            self.check_input()
            self.draw_bg()
            self._renderer.draw_rect(0, 330, SCREEN_W, SCREEN_H - 330)
            self._renderer.draw_text('attack', 32, self.attack_x, self.attack_y)
            self._renderer.draw_text('skills', 32, self.skill_x, self.skill_y)
            self._renderer.draw_text('items', 32, self.item_x, self.item_y)
            self._renderer.draw_cursor(self.cursor)

    def move_cursor(self):
        if self._keys.DOWN_K:
            if self.state == 'attack':
                self.cursor.rect.midtop = (self.skills_x + self.offset, self.skills_y)
                self.state = 'skills'
            elif self.state == 'skills':
                self.cursor.rect.midtop = (self.items_x + self.offset, self.items_y)
                self.state = 'items'
            elif self.state == 'items':
                self.cursor.rect.midtop = (self.attack_x + self.offset, self.attack_y)
                self.state = 'attack'
        elif self._keys.UP_K:
            if self.state == 'attack':
                self.cursor.rect.midtop = (self.items_x + self.offset, self.items_y)
                self.state = 'items'
            elif self.state == 'skills':
                self.cursor.rect.midtop = (self.attack_x + self.offset, self.attack_y)
                self.state = 'attack'
            elif self.state == 'items':
                self.cursor.rect.midtop = (self.skills_x + self.offset, self.skills_y)
                self.state = 'skills'

    def check_input(self):
        self.move_cursor()
        if self._keys.SELECT_K:
            return str(self.state)

    def draw_bg(self):
        self._renderer.draw_img(self.bg)

