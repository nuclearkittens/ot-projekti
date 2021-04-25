import pygame as pg

from bar import HPBar
from containers import SkillContainer
from util import *

class Character(pg.sprite.Sprite):
    def __init__(self, clock, renderer, name):
        self._clock = clock
        self._renderer = renderer
        self.update_time = self._clock.get_ticks()

        pg.sprite.Sprite.__init__(self)
        self.name = name
        self.proper_name = None
        self.descr = None
        self.alive = True
        self.tick_spd = None

        self.max_hp = None
        self.curr_hp = None
        self.max_mp = None
        self.curr_mp = None

        self.str = None
        self.mag = None
        self.defs = None
        self.mdef = None
        self.agi = None
        self.res = None

        self.hp_bar = None
        self.hp_bar_center = False

        self.anim_lst = []
        self.frame_idx = 0
        self.action = 0 # 0: idle, 1: attack, 2: hurt, 3: dead
        self._load_imgs()
        self.image = self.anim_lst[0][0]
        self.rect = self.image.get_rect()

        self.items = None
        # self.skills = SkillContainer(self)
        # self.magic = SkillContainer(self)
        self.skills = []
        self.magic = []

    def new_hp_bar(self, w, h, x, y):
        self.hp_bar = HPBar(w, h, self.max_hp, self.curr_hp, self.hp_bar_center)
        self.hp_bar.set_position(x, y)

    def set_position(self, x, y):
        self.rect.midbottom = (x, y)

    def set_tick_speed(self):
        pass

    def reset_tick_speed(self):
        self.tick_spd = None

    def check_hp(self):
        if self.curr_hp > self.max_hp:
            self.curr_hp = self.max_hp
        elif self.curr_hp <= 0:
            self.curr_hp = 0
            self.alive = False

    def check_mp(self):
        if self.curr_mp > self.max_mp:
            self.curr_mp = self.max_mp

    def remove_item(self, item):
        if item in self.items:
            if self.items[item] == 1:
                self.items.pop(item)
            else:
                self.items[item] -= 1

    def update(self):
        anim_cooldown = 200
        self.image = self.anim_lst[self.action][self.frame_idx]
        if self._clock.get_ticks() - self.update_time > anim_cooldown:
            self.update_time = self._clock.get_ticks()
            self.frame_idx += 1
        if self.frame_idx >= len(self.anim_lst[self.action]):
            self.frame_idx = 0

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
            self.anim_lst.append(temp)

    def _load_data(self):
        pass

    def _fetch_items(self):
        pass
        
    def _set_stats(self, stats):
        for stat in stats:
            self.max_hp = stats['hp']
            self.curr_hp = stats['hp']
            self.max_mp = stats['mp']
            self.curr_mp = stats['mp']
            self.str = stats['str']
            self.mag = stats['mag']
            self.defs = stats['def']
            self.mdef = stats['mdef']
            self.agi = stats['agi']
            self.res = stats['res']

    def _set_skills(self, skills):
        for skill in skills:
            self.skills = skills['skills']
            self.magic = skills['blk_mag']

    def _fetch_skills(self, tech):
        for skill in tech['skills']:
            new_skill = fetch_skill(skill)
            self.skills.add(new_skill)
        for skill in tech['blk_mag']:
            new_skill = fetch_blk_spell(skill)
            self.magic.add(new_skill)