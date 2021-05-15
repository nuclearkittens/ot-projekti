from collections import deque

import unittest
import pygame as pg

from combat.battle import Battle
from database.initialise_db import initialise_db
from ui.renderer import Renderer
from config import NATIVE_RESOLUTION
from prepare import create_demo_party
from keys import Keys

class StubEventHandler:
    def __init__(self):
        self.keys = Keys()
        self.queue = deque()

    def set_event_queue(self, event_queue):
        for event in event_queue:
            self.queue.append(event)

    def check_input(self):
        try:
            event = self.queue.popleft()
        except IndexError:
            event = ('keydown', 'select')

        if event[0] == 'quit':
            self.keys.QUIT = True
        elif event[0] == 'keydown':
            if event[1] == 'select':
                self.keys.SELECT = True
            if event[1] == 'start':
                self.keys.START = True
            if event[1] == 'back':
                self.keys.BACK = True
            if event[1] == 'pause':
                self.keys.PAUSE = True
            if event[1] == 'up':
                self.keys.UP = True
            if event[1] == 'down':
                self.keys.DOWN = True
            if event[1] == 'left':
                self.keys.LEFT = True
            if event[1] == 'right':
                self.keys.RIGHT = True

class StubClock:
    def __init__(self):
        self.ticks = 0

    def tick(self, FPS):
        self.ticks += 1

def init_test_battle():
    screen = pg.display.set_mode(NATIVE_RESOLUTION, pg.HIDDEN)
    renderer = Renderer(screen)
    party = create_demo_party()
    events = StubEventHandler()
    clock = StubClock()
    return Battle(clock, renderer, events, party)

class TestBattleLoops(unittest.TestCase):
    def setUp(self):
        initialise_db()
        pg.init()
        self.battle = init_test_battle()
        self.curr = self.battle._gfx.party.sprites()[0]

    def tearDown(self):
        pg.quit()

    def test_pause_loop(self):
        q = [('keydown', 'pause')]
        self.battle._eventhandler.set_event_queue(q)
        self.battle._keys.SELECT = True
        self.battle._pause()
        self.assertGreater(self.battle._clock.ticks, 0)
        self.assertFalse(self.battle._keys.PAUSE)
        self.assertFalse(self.battle._keys.SELECT)

    def test_game_over_loop(self):
        self.battle._gameover = True
        self.battle._game_over()
        self.assertGreater(self.battle._clock.ticks, 0)
        self.assertTrue(self.battle._keys.SELECT)
        self.assertFalse(self.battle._gameover)

    def test_player_loop_quit(self):
        q = [('quit', 'quit')]
        self.battle._eventhandler.set_event_queue(q)
        action, target = self.battle._player_loop(self.curr)
        self.assertIsNone(action)
        self.assertIsNone(target)

    def test_player_loop_magic(self):
        q = [
            ('keydown', 'down'), ('keydown', 'down'), ('keydown', 'select'),
            ('keydown', 'select'), ('keydown', 'back'), ('keydown', 'select'),
            ('keydown', 'right'), ('keydown', 'left'), ('keydown', 'select')
        ]
        self.battle._eventhandler.set_event_queue(q)
        action, target = self.battle._player_loop(self.curr)
        self.assertEqual(action, 'test_magic')
        self.assertIsNotNone(target)

    def test_player_loop_attack(self):
        action, target = self.battle._player_loop(self.curr)
        self.assertEqual(action, 'attack')
        self.assertIsNotNone(target)

    def test_player_loop_pause_and_item(self):
        q = [
            ('keydown', 'pause'), ('keydown', 'pause'), ('keydown', 'up'),
            ('keydown', 'select'), ('keydown', 'select'), ('keydown', 'select')
        ]
        self.battle._eventhandler.set_event_queue(q)
        action, target = self.battle._player_loop(self.curr)
        self.assertEqual(action, 'test_item1')
        self.assertIsNotNone(target)
        self.assertGreater(self.battle._clock.ticks, 0)

    def test_player_loop_not_enough_items(self):
        self.curr.character.use_item('test_item1', self.curr.character)
        q = [
            ('keydown', 'up'), ('keydown', 'select'), ('keydown', 'select'),
            ('keydown', 'back'), ('keydown', 'back'), ('keydown', 'down'),
            ('keydown', 'select'), ('keydown', 'select')
        ]
        self.battle._eventhandler.set_event_queue(q)
        action, target = self.battle._player_loop(self.curr)
        self.assertEqual(action, 'attack')
        self.assertIsNotNone(target)

    def test_player_loop_not_enough_mp(self):
        self.curr.character.curr_mp = 0
        q = [
            ('keydown', 'down'), ('keydown', 'down'), ('keydown', 'select'),
            ('keydown', 'select'), ('keydown', 'back'), ('keydown', 'back'),
            ('keydown', 'down'), ('keydown', 'down'), ('keydown', 'select'),
            ('keydown', 'select')
        ]
        self.battle._eventhandler.set_event_queue(q)
        action, target = self.battle._player_loop(self.curr)
        self.assertEqual(action, 'attack')
        self.assertIsNotNone(target)

    def test_battle_loop_victory(self):
        enem = self.battle._gfx.enemies.sprites()[0]
        self.battle._turns[enem] = 100
        enem.character.curr_hp = 1
        self.battle._turns[self.curr] = 0
        self.battle.loop()
        self.assertTrue(self.battle._victory)

    def test_battle_loop_player_lost(self):
        self.battle._victory = True
        enem = self.battle._gfx.enemies.sprites()[0]
        self.battle._turns[enem] = 0
        self.curr.character.curr_hp = 1
        self.battle._turns[self.curr] = 100
        self.curr.character.curr_hp = 1
        self.battle.loop()
        self.assertFalse(self.battle._victory)

    def test_battle_loop_pause_then_quit(self):
        q = [('keydown', 'pause'), ('keydown', 'pause'), ('quit', 'quit')]
        self.battle._eventhandler.set_event_queue(q)
        self.battle.loop()
        self.assertFalse(self.battle._gameover)
