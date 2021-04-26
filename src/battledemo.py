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


class BattleMenuHandler:
    def __init__(self, keys, renderer, item_container, skill_container, magic_container, party):
        self._keys = keys
        self._renderer = renderer,
        self._items = item_container.items
        self._skills = skill_container.skills
        self._magics = magic_container.skills
        self._party = party

        self.menu_pos = self._calc_menu_placement()
        self.all_menus = []
        self.menu_actions = ['skill', 'magic', 'item']

        self.main_menu = self._create_main_menu()
        self.all_menus.append(self.main_menu)
        self.main_menu.active = True
        # self.current_menu = self.main_menu

        self.skill_menus = {}
        self.magic_menus = {}
        self.item_menu = self._create_item_menu()
        self.all_menus.append(self.item_menu)

        self._create_char_menus()

    def draw_menus(self, current):
        action = None
        self.main_menu.draw_menu()
        for menu in self.all_menus:
            if menu.active:
                action = menu.update()
                menu.active = False
                if action in self.menu_actions:
                    if action == self.menu_actions[0]:
                        self.skill_menus[current].active = True
                    elif action == self.menu_actions[1]:
                        self.magic_menus[current].active = True
                    else:
                        self.item_menu.active = True
        return action

    def _calc_menu_placement(self):
        temp = []
        c = SCREEN_W // 4
        x = 0
        y = 3 * SCREEN_H // 4
        for i in range(2):
            temp.append((x, y))
            x += c
        return temp

    def _create_char_menus(self):
        x = self.menu_pos[1][0]
        y = self.menu_pos[1][1]

        for char in self._party.group.sprites():
            temp_options = []
            temp_actions = []
            temp_skills, temp_mag = self._create_options(char)
            for skill, val in temp_skills.items():
                text = f'{val[0]:20}{val[1]}'
                temp_actions.append(skill)
                temp_options.append(text)
            new_menu = BattleMenu(
                'skill', [char], self._renderer, self._keys,
                temp_options, temp_actions, x, y
                )
            self.all_menus.append(new_menu)
            self.skill_menus[char] = new_menu
            temp_options = []
            for mag, val in temp_mag.items():
                text = f'{val[0]:20}{val[1]}'
                temp_actions.append(mag)
                temp_options.append(text)
            new_menu = BattleMenu(
                'magic', [char], self._renderer, self._keys,
                temp_options, temp_actions, x, y
                )
            self.all_menus.append(new_menu)
            self.magic_menus[char] = new_menu

    def _create_item_menu(self):
        x = self.menu_pos[1][0]
        y = self.menu_pos[1][1]

        temp_options = []
        temp_actions = []
        temp_frames = []
        for item, qty in self._party.items.items():
            name = self._items[item]._name
            text = f'{name:20}{qty}'
            temp_options.append(text)
            temp_actions.append(item)
            itm_frames = []
            for i in range(qty+1):
                text = f'{name:20}{i}'
                itm_frames.append(text)
            temp_frames.append(itm_frames)

        new_menu = BattleMenu(
            'item', self._party.group.sprites(),
            self._renderer, self._keys,
            temp_options, temp_actions, x, y
            )

        for button in new_menu.buttons.sprites():
            if hasattr(button, 'text'):
                for frames in temp_frames:
                    if button.text == frames[-1]:
                        frames.pop()
                        for frame in frames:
                            button.add_frame(frame)
                        frames = None
        return new_menu

    def _create_options(self, char):
        temp_skills = {}
        temp_mag = {}
        for skill in char.skills:
            if skill in self._skills and skill != 'attack':
                name, cost = self._skills[skill]._name, self._skills[skill]._mp_cost
                temp_skills[skill] = (name, cost)
        for mag in char.magic:
            if mag in self._magics:
                name, cost = self._magics[mag]._name, self._magics[mag]._mp_cost
                temp_mag[mag] = (name, cost)
        return temp_skills, temp_mag

    def _create_main_menu(self):
        options = ['Attack', 'Skill', 'Magic', 'Item']
        actions = [option.lower() for option in options]
        x, y = self.menu_pos[0][0], self.menu_pos[0][1]
        return BattleMenu(
            'main', self._party.group.sprites(),
            self._renderer, self._keys,
            options, actions, x, y
            )

