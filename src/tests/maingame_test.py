import unittest
import pygame

from keys import Keys
from gamestate import GameState
from maingame import MainGame

class StubEventCheck:
    def __init__(self, gamestate, keys):
        self._gamestate = gamestate
        self._keys = keys

    def check(self):
        pass

class StubTitleScreen:
    def __init__(self, renderer, keys, gamestate, eventcheck):
        self._gamestate = gamestate
        self._renderer = renderer
        self._keys = keys
        self._eventcheck = eventcheck

    def display_menu(self):
        pass

    def move_cursor(self):
        pass

    def check_input(self):
        pass

class StubStaticMenu:
    def __init__(self, renderer, keys, gamestate, eventcheck):
        self._gamestate = gamestate
        self._renderer = renderer
        self._keys = keys
        self._eventcheck = eventcheck

    def display_menu(self):
        pass

class StubRenderer:
    def __init__(self):
        self.SCREEN_W = 512
        self.SCREEN_H = 448

    def draw_text(self):
        pass

    def draw_cursor(self):
        pass

    def blit_screen(self):
        pass

    def update(self):
        pass

    def fill(self):
        pass

class StubBattle:
    def __init__(self, gamestate, renderer, keys, eventcheck):
        self._gamestate = gamestate
        self._renderer = renderer
        self._keys = keys
        self._eventcheck = eventcheck

    def game_loop(self):
        pass

    def check_events(self):
        pass

KEYS = Keys()
GAMESTATE = GameState()
RENDERER = StubRenderer()
EVENTCHECK = StubEventCheck(GAMESTATE, KEYS)
BATTLE = StubBattle(GAMESTATE, RENDERER, KEYS, EVENTCHECK)
TITLESCREEN = StubTitleScreen(RENDERER, KEYS, GAMESTATE, EVENTCHECK)
MENU1 = StubStaticMenu(RENDERER, KEYS, GAMESTATE, EVENTCHECK)
MENU2 = StubStaticMenu(RENDERER, KEYS, GAMESTATE, EVENTCHECK)


class TestMainGame(unittest.TestCase):
    def setUp(self):
        self.game = MainGame(GAMESTATE, RENDERER, KEYS, EVENTCHECK, BATTLE, TITLESCREEN, MENU1, MENU2)
        self.game._test_val = True

    def test_game_is_initialised(self):
        self.assertIsNone(self.game.current)

    def test_new_game(self):
        self.game.new_game()
        self.assertTrue(self.game.running)

    def test_state_battle(self):
        self.game._gamestate.battle = True
        self.game.check_state()
        self.assertEqual(self.game.current, self.game._gamestate.battle)

    def test_state_title(self):
        self.game._gamestate.title = True
        self.game.check_state()
        self.assertEqual(self.game.current, self.game._gamestate.title)

    def test_state_menu1(self):
        self.game._gamestate.menu1 = True
        self.game.check_state()
        self.assertEqual(self.game.current, self.game._gamestate.menu1)

    def test_state_menu2(self):
        self.game._gamestate.menu2 = True
        self.game.check_state()
        self.assertEqual(self.game.current, self.game._gamestate.menu2)


    



