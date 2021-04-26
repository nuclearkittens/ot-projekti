import pygame as pg

from config import SCREEN_W, SCREEN_H, SCALE, BAR_W, BAR_H
from monster import Monster

class BattleSpriteHandler:
    def __init__(self, clock, renderer, party):
        self._clock = clock
        self._renderer = renderer
        self._party = party

        self.party = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.all = pg.sprite.Group()
        self.bars = pg.sprite.Group()

        self._setup()

    def _setup(self):
        # TODO: random encounter creator;
        # fetch monsters for a certain area, initialise them here;
        # 1-3 monsters per battle
        monster1 = Monster(self._clock, self._renderer, 'ikorni')
        monster2 = Monster(self._clock, self._renderer, 'ikorni')
        self.enemies.add(monster1, monster2)
        self.all.add(monster1, monster2)
        for char in self._party.group:
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
        # self.all.draw(self._renderer._display)
        self._renderer.draw_sprites(self.all)
        for bar in self.bars.sprites():
            bar.update()
            self._draw_bar(bar)

    def _draw_bar(self, bar):
        self._renderer.draw_bar(bar)

    # @property
    # def item_inventory(self, owner):
    #     try:
    #         if owner in self.all:
    #             return self.all.sprites(owner.items)
    #     except KeyError:
    #         return 'owner not found'

    # @property
    # def skill_inventory(self, owner):
    #     try:
    #         if owner in self.all:
    #             return self.all.sprites(owner.skills)
    #     except KeyError:
    #         return 'owner not found'

    # @property
    # def magic_inventory(self, owner):
    #     try:
    #         if owner in self.all:
    #             return self.all.sprites(owner.magic)
    #     except KeyError:
    #         return 'owner not found'

    # @property
    # def enemies(self):
    #     return self.enemies.sprites()

    # @property
    # def partymembers(self):
    #     return self.party.sprites()

    @property
    def participants(self):
        return self.enemies.sprites() + self.party.sprites()