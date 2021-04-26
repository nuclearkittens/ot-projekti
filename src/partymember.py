import random

from character import Character
from buttons import Button
from bar import MPBar
from util import load_file
from config import PARTY_DB, FONT_SIZE, DARK_PURPLE

class PartyMember(Character):
    def __init__(self, clock, renderer, name, items):
        Character.__init__(self, clock, renderer, name)

        self.mp_bar = None
        self.name_button = None
        self._items = items
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
        self.mp_bar = MPBar(w, h, self._max_mp, self._curr_mp)
        self.mp_bar.set_position(x, y)

    def new_name_button(self, x, y):
        self.name_button = Button(self._proper_name.upper(), FONT_SIZE // 2, DARK_PURPLE)
        self.name_button.rect.midleft = (x, y)

    def set_tick_speed(self):
        rand = random.randint(-2, 2)
        self._tick_spd = 100 // (self._agi + rand)
        return self._tick_spd

    def _load_data(self):
        data = load_file(PARTY_DB)
        for key, val in data.items():
            if key == self.name:
                self._proper_name = val['name']
                self.lvl = val['lvl']
                self._set_stats(val['stats'])
                self._set_skills(val['tech'])
                break
