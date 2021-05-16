import pygame as pg

from config import FPS
from core.prepare import initialise_demo_display, create_demo_party
from core.keys import Keys
from database.initialise_db import initialise_db, drop_tables
from database.db_util import get_db_connection
from ui.event_handler import EventHandler
from ui.renderer import Renderer
from ui.help_screen import HelpScreen
from ui.title import TitleScreen
from combat.battle import Battle

class Demo:
    '''A class that functions as the demo itself.

    attr:
        clock: Pygame Clock object
        keys: Keys object
        eventhandler: EventHandler object
        screen: Pygame display
        renderer: Renderer object
        titlescreen: TitleScreen object
        party: lst; party formation used in the demo
        battle: bool; tells whether the demo is on battle state
        title: bool; tells whether the demo is on title state
        help: bool; tells whether to display the help menu
    '''
    def __init__(self):
        '''Constructor for the Demo class.'''
        initialise_db()

        self._clock = pg.time.Clock()
        self._keys = Keys()
        self._eventhandler = EventHandler(self._keys)

        self._screen = initialise_demo_display()
        self._renderer = Renderer(self._screen)
        self._title_screen = TitleScreen(self._renderer)
        self._help_screen = HelpScreen(self._renderer)

        self._party = create_demo_party()

        self.battle = False
        self.title = False
        self.help = False

    def loop(self):
        '''The main game loop.'''
        self.title = True
        running = True

        while running:
            self._eventhandler.check_input()
            if self._keys.QUIT:
                running = False
            if self.battle:
                self._new_battle()
            if self.help:
                self._help_loop()
            if self.title:
                self._title_loop()
            self._keys.reset_keys()

        conn = get_db_connection()
        drop_tables(conn)
        conn.close()

    def _render(self):
        '''Updates the game display. Called once per loop.'''
        self._renderer.update_display()

    def _new_battle(self):
        '''Creates a new Battle object, and runs the battle loop.'''
        battle = Battle(
            self._clock, self._renderer,
            self._eventhandler, self._party
            )
        battle.loop()
        self.battle = False
        if not self._keys.QUIT:
            self.title = True
            self._party = create_demo_party()

    def _help_loop(self):
        '''Displays the help screen.'''
        self._keys.reset_keys()

        while self.help:
            self._eventhandler.check_input()
            if self._keys.QUIT or self._keys.BACK:
                self.help = False
                if self._keys.BACK:
                    self.title = True
            self._help_screen.render()
            self._render()
            self._clock.tick(FPS)

    def _title_loop(self):
        '''Loops the title screen menu if on title status.'''
        self._title_screen.menu.active = True
        self._title_screen.menu.reset_cursor()
        self._keys.reset_keys()

        while self.title:
            self._eventhandler.check_input()
            if self._keys.QUIT:
                self.title = False
            action = self._title_screen.update(self._keys)
            self._keys.reset_keys()
            if action == 'battle':
                self.battle = True
                self.title = False
            elif action == 'help':
                self.help = True
                self.title = False
            elif action == 'quit':
                self._keys.QUIT = True
            self._title_screen.render()
            self._render()
            self._clock.tick(FPS)

        self._title_screen.menu.reset_buttons()
