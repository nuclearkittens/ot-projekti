import pygame as pg

from bar import HPBar
from util import fetch_blk_spell, fetch_skill

class Character(pg.sprite.Sprite):
    def __init__(self, clock, renderer, name):
        self._clock = clock
        self._renderer = renderer
        self._update_time = self._clock.get_ticks()

        pg.sprite.Sprite.__init__(self)
        self.name = name
        self._proper_name = None
        self._descr = None
        self.alive = True
        self._tick_spd = None

        self._max_hp = None
        self._curr_hp = None
        self._max_mp = None
        self._curr_mp = None

        self._str = None
        self._mag = None
        self._defs = None
        self._mdef = None
        self._agi = None
        self._res = None

        self.hp_bar = None
        self.hp_bar_center = False

        self._anim_lst = []
        self._frame_idx = 0
        self._action = 0 # 0: idle, 1: attack, 2: hurt, 3: dead
        self._load_imgs()
        self.image = self._anim_lst[0][0]
        self.rect = self.image.get_rect()

        self._items = {}
        # self.skills = SkillContainer(self)
        # self.magic = SkillContainer(self)
        self._skills = []
        self._magic = []

    def new_hp_bar(self, w, h, x, y):
        self.hp_bar = HPBar(w, h, self._max_hp, self._curr_hp, self.hp_bar_center)
        self.hp_bar.set_position(x, y)

    def set_position(self, x, y):
        self.rect.midbottom = (x, y)

    def set_tick_speed(self):
        return self._agi

    def reset_tick_speed(self):
        self._tick_spd = None

    def check_hp(self):
        if self._curr_hp > self._max_hp:
            self._curr_hp = self._max_hp
        elif self._curr_hp <= 0:
            self._curr_hp = 0
            self.alive = False

    def check_mp(self):
        if self._curr_mp > self._max_mp:
            self._curr_mp = self._max_mp

    def remove_item(self, item):
        if item in self._items:
            if self._items[item] == 1:
                self._items.pop(item)
            else:
                self._items[item] -= 1

    def update(self):
        anim_cooldown = 200
        self.image = self._anim_lst[self._action][self._frame_idx]
        if self._clock.get_ticks() - self._update_time > anim_cooldown:
            self._update_time = self._clock.get_ticks()
            self._frame_idx += 1
        if self._frame_idx >= len(self._anim_lst[self._action]):
            self._frame_idx = 0

    def _load_imgs(self):
        frames_lst = [
            ['idle1.png', 'idle2.png'],
            ['attack1.png', 'attack2.png', 'attack3.png', 'attack4.png'],
            ['idle1.png', 'hurt.png'],
            ['dead.png']
        ]
        for frames in frames_lst:
            temp = []
            for frame in frames:
                path = f'assets/gfx/sprites/{self.name}/{frame}'
                temp.append(self._renderer.load_img(path))
            self._anim_lst.append(temp)

    def _load_data(self):
        pass

    def _fetch_items(self):
        pass

    def _set_stats(self, stats):
        self._max_hp = stats['hp']
        self._curr_hp = stats['hp']
        self._max_mp = stats['mp']
        self._curr_mp = stats['mp']
        self._str = stats['str']
        self._mag = stats['mag']
        self._defs = stats['def']
        self._mdef = stats['mdef']
        self._agi = stats['agi']
        self._res = stats['res']

    def _set_skills(self, skills):
        self._skills = skills['skills']
        self._magic = skills['blk_mag']

    def _fetch_skills(self, tech):
        for skill in tech['skills']:
            new_skill = fetch_skill(skill)
            self._skills.add(new_skill)
        for skill in tech['blk_mag']:
            new_skill = fetch_blk_spell(skill)
            self._magic.add(new_skill)

    @property
    def skills(self):
        return self._skills

    @property
    def items(self):
        return self._items

    @property
    def magics(self):
        return self._magic