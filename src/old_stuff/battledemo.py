import random
import pygame as pg

from config import SCREEN_W, SCREEN_H
from clock import Clock
from renderer import Renderer
from party import Party
from containers import ItemContainer, SkillContainer
from keys import Keys
from eventhandler import EventHandler
from battleactionhandler import BattleActionHandler
from battlemenuhandler import BattleMenuHandler
from battlespritehandler import BattleSpriteHandler

class BattleDemo:
    def __init__(self):
        pg.init()
        self.clock = Clock()
        self.running = True

        self.screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
        pg.display.set_caption('battle demo')

        self.renderer = Renderer(self.screen)
        self.keys = Keys()

        self.item_cntr = ItemContainer()
        self.skill_cntr = SkillContainer('skill')
        self.magic_cntr = SkillContainer('blk_mag')

        self.bg_img = self.renderer.load_img('assets/gfx/backgrounds/battlebg1.png')

        self.party_obj = Party(self.clock, self.renderer)
        self.party_obj.add_item('potion', 3)
        self.party_obj.add_item('witch_potion')

        self.party = self.party_obj.active_party

        self.event_handler = EventHandler(self.keys)
        self.sprite_handler = BattleSpriteHandler(self.clock, self.renderer, self.party_obj)
        self.menu_handler = BattleMenuHandler(self.keys, self.renderer, self.party_obj)
        self.action_handler = BattleActionHandler(
            self.sprite_handler.participants, self.item_cntr.items,
            self.skill_cntr.skills, self.magic_cntr.skills
            )

        self.enemies = self.sprite_handler.enemies

    def _draw_bg(self):
        self.renderer.blit(self.bg_img)

    def main_loop(self):
        action = 'no action'
        target = self.action_handler.target
        while self.running:
            self._draw_bg()
            self.menu_handler.draw_main_menu()
            if self.event_handler.quit():
                self.running = False
            self.action_handler.tick()
            self.action_handler.check_turn()
            current = self.action_handler.current
            if current:
                print(current)
                if current in self.party:
                    action, target = self._player_turn(current)
                elif current in self.enemies:
                    action, target = current.make_decision(self.party)
                print(action, target)
                if target:
                    self.action_handler.target = target
                if self.action_handler.execute_action(action):
                    print('action executed!')
            self.sprite_handler.draw_sprites()
            self.clock.tick()
            pg.display.update()

    def _player_turn(self, current):
        print('player turn!')
        menu = True
        while True:
            self.event_handler.check_input()
            action = self.menu_handler.get_action(current)
            print(action)
            menu = self.action_handler.check_action(action)
            if not menu:
                target = random.choice([enem for enem in self.enemies if enem.alive])
                return action, target
            self.sprite_handler.draw_sprites()
            self.clock.tick()

    def _draw_panel(self, submenu):
        panel_w = SCREEN_W // 4
        panel_h = SCREEN_H // 4
        colour = DARK_PURPLE
        margin = int(0.1 * panel_w)
        gutter = int(0.01 * SCREEN_W)

        def draw_main_menu():
            surf = pg.Surface((panel_w, panel_h))


if __name__ == '__main__':
    demo = BattleDemo()
    demo.main_loop()
