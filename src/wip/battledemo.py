import pygame
from collections import deque

from src.keys import Keys
from src.eventcheck import EventCheck
from src.gamestate import GameState
from src.renderer import Renderer
from src.constants import *
from src.load_util import load_img
from battlemenu import BattleMenu
from monster import Monster
from player import Player

class BattleDemo:
    def __init__(self, renderer, keys, gamestate, eventcheck):
        self._renderer = renderer
        self._keys = keys
        self._gamestate = gamestate
        self._eventcheck = eventcheck
        self._menu = BattleMenu(self, self._renderer, self._keys, self._gamestate, self._eventcheck)
        
        self.turns = deque([])

        # these are here just for the demo; figure out a better way for the actual battle
        self.ej = Player('ej')
        self.witch = Player('witch')
        self.monster1 = Monster('ikorni')
        self.monster2 = Monster('ikorni')

        self.party = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.all = pygame.sprite.group()

        self.party.add(self.ej, self.witch)
        self.monsters.add(self.monster1, self.monster2)
        self.all.add(self.ej, self.witch, self.monster1, self.monster2)

        self.atk = Attack("Attack")

    def battle_loop(self):
        while self._gamestate.battle:
            self._menu.display_menu()
            nxt = self.turns.popleft()
            self.turns.append(next_turn)
            if nxt in self.party:
                self._eventcheck.check()
                self._menu.move_cursor()
                if self._menu.check_state():
                    if self._menu.state == 'attack':
                        target = self.monsters.sprites()
                        self.attack(nxt, target[0])
                    # haven't done anything about items or skills/magic yet, so these can wait
                    elif self._menu.state == 'skills':
                        pass
                    elif self._menu.state == 'items':
                        pass
            else:
                target = self.party.sprites()
                self.attack(nxt, target[0])
            self.health_check()
            

    def generate_battle_queue(self):
        temp = []
        for sprite in self.all:
            temp.append((sprite.agi, sprite))
        temp.sort(reverse=True)
        for sprite in temp:
            self.turns.append(sprite[1])

    def attack(self, user, target): 
        dmg = self.atk.use_skill(user, target)
        target.curr_hp -= dmg

    def health_check(self):
        for sprite in self.all:
            if sprite.curr_hp <= 0:
                sprite.alive = False
                sprite.kill()
    



            




    

