from collections import deque

import unittest
import pygame as pg

from config import NATIVE_RESOLUTION
from core.demo import Demo
from core.keys import Keys
from database.initialise_db import initialise_db
from ui.renderer import Renderer

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
            event = ('quit', 'quit')

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

class TestDemo(unittest.TestCase):
    def setUp(self):
        initialise_db()
        pg.init()
        self.demo = Demo()
        self.demo._eventhandler = StubEventHandler()
        self.demo._keys = self.demo._eventhandler.keys
        self.demo._clock = StubClock()
        self.demo._screen = pg.display.set_mode(NATIVE_RESOLUTION, pg.HIDDEN)
        self.demo._renderer = Renderer(self.demo._screen)

    def tearDown(self):
        pg.quit()

    def test_new_battle(self):
        self.demo.battle = True
        q = [('keydown', 'select') for x in range(2000)]
        self.demo._eventhandler.set_event_queue(q)
        self.demo._new_battle()
        self.assertFalse(self.demo.battle)
        self.assertTrue(self.demo.title)

    def test_new_battle_quit(self):
        self.demo.battle = True
        self.demo._new_battle()
        self.assertFalse(self.demo.battle)
        self.assertFalse(self.demo.title)

    def test_title_loop_choose_battle(self):
        self.demo.title = True
        q = [('keydown', 'select') for x in range(5)]
        self.demo._eventhandler.set_event_queue(q)
        self.demo._title_loop()
        self.assertTrue(self.demo.battle)
        self.assertFalse(self.demo.title)

    def test_title_loop_quit(self):
        self.demo.title = True
        self.demo._title_loop()
        self.assertFalse(self.demo.battle)
        self.assertFalse(self.demo.title)

    def test_title_loop_help_then_quit(self):
        self.demo.title = True
        q = [
            ('keydown', 'down'), ('keydown', 'select'),
            ('keydown', 'down'), ('keydown', 'select')
        ]
        self.demo._eventhandler.set_event_queue(q)
        self.demo._title_loop()
        self.assertTrue(self.demo.help)
        self.assertFalse(self.demo.title)
        self.assertTrue(self.demo._keys.QUIT)

    def test_main_loop_quit(self):
        self.demo.loop()
        self.assertTrue(self.demo._keys.QUIT)
    
    def test_main_loop_title(self):
        self.demo.title = True
        self.demo._eventhandler.set_event_queue([(None, None)])
        self.demo.loop()
        self.assertFalse(self.demo.title)
        self.assertTrue(self.demo._keys.QUIT)

    def test_main_loop_battle(self):
        self.demo.battle = True
        q = [(None, None), (None, None)]
        self.demo._eventhandler.set_event_queue(q)
        self.demo.loop()
        self.assertFalse(self.demo.battle)
        self.assertTrue(self.demo._keys.QUIT)
