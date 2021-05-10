import pygame as pg

from config import (
    SCREEN_W, SCREEN_H, BAR_W, BAR_H,
    HP_GREEN, HP_RED, MP_BLUE)
from prepare import create_demo_enemies
from util import load_img
from ui.menu import BattleMenu
from ui.buttons import DamageText
from ui.cursors import TargetCursor

class BattleGFX:
    '''A class for updating and handling the graphics elements in battle.

    attr:
        enemies: lst; enemies to defeat in battle; currently creates a demo battle,
            to be updated when random battles become a reality
        party: lst; list of available party members
        all: sprite Group; contains both enemies' and party's battle sprites
        target_cursor: Target Cursor object; used for choosing target for
            an action
        dmg_text: sprite Group; group for handling damage text buttons
        bg_img: Surface; background image for the battle
        menus: dict; menus used in battle
        default_menu: BattleMenu object; default menu that remains drawn on the
            screen for the duration of the battle
    '''
    def __init__(self, party):
        '''Constructor for the BattleGFX class.

        args:
            party: lst; list of current party members
        '''
        self.enemies = [enem.battlesprite for enem in create_demo_enemies()]
        self.party = [member.battlesprite for member in party]
        self.all = pg.sprite.Group(self.enemies, self.party)
        self.target_cursor = TargetCursor()
        self.dmg_text = pg.sprite.Group()

        self.bg_img = load_img('assets/gfx/backgrounds/battlebg1.png')
        self.menus = {}
        self.default_menu = None

        self._create_menus()
        self._calc_sprite_placement()
        self._calc_target_cursor_pos()

    def create_dmg_txt_button(self, stat, amount, target):
        '''Creates a button displaying damage taken/amount healed.

        args:
            stat: str; HP or MP
            amount: int; amount healed or damage taken
            target: BattleSprite object
        '''
        if stat == 'hp':
            if amount < 0:
                colour = HP_RED
            else:
                colour = HP_GREEN
        elif stat == 'mp':
            colour = MP_BLUE

        button = DamageText(str(abs(amount)), colour, target.rect.midtop)
        button.add(self.dmg_text)

    def render(self, renderer, current=None):
        '''Draws the graphic elements on screen.

        args:
            renderer: Renderer object
            current: Character object; character whose turn it is
        '''
        renderer.blit(self.bg_img, (0, 0))
        renderer.draw_sprites(self.all)
        renderer.draw_sprites(self.dmg_text)
        for sprite in self.all:
            sprite.draw_bars(renderer)
        if current not in self.party:
            self.default_menu.reset_cursor()
            self.default_menu.draw(renderer)

    def draw_cursor(self, renderer):
        '''Draws the target selection cursor if target selection is in an active state.

        args:
            renderer: Renderer object
        '''
        if self.target_cursor.active:
            renderer.blit(self.target_cursor.image, self.target_cursor.rect)

    def update_sprites(self):
        '''Updates all sprites as per their own update methods.'''
        def update_dmg_buttons():
            '''Checks that the damage buttons don't overlap.'''
            sprites = sorted(
                self.dmg_text.sprites(), key=lambda sprite: sprite.rect.y,
                reverse=True)
            for idx, sprite in enumerate(sprites, start=1):
                if idx < len(sprites)-1:
                    if sprite.rect.y - sprites[idx].rect.y < sprite.rect.h:
                        sprite.rect.y = sprites[idx].rect.y - sprite.rect.h

        self.all.update()
        update_dmg_buttons()
        self.dmg_text.update()

    def update_target_list(self):
        '''Checks if the length of the target list remains the same,
        i.e. has any of the participants died, and updates the
        target cursor position list accordingly.
        '''
        if len(self.all) < len(self.target_cursor.pos):
            self._calc_target_cursor_pos()

    def _calc_sprite_placement(self):
        '''Function to calculate the sprite placement on screen. Is called when
        class is initialised.'''
        def enemy_placement(x, y, offset, max_w):
            '''Calculates the on-screen placement for enemy sprites and their HP bars.

            args:
                x: int; x-coordinate for the leftmost sprite to place
                y: int; y-coordinate for the leftmost sprite to place
                offset: int; sprite offset
                max_w: int; maximum possible width of an enemy sprite
            '''
            for sprite in self.enemies:
                hp_offset = sprite.rect.height + offset
                sprite.set_position(x, y)
                sprite.create_hp_bar(BAR_W, BAR_H)
                sprite.set_bar_position(x, y - hp_offset, True)
                x += max_w
                y -= offset

        def party_placement(x, y, bar_x, bar_y, max_w, offset, margin):
            '''Calculates the on-screen placement for party and their HP/MP bars.

            args:
                x: int; x-coordinate for the leftmost sprite to place
                y: int; y-coordinate for the leftmost sprite to place
                bar_x: int; x-coordinate for the topmost HP bar
                bar_y: int; y-coordinate for the topmost HP bar
                offset: int; sprite offset
                margin: int; margin for bar placement
            '''
            for sprite in self.party:
                sprite.set_position(x, y)
                sprite.create_hp_bar((2 * BAR_W), (2 * BAR_H))
                sprite.create_mp_bar((2 * BAR_W), BAR_H)
                sprite.set_bar_position(bar_x, bar_y + margin, False)
                x += max_w
                y += offset
                margin += margin

        margin = SCREEN_W // 16
        gutter = margin // 8

        max_w_enem = ((SCREEN_W // 2) - margin) // len(self.enemies)
        max_w_party = ((SCREEN_W // 2) - margin) // len(self.party)

        offset = margin
        enem_x = max_w_enem // 2
        enem_y = 3 * SCREEN_H // 4 - (offset + (gutter * (len(self.enemies)-1)))
        party_x = (max_w_party // 2) + (SCREEN_W // 2) + margin
        party_y = 3 * SCREEN_H // 4 - offset

        offset = gutter
        enemy_placement(enem_x, enem_y, offset, max_w_enem)

        bar_x = SCREEN_W - ((2 * BAR_W) + margin // 2)
        bar_y = (3 * SCREEN_H // 4) - margin
        party_placement(
            party_x, party_y, bar_x, bar_y, max_w_party,
            offset, margin)

    def _calc_target_cursor_pos(self):
        '''Calculates the possible positions for a target cursor.'''
        self.target_cursor.pos = sorted(
            [sprite.rect.midright for sprite in self.all])
        self.target_cursor.current_pos = self.target_cursor.pos[0]

    def _create_menus(self):
        '''Creates menus for each party member in battle.'''
        main_options = ['attack', 'skill', 'magic', 'item']

        def skill_options(char):
            '''Creates menu button options for a character's skill
            and magic menus.

            args:
                char: Character object
            '''
            temp_skl = []
            temp_mag = []
            for skill_id, skill in char.skills.items():
                if skill_id != 'attack':
                    if skill.category == 'skills':
                        temp_skl.append((skill_id, skill.name.lower(), skill.mp_cost))
                    elif skill.category == 'magic':
                        temp_mag.append((skill_id, skill.name.lower(), skill.mp_cost))
            return temp_skl, temp_mag

        def item_options(char):
            '''Creates menu button options for a character's item menu.

            args:
                char: Character object
            '''
            temp = []
            for item_id, lst in char.inventory.items():
                temp.append((item_id, lst[0].name, lst[1]))
            return temp

        item_menu = None
        for sprite in self.party:
            char_menus = {}
            skl_options, mag_options = skill_options(sprite.character)
            itm_options = item_options(sprite.character)
            char_menus['main'] = BattleMenu('main', main_options)
            if self.default_menu is None:
                self.default_menu = char_menus['main']
            char_menus['skill'] = BattleMenu('skill', skl_options)
            char_menus['magic'] = BattleMenu('magic', mag_options)
            if item_menu is None:
                item_menu = BattleMenu('item', itm_options)
            char_menus['item'] = item_menu
            self.menus[sprite] = char_menus
