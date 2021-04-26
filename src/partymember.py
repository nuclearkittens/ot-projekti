import pygame as pg
import random
import math

from character import Character
from buttons import Button
from bar import HPBar, MPBar
from containers import SkillContainer
from util import load_file, fetch_blk_spell, fetch_item, fetch_skill
from config import PARTY_DB, FONT_SIZE, DARK_PURPLE

class PartyMember(Character):
    def __init__(self, clock, renderer, name, items):
        Character.__init__(self, clock, renderer, name)

        self.mp_bar = None
        self.name_button = None
        self.items = items
        self.lvl = None
        self.joined = False
        self.active = False

        self._load_data()

    def join_party(self):
        self.joined = True

    def add_to_active_party(self):
        self.active = True

    def remove_from_active_party(self):
        self.active = False

    def new_mp_bar(self, w, h, x, y):
        self.mp_bar = MPBar(w, h, self.max_mp, self.curr_mp)
        self.mp_bar.set_position(x, y)

    def new_name_button(self, x, y):
        self.name_button = Button(self.proper_name.upper(), FONT_SIZE // 2, DARK_PURPLE)
        self.name_button.rect.midleft = (x, y)

    def set_tick_speed(self):
        rand = random.randint(-2, 2)
        self.tick_spd = 100 // self.agi + rand

    def _load_data(self):
        data = load_file(PARTY_DB)
        for key, val in data.items():
            if key == self.name:
                self.proper_name = val['name']
                self.lvl = val['lvl']
                self._set_stats(val['stats'])
                self._set_skills(val['tech'])
                break
