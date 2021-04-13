import pygame
import unittest
from game import Game

class StubCursor:
    def __init__(self, char='>', h=32, w=32):
        self.cursor = char
        self.rect = pygame.Rect(0,0,w,h)

class StubRenderer:
    def __init__(self):
        self.SCREEN_W = 512
        self.SCREEN_H = 448
        self.screen = pygame.Surface((self.SCREEN_W,self.SCREEN_H))
        self.display = pygame.display.set_mode(((self.SCREEN_W,self.SCREEN_H)))

    def draw_text(self, text='', size=16, x=0, y=0, colour=(0,0,0)):
        pass
    
    def draw_cursor(self, cursor='>', size=16):
        pass

    def blit_screen(self):
        pass

    def update(self):
        pass

    def fill(self, colour=(0,0,0)):
        pass

class StubMenu:
    def __init__(self, game, w, h, offset):
        self._game = game
        self._renderer = self._game._renderer
        self.mid_w = w // 2
        self.mid_h = h // 2
        self.offset = offset
        self.cursor = StubCursor()
        self.run_menu = True

    def blit(self):
        pass

class StubTitleScreen(StubMenu):
    def __init__(self, game):
        StubMenu.__init__(self, game)

    def display_menu(self):
        pass

    def move_cursor(self):
        pass

    def check_input(self):
        pass

class StubStaticMenu(StubMenu):
    def __init__(self, game):
        StubMenu.__init__(self, game)

    def display_menu(self):
        pass

class StubKeys:
    def __init__:
        self.UP_K, self.DOWN_K = False, False
        self.RIGHT_K, self.LEFT_K = False, False
        self.SELECT_K, self.START_K = False, False
        self.BACK_K, self.PAUSE_K = False, False

    def reset_keys(self):
        pass


SCREEN_W = 512
SCREEN_H = 448

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
