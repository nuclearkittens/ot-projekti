import pygame as pg

from config import FPS
from prepare import initialise_demo_display, create_demo_party
from keys import Keys
from battle import Battle
from database.initialise_db import initialise_db, drop_tables
from database.db_util import get_db_connection
from ui.eventhandler import EventHandler
from ui.renderer import Renderer

class Demo:
    '''A class that functions as the demo itself.

    attr:
        keys: Keys object
        eventhandler: EventHandler object
        screen: Pygame display
        renderer: Renderer object
        party: lst; party formation used in the demo
        battle: bool; tells whether the demo is on battle state
    '''
    def __init__(self):
        '''Constructor for the Demo class.'''
        initialise_db()

        self._clock = pg.time.Clock()
        self._keys = Keys()
        self._eventhandler = EventHandler(self._keys)

        self._screen = initialise_demo_display()
        self._renderer = Renderer(self._screen)

        self._party = create_demo_party()

        self.battle = False

    def loop(self):
        '''The main game loop.'''
        running = True
        while running:
            self._eventhandler.check_input()
            if self._keys.QUIT:
                running = False
            if self.battle:
                battle = Battle(
                    self._clock, self._renderer,
                    self._eventhandler, self._party
                    )
                battle.loop()
                self.battle = False
            self._render()
            self._clock.tick(FPS)
        conn = get_db_connection()
        drop_tables(conn)
        conn.close()

    def _render(self):
        '''Updates the game display. Called once per loop.'''
        self._renderer.update_display()