class BattleSpriteHandler:
    def __init__(self, clock, renderer, party, demo=True):
        self._clock = clock
        self._renderer = renderer
        self._party = party
        self._demo = demo

        self.party = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.all = pg.sprite.Group()
        self.bars = pg.sprite.Group()

        self._setup()

    def _setup(self):
        # TODO: random encounter creator;
        # fetch monsters for a certain area, initialise them here;
        # 1-3 monsters per battle
        if self._demo:
            monster1 = Monster(self._clock, self._renderer, 'ikorni')
            monster2 = Monster(self._clock, self._renderer, 'ikorni')
            self.enemies.add(monster1, monster2)
            self.all.add(monster1, monster2)
        for char in self._party.active_party:
            char.add(self.all, self.party)

        self._calc_sprite_placement()

    def _calc_sprite_placement(self):
        area_w = SCREEN_W // 2
        margin = 20 * SCALE
        gutter = 5 * SCALE
        qty_enem = len(self.enemies)
        qty_party = len(self.party)
        sprite_lst_enem = self.enemies.sprites()
        sprite_lst_party = self.party.sprites()

        hp_bar_w_enem = BAR_W
        hp_bar_h_enem = BAR_H
        hp_bar_w_party = 2 * BAR_W
        hp_bar_h_party = 2 * BAR_H
        mp_bar_w = 2 * BAR_W
        mp_bar_h = BAR_H

        max_w_enem = (area_w - margin) // qty_enem
        max_w_party = (area_w - margin) // qty_party

        offset_y = 30 * SCALE
        enem_x = max_w_enem // 2
        enem_y = 3 * SCREEN_H // 4 - (offset_y + (10 * SCALE * (qty_enem-1)))
        party_x = (max_w_party // 2) + area_w + margin
        party_y = 3 * SCREEN_H // 4 - offset_y

        offset_y = 10 * SCALE
        for sprite in sprite_lst_enem:
            hp_offset_y = sprite.rect.height + offset_y
            sprite.set_position(enem_x, enem_y)
            sprite.new_hp_bar(hp_bar_w_enem, hp_bar_h_enem, enem_x, enem_y - hp_offset_y)
            sprite.hp_bar.add(self.bars)
            enem_x += max_w_enem
            enem_y -= offset_y

        offset = 40 * SCALE
        bar_x = SCREEN_W - (hp_bar_w_party + offset // 2)
        bar_y = (3 * SCREEN_H // 4) - offset
        for sprite in sprite_lst_party:
            sprite.set_position(party_x, party_y)
            sprite.new_hp_bar(hp_bar_w_party, hp_bar_h_party, bar_x, bar_y + offset)
            mp_y = sprite.hp_bar.rect.bottomleft[1] + gutter
            sprite.new_mp_bar(mp_bar_w, mp_bar_h, bar_x, mp_y)
            button_y = mp_y - margin
            sprite.new_name_button(bar_x, button_y)
            self.bars.add(sprite.hp_bar, sprite.mp_bar)
            self.all.add(sprite.name_button)
            party_x += max_w_party
            party_y += offset_y
            offset += offset

    def draw_sprites(self):
        for sprite in self.all.sprites():
            sprite.update()
        self.all.draw(self._renderer._display)
        for bar in self.bars.sprites():
            bar.update()
            self._draw_bar(bar)

    def _draw_bar(self, bar):
        self._renderer.draw_bar(bar)

    def get_participants(self):
        return self.enemies.sprites() + self.party.sprites()

    def get_inventory(self, sprite, cat):
        values = ['skill', 'magic', 'item']
        for sprite in self.party.sprites():
            if cat == values[0]:
                return sprite.skills
            elif cat == values[1]:
                return sprite.magic
            elif cat == values[2]:
                return sprite.items.keys()

    def get_enemies(self):
        return self.enemies.sprites()

    def get_party(self):
        return self.party.sprites()

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

class BattleActionHandler:
    def __init__(self, participants, item_container, skill_container, magic_container):
        self.participants = participants
        self.turns = {}
        self._generate_turns()
        self.current = None
        self.target = None
        self._items = item_container.items
        self._skills = skill_container.skills
        self._magics = magic_container.skills
        self._menus = ['skill', 'magic', 'item']

    def execute_action(self, action):
        if action in self._items:
            self.current.remove_item(action)
            self._items[action].use(self.target)
        elif action in self._skills:
            self._skills[action].use(self.current, self.target)
        elif action in self._magics:
            self._magics[action].use(self.current, self.target)
        elif action in self._menus:
            return False
        return True

    def _generate_turns(self):
        for char in self.participants:
            self.turns[char] = char.set_tick_speed()

    def tick(self):
        for counter in self.turns.values():
            if counter > 0:
                counter -= 1

    def check_turn(self):
        for char in self.turns:
            if self.turns[char] == 0:
                self.current = char
                return self.current

    def _reset_counter(self):
        self.turns[self.current] = self.current.set_tick_speed()

    def reset_current(self):
        self.current = None

    def set_target(self, target):
        self.target = target

    def reset_target(self):
        self.target = None

if __name__ == '__main__':
    demo = BattleDemo()
    demo.main_loop()
