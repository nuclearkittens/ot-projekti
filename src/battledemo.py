import random
import pygame as pg

from config import SCREEN_W, SCREEN_H, BAR_W, BAR_H, SCALE
from clock import Clock
from renderer import Renderer
from party import Party
from monster import Monster
from containers import ItemContainer, SkillContainer
from keys import Keys
from menu import BattleMenu
from eventcheck import EventCheck

class BattleDemo:
    def __init__(self):
        pg.init()
        self.clock = Clock()
        self.running = True

        self.screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
        pg.display.set_caption('battle demo')

        self.renderer = Renderer(self.screen)
        self.keys = Keys()
        self.eventcheck = EventCheck(self.keys)

        self.item_container = ItemContainer()
        self.skill_container = SkillContainer('skill')
        self.magic_container = SkillContainer('blk_mag')

        self.bg_img = self.renderer.load_img('assets/gfx/backgrounds/battlebg1.png')

        self.party = Party(self.clock, self.renderer)
        self.party.add_item('potion', 3)
        self.party.add_item('witch_potion')

        self.spritehandler = BattleSpriteHandler(self.clock, self.renderer, self.party)
        participants = self.spritehandler.get_participants()
        self.actionhandler = BattleActionHandler(
            participants, self.item_container, self.skill_container, self.magic_container)
        self.menuhandler = BattleMenuHandler(
            self.keys, self.renderer,
            self.item_container, self.skill_container, self.magic_container,
            self.party
            )

        self.enemies = self.spritehandler.get_enemies()
        self.players = self.spritehandler.get_party()

    def draw_bg(self):
        self.renderer.blit(self.bg_img)

    def main_loop(self):
        while self.running:
            self.eventcheck.check()
            self.clock.tick()
            self.draw_bg()
            # self.draw_menu(self.menu_base_main, self.menu_pos_main, DARK_PURPLE)
            # self.draw_menu(self.menu_base_sub, self.menu_pos_sub, DARK_ROSE)
            self.spritehandler.draw_sprites()
            self.actionhandler.tick()
            current = self.actionhandler.check_turn()
            if current is not None:
                if current in self.enemies:
                    action, self.actionhandler.target = current.make_decision(self.players)
                elif current in self.players:
                    self.keys.reset_keys()
                    action = self._player_turn(current)
                if self.actionhandler.execute_action(action):
                    self.actionhandler.reset_current()
                    self.actionhandler.reset_target()
            pg.display.update()
        pg.quit()

    def _player_turn(self, current):
        menu_actions = self.menuhandler.menu_actions
        running = True
        while running:
            self.eventcheck.check()
            action = self.menuhandler.draw_menus(current)
            if action is not None:
                if action in menu_actions:
                    continue
                else:
                    target = random.choice(self.enemies)
                    self.actionhandler.set_target(target)
                    running = False
            self.keys.reset_keys()
            pg.display.update()
        return action

class BattleState:
    def __init__(self):
        self.attack = False
        self.skill = False
        self.magic = False
        self.items = False

    def reset(self):
        self.attack = False
        self.skill = False
        self.magic = False
        self.items = False

if __name__ == '__main__':
    demo = BattleDemo()
    demo.main_loop()
