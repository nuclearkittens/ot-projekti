import random

from character import Character
from util import load_file
from config import ENEM_DB

class Monster(Character):
    def __init__(self, clock, renderer, name):
        Character.__init__(self, clock, renderer, name)
        self.hp_bar_center = True

        self._category = None
        self._drops = None

        self._load_data()

    def set_tick_speed(self):
        rand = random.randint(-3, 3)
        self._tick_spd = 100 // self._agi + rand
        return self._tick_spd

    def make_decision(self, target_list):
        if self._curr_hp < self._max_hp // 4 and self._items:
            action = random.choice(self._items)
            target = self
        else:
            action = random.choice(self._skills) # hox! remember to add magics to random.choices
            target = random.choice(target_list)
        return action, target

    

    def _load_data(self):
        data = load_file(ENEM_DB)
        for key, val in data.items():
            if key == self.name:
                self._proper_name = val['name']
                self._category = val['category']
                self._descr = val['descr']
                self._drops = val['drops']
                self._set_stats(val['stats'])
                # self._fetch_skills(val['tech'])
                # self._fetch_items(val['items'])
                self._set_skills(val['tech'])
                self._items = val['items']
                break

    # def _fetch_items(self, items):
    #     for item, qty in items.items():
    #         new_item = fetch_item(item)
    #         self.items.add(new_item, qty)
