import pygame

class MainGame:
    def __init__(self, gamestate, renderer, keys, eventcheck, battle, titlescreen, menu1, menu2):
        self._gamestate = gamestate
        self._renderer = renderer
        self._keys = keys
        self._eventcheck = eventcheck
        self._battle = battle
        self._titlescreen = titlescreen
        self._menu1 = menu1
        self._menu2 = menu2

        self.running = self._gamestate.running
        self.current = None
        self._test_val = False

    def new_game(self):
        self.running = True
        self._gamestate.title = True
        self.start()

    def start(self):
        if not self._test_val:
            while self.running:
                self.check_state()

    def check_state(self):
        if self._gamestate.battle:
            self.current = self._gamestate.battle
            self._battle.game_loop()
        elif self._gamestate.title:
            self.current = self._gamestate.title
            self._titlescreen.display_menu()
        elif self._gamestate.menu1:
            self.current = self._gamestate.menu1
            self._menu1.display_menu()
        elif self._gamestate.menu2:
            self.current = self._gamestate.menu2
            self._menu2.display_menu()



