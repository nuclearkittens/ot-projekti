import pygame as pg

# from config import FPS
from prepare import initialise_demo_display, create_demo_party
from keys import Keys
from battle import Battle
from database.initialise_db import initialise_db, drop_tables
from database.db_connection import get_db_connection
from ui.eventhandler import EventHandler
from ui.renderer import Renderer

class Demo:
    def __init__(self):
        initialise_db()
        self._conn = get_db_connection()

        self._clock = pg.time.Clock()
        self._keys = Keys()
        self._eventhandler = EventHandler(self._keys)

        self._screen = initialise_demo_display()
        self._renderer = Renderer(self._screen)

        self._party = create_demo_party(self._conn)

        self.battle = False

    def loop(self):
        running = True
        while running:
            if self._keys.QUIT:
                running = False
            if self.battle:
                battle = Battle(
                    self._renderer, self._eventhandler,
                    self._party, self._conn
                    )
                battle.loop()
            self._render()
            # self._clock.tick(FPS)
        drop_tables(self._conn)
        self._conn.close()

    def _render(self):
        self._renderer.update_display()
