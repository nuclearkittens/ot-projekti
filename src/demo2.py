import pygame as pg

from config import SCREEN_W, SCREEN_H
from clock import Clock
from renderer import Renderer
from battlespritehandler import BattleSpriteHandler
from party import Party
from containers import ItemContainer, SkillContainer
from buttons import BattleMenuButton, ActionButton, ItemButton
from keys import Keys
from eventhandler import EventHandler
from battleactionhandler import BattleActionHandler

class Demo:
    def __init__(self):
        pg.init()

        self.running = True

        self._screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
        pg.display.set_caption('battle demo v2')

        self._clock = Clock()
        self._renderer = Renderer(self._screen)
        self._keys = Keys()
        self._events = EventHandler(self._keys)

        self._item_cntr = ItemContainer()
        self._skill_cntr = SkillContainer('skill')
        self._magic_cntr = SkillContainer('blk_mag')

        # get rid of the party object for actual battle idk needs work
        self._current_party = Party(self._clock)
        self._current_party.add_item('potion', 3)
        self._current_party.add_item('witch_potion')

        self.bg_img = self._renderer.load_img('assets/gfx/backgrounds/battlebg1.png')

        self.gutter = SCREEN_W // 64
        self.panel_w = (SCREEN_W // 3) - self.gutter
        self.panel_h = SCREEN_H // 4

        self.main_panel = pg.Surface((self.panel_w, self.panel_h))
        self._renderer.fill(self.main_panel)
        self.main_rect = self.main_panel.get_rect()
        self.main_pos = (self.gutter, SCREEN_H - self.panel_h - self.gutter)
        self.main_rect.topleft = self.main_pos
        self.main_buttons = pg.sprite.Group()

        self.sub_panel = pg.Surface((self.panel_w, self.panel_h))
        self._renderer.fill(self.sub_panel)
        self.sub_rect = self.sub_panel.get_rect()
        self.sub_pos = (self.panel_w + self.main_pos[0] + self.gutter, self.main_pos[1])
        self.sub_rect.topleft = self.sub_pos

        self.skill_buttons = {} # key, val: char, pg.group()
        self.mag_buttons = {}
        self.item_buttons = pg.sprite.Group()
        self.all_buttons = pg.sprite.Group()

        self.main_active = False
        self.sub_active = False
        self.skl_active = False
        self.mag_active = False
        self.itm_active = False
        self.target_active = False

        self._create_menu_buttons()

        self._sprite_handler = BattleSpriteHandler(self._clock, self._renderer, self._current_party)
        self._participants = self._sprite_handler.participants

        self.action_handler = BattleActionHandler(
            self._participants, self._item_cntr.items,
            self._skill_cntr.skills, self._magic_cntr.skills
            )

    def _create_menu_buttons(self):
        def button_pos(sub=True):
            # max 4 items in a menu atm, fix this later
            pos = []
            y = self.main_pos[1]
            if sub:
                x = self.sub_pos[0] + self.gutter
            else:
                x = self.main_pos[0] + self.gutter
            for i in range(4):
                pos.append((x, y))
                y += self.panel_h // 4
            return pos

        def skill_options(char):
            temp_skills = []
            for skill in char.skills:
                if skill != 'attack':
                    info = self._skill_cntr.fetch_skill(skill)
                    name, cost = info[0].lower(), info[5]
                    temp_skills.append((name, cost))
            return temp_skills

        def magic_options(char):
            temp_mag = []
            for mag in char.magics:
                info = self._magic_cntr.fetch_skill(mag)
                name, cost = info[0].lower(), info[5]
                temp_mag.append((name, cost))
            return temp_mag

        def item_menu(items):
            options = []
            for itm, qty in items.items():
                info = self._item_cntr.fetch_item(itm)
                name = info[0].lower()
                options.append((name, qty))
            if not options:
                return
            else:
                pos = button_pos()
                for i in range(len(options)):
                    name, qty = options[i][0], options[i][1]
                    new_button = ItemButton(name, qty)
                    new_button.rect.topleft = pos[i]
                    new_button.add(self.item_buttons, self.all_buttons)
                    # self.item_buttons.add(new_button)

        def main_menu():
            options = ['attack', 'magic', 'skill', 'item']
            pos = button_pos(False)
            for i in range(len(options)):
                option = options[i]
                new_button = BattleMenuButton(option)
                new_button.rect.topleft = pos[i]
                new_button.add(self.main_buttons, self.all_buttons)
                # self.main_buttons.add(new_button)

        for char in self._current_party.group:
            skl = skill_options(char)
            mag = magic_options(char)
            skl_group = pg.sprite.Group()
            mag_group = pg.sprite.Group()
            pos = button_pos()
            if skl:
                for i in range(len(skl)):
                    name, cost = skl[i][0], skl[i][1]
                    new_button = ActionButton(name, cost)
                    new_button.rect.topleft = pos[i]
                    new_button.add(skl_group, self.all_buttons)
                    # skl_group.add(new_button)
            if mag:
                for i in range(len(mag)):
                    name, cost = mag[i][0], mag[i][1]
                    new_button = ActionButton(name, cost)
                    new_button.rect.topleft = pos[i]
                    new_button.add(mag_group, self.all_buttons)
                    # mag_group.add(new_button)
            self.skill_buttons[char] = skl_group
            self.mag_buttons[char] = mag_group

        item_menu(self._current_party.items)
        main_menu()

    def _draw_all(self, current_char=None):
        self._renderer.blit(self.bg_img)
        self._renderer.blit(self.main_panel, self.main_pos)
        self._sprite_handler.draw_sprites()
        self.all_buttons.update()
        if self.sub_active:
            self._renderer.blit(self.sub_panel, self.sub_pos)
            if self.skl_active:
                self._renderer.draw_sprites(self.skill_buttons[current_char])
            elif self.mag_active:
                self._renderer.draw_sprites(self.mag_buttons[current_char])
            elif self.itm_active:
                self._renderer.draw_sprites(self.item_buttons)
        self._renderer.draw_sprites(self.main_buttons)

    def _player_action(self, current_char):
        action = None
        while True:
            self._events.check_input()
            self._draw_all(current_char)
            pos = self._keys.mouse_position
            if pos:
                for button in self.all_buttons:
                    if button.rect.collidepoint(pos):
                        button.active = True
                    else:
                        button.active = False
            if self._keys.SELECT:
                pos = self._keys.mouse_position
                if not self.target_active:
                    action = self._menu_action(pos, current_char)
                    if (
                            action in current_char.skills or
                            action in current_char.magics or
                            action in current_char.items or
                            action == 'attack'
                        ):
                        self.target_active = True
                    for button in self.all_buttons:
                        if button.rect.collidepoint(pos):
                            button.pressed = True
                        else:
                            button.pressed = False
                else:
                    for target in self._participants:
                        if target.rect.collidepoint(pos):
                            self._keys.reset_keys()
                            self.target_active = False
                            return action, target
            pg.display.update()

    def _menu_action(self, pos, current_char):
        if self.sub_active:
            if self.itm_active:
                for button in self.item_buttons:
                    if button.rect.collidepoint(pos):
                        # self.itm_active = False
                        # self.sub_active = False
                        self.target_active = True
                        return button.action
            elif self.skl_active:
                for button in self.skill_buttons[current_char]:
                    if button.rect.collidepoint(pos):
                        # self.skl_active = False
                        # self.sub_active = False
                        self.target_active = True
                        return button.action
            elif self.mag_active:
                for button in self.mag_buttons[current_char]:
                    if button.rect.collidepoint(pos):
                        # self.mag_active = False
                        # self.sub_active = False
                        self.target_active = True
                        return button.action
        for button in self.main_buttons:
            if button.rect.collidepoint(pos):
                self._reset_menus()
                if button.action != 'attack':
                    if button.action == 'skill':
                        self.skl_active = True
                    elif button.action == 'magic':
                        self.mag_active = True
                    elif button.action == 'item':
                        self.itm_active = True
                    self.sub_active = True
                return button.action
        self._keys.reset_keys()
        return None

    def _reset_menus(self):
        self.sub_active = False
        self.skl_active = False
        self.mag_active = False
        self.itm_active = False

    def game_loop(self):
        party = self._current_party.current_party
        enemies = self._sprite_handler.enemies
        action = None
        target = self.action_handler.target
        current_char = self.action_handler.current
        while self.running:
            if self._events.quit():
                self.running = False
            self._reset_menus()
            self._draw_all(current_char)
            self.action_handler.tick()
            self.action_handler.check_turn()
            current_char = self.action_handler.current
            if current_char in party:
                action, target = self._player_action(current_char)
            elif current_char in enemies:
                action, target = current_char.make_decision(party)
            print(action, target)
            self.action_handler.target = target
            print(self.action_handler.target)
            self.action_handler.execute_action(action)
            self._clock.tick()
            pg.display.update()
        pg.quit()


if __name__ == '__main__':
    demo = Demo()
    demo.main_active = True
    # demo.sub_active = True
    demo.game_loop()