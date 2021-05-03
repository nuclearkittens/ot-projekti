import pygame as pg

from util import load_img
from config import SCREEN_W, SCREEN_H, BAR_W, BAR_H
from prepare import create_demo_enemies
from ui.menu import BattleMenu
from ui.buttons import TargetCursor

class BattleGFX:
    def __init__(self, party, conn):
        # change into random battle for the actual game
        self.enemies = [enem.battlesprite for enem in create_demo_enemies(conn)]
        self.party = [member.battlesprite for member in party]
        self.all = pg.sprite.Group(self.enemies, self.party)
        self.target_cursor = TargetCursor()

        self.bg_img = load_img('assets/gfx/backgrounds/battlebg1.png')
        self.menus = {}
        self.default_menu = None

        self._create_menus()
        self._calc_sprite_placement()

    def update_sprites(self):
        self.all.update()

    def update_target_list(self):
        if len(self.all) < len(self.target_cursor.pos):
            print('updating target list:')
            print(f'old: {self.target_cursor.pos}')
            self.target_cursor.pos = sorted(
                [sprite.rect.midright for sprite in self.all])
            self.target_cursor.current_pos = self.target_cursor.pos[0]
            print(f'new: {self.target_cursor.pos}')

    def render(self, renderer, current):
        renderer.blit(self.bg_img, (0, 0))
        renderer.draw_sprites(self.all)
        for sprite in self.all:
            sprite.draw_bars(renderer)
        if current not in self.party:
            self.default_menu.reset_cursor()
            self.default_menu.draw(renderer)

    def draw_cursor(self, renderer):
        if self.target_cursor.active:
            renderer.blit(self.target_cursor.image, self.target_cursor.rect)

    def _calc_sprite_placement(self):
        margin = SCREEN_W // 16
        gutter = margin // 8

        max_w_enem = ((SCREEN_W // 2) - margin) // len(self.enemies)
        max_w_party = ((SCREEN_W // 2) - margin) // len(self.party)

        offset_y = margin
        enem_x = max_w_enem // 2
        enem_y = 3 * SCREEN_H // 4 - (offset_y + (gutter * (len(self.enemies)-1)))
        party_x = (max_w_party // 2) + (SCREEN_W // 2) + margin
        party_y = 3 * SCREEN_H // 4 - offset_y

        temp_cursor_pos = []

        offset_y = gutter
        for sprite in self.enemies:
            hp_offset_y = sprite.rect.height + offset_y
            sprite.set_position(enem_x, enem_y)
            temp_cursor_pos.append(sprite.rect.midright)
            sprite.create_hp_bar(BAR_W, BAR_H)
            sprite.set_bar_position(enem_x, enem_y - hp_offset_y, True)
            enem_x += max_w_enem
            enem_y -= offset_y

        bar_x = SCREEN_W - ((2 * BAR_W) + margin // 2)
        bar_y = (3 * SCREEN_H // 4) - margin
        for sprite in self.party:
            sprite.set_position(party_x, party_y)
            temp_cursor_pos.append(sprite.rect.midright)
            sprite.create_hp_bar((2 * BAR_W), (2 * BAR_H))
            sprite.create_mp_bar((2 * BAR_W), BAR_H)
            sprite.set_bar_position(bar_x, bar_y + margin, False)
            # button_y = mp_y - margin
            # sprite.new_name_button(bar_x, button_y)
            party_x += max_w_party
            party_y += offset_y
            margin += margin

        self.target_cursor.pos = sorted(temp_cursor_pos)
        # print(self.target_cursor.pos)
        self.target_cursor.current_pos = self.target_cursor.pos[0]

    def _create_menus(self):
        main_options = ['attack', 'skill', 'magic', 'item']

        def skill_options(char):
            temp_skl = []
            temp_mag = []
            for skill in char.skills.values():
                if skill.name != 'Attack':
                    if skill.category == 'skills':
                        temp_skl.append((skill.name.lower(), skill.mp_cost))
                    elif skill.category == 'magic':
                        temp_mag.append((skill.name.lower(), skill.mp_cost))
            return temp_skl, temp_mag

        def item_options(char):
            temp = []
            for lst in char.inventory.values():
                temp.append((lst[0].name, lst[1]))
            return temp

        for sprite in self.party:
            char_menus = {}
            skl_options, mag_options = skill_options(sprite.character)
            itm_options = item_options(sprite.character)
            char_menus['main'] = BattleMenu('main', main_options)
            if self.default_menu is None:
                self.default_menu = char_menus['main']
            char_menus['skill'] = BattleMenu('skill', skl_options)
            char_menus['magic'] = BattleMenu('magic', mag_options)
            char_menus['item'] = BattleMenu('item', itm_options)
            self.menus[sprite] = char_menus
