from collections import deque
import unittest
import pygame as pg

from config import NATIVE_RESOLUTION, TILE_SIZE, TEST_IMG
from database.initialise_db import initialise_db
from prepare import create_demo_party
from battle import Battle
from keys import Keys
from ui.renderer import Renderer

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

    def test_check_events(self):
        events = [('keydown', 'pause')]
        self.battle._eventhandler.set_event_queue(events)
        self.battle._check_events()
        self.assertTrue(self.battle._keys.PAUSE)

    def test_generate_turns(self):
        turns = self.battle._generate_turns()
        self.assertIsInstance(turns, dict)
        self.assertEqual(len(turns), 2)

    def test_reset_menus(self):
        pass
