from collections import deque

import unittest
import pygame as pg

from config import NATIVE_RESOLUTION
from core.prepare import create_demo_party
from core.keys import Keys
from database.initialise_db import initialise_db
from ui.renderer import Renderer
from combat.battle import Battle

class StubEventHandler:
    def __init__(self):
        self.keys = Keys()
        self.queue = deque()

    def set_event_queue(self, event_queue):
        for event in event_queue:
            self.queue.append(event)

    def check_input(self):
        event = self.queue.popleft()
        if event[0] == 'quit':
            self.keys.QUIT = True
            self._quit()
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

    def _quit(self):
        pg.quit()

class StubClock:
    def tick(self, FPS):
        pass

def init_test_battle():
    screen = pg.display.set_mode(NATIVE_RESOLUTION, pg.HIDDEN)
    renderer = Renderer(screen)
    party = create_demo_party()
    events = StubEventHandler()
    clock = StubClock()
    return Battle(clock, renderer, events, party)

class TestBattleMethods(unittest.TestCase):
    def setUp(self):
        initialise_db()
        pg.init()
        self.battle = init_test_battle()

    def tearDown(self):
        pg.quit()

    def test_generate_turns(self):
        turns = self.battle._generate_turns()
        self.assertIsInstance(turns, dict)
        self.assertEqual(len(turns), 2)

    def test_get_current(self):
        q = deque(self.battle._generate_turns().keys())
        curr = self.battle._get_current(q)
        self.assertEqual(curr.character.name, 'Bob')

    def test_get_current_empty_queue(self):
        curr = self.battle._get_current(deque())
        self.assertIsNone(curr)

    def test_get_current_all_dead(self):
        q = deque(self.battle._generate_turns().keys())
        for sprite in q:
            sprite.character.alive = False
        curr = self.battle._get_current(q)
        self.assertIsNone(curr)

    def test_check_events(self):
        events = [('keydown', 'pause')]
        self.battle._eventhandler.set_event_queue(events)
        self.battle._check_events()
        self.assertTrue(self.battle._keys.PAUSE)

    def test_check_events_quit(self):
        events = [('quit', 'quit')]
        self.battle._eventhandler.set_event_queue(events)
        self.battle._check_events()
        self.assertTrue(self.battle._keys.QUIT)
        self.assertFalse(pg.get_init())

    def test_check_turn(self):
        self.battle._generate_turns()
        for i in range(15):
            self.battle._tick()
        curr = self.battle._check_turn()
        self.assertEqual(curr.character.name, 'Bob')

    def test_check_turn_no_ones_turn(self):
        self.battle._generate_turns()
        curr = self.battle._check_turn()
        self.assertIsNone(curr)

    def test_game_over_false(self):
        self.battle._check_game_over()
        self.assertFalse(self.battle._gameover)
    
    def test_game_over_player_lost(self):
        self.battle._gfx.party.empty()
        self.battle._check_game_over()
        self.assertTrue(self.battle._gameover)
        self.assertFalse(self.battle._victory)

    def test_game_over_player_won(self):
        self.battle._gfx.enemies.empty()
        self.battle._check_game_over()
        self.assertTrue(self.battle._gameover)
        self.assertTrue(self.battle._victory)

    def test_choose_target(self):
        self.battle._gfx.target_cursor.active = True
        self.battle._keys.SELECT = True
        target, name = self.battle._choose_target()
        self.assertIsNotNone(target)
        self.assertEqual(name, 'Bob')

    def test_choose_target_none_selected(self):
        self.battle._gfx.target_cursor.active = True
        self.battle._keys.BACK = True
        target, name = self.battle._choose_target()
        self.assertIsNone(target)
        self.assertEqual(name, 'Bob')

    def test_choose_target_cursor_inactive(self):
        target, name = self.battle._choose_target()
        self.assertIsNone(target)
        self.assertIsNone(name)

    def test_tick_all_alive(self):
        self.battle._generate_turns()
        expected = [val-1 for val in self.battle._turns.values()]
        self.battle._tick()
        actual = list(self.battle._turns.values())
        self.assertListEqual(actual, expected)

    def test_tick_all_dead(self):
        self.battle._generate_turns()
        self.battle._gfx.all.empty()
        self.battle._gfx.party.empty()
        self.battle._gfx.enemies.empty()
        self.battle._tick()
        actual = list(self.battle._turns.values())
        expected = [-1, -1]
        self.assertListEqual(actual, expected)

    def test_update_player_turn(self):
        self.battle._generate_turns()
        expected = list(self.battle._turns.values())
        self.battle._update(True)
        actual = list(self.battle._turns.values())
        self.assertListEqual(actual, expected)

    def test_update_not_player_turn(self):
        self.battle._keys.START = True
        self.battle._generate_turns()
        expected = [val-1 for val in self.battle._turns.values()]
        self.battle._update()
        actual = list(self.battle._turns.values())
        self.assertListEqual(actual, expected)
        self.assertFalse(self.battle._keys.START)
