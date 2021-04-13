import pygame
from eventcheck import EventCheck
from battle import Battle
from gamestate import GameState
from titlescreen import TitleScreen
from helpmenu import HelpMenu
from creditsmenu import CreditsMenu
from renderer import Renderer
from keys import Keys

class MainGame:
    def __init__(self):
        self.gamestate = GameState()
        self.renderer = Renderer()
        self.keys = Keys()
        self.eventcheck = EventCheck(self.gamestate, self.keys)
        self.battle = Battle(self.gamestate, self.renderer, self.keys, self.eventcheck)
        self.titlescreen = TitleScreen(self.renderer, self.keys, self.gamestate, self.eventcheck)
        self.menu1 = HelpMenu(self.renderer, self.keys, self.gamestate, self.eventcheck)
        self.menu2 = CreditsMenu(self.renderer, self.keys, self.gamestate, self.eventcheck)

        self.running = self.gamestate.running

        self.new_game()

    def new_game(self):
        while self.running:
            self.check_state()

    def check_state(self):
        if self.gamestate.battle:
            self.battle.game_loop()
        elif self.gamestate.title:
            self.titlescreen.display_menu()
        elif self.gamestate.menu1:
            self.menu1.display_menu()
        elif self.gamestate.menu2:
            self.menu2.display_menu()


