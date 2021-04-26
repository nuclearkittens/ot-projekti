import random

from character import Character
from util import load_file
from config import ENEM_DB

class Monster(Character):
    def __init__(self, clock, renderer, name):
        Character.__init__(self, clock, renderer, name)
        self.hp_bar_center = True

        self.category = None
        self.drops = None

        self._load_data()

    def set_tick_speed(self):
        rand = random.randint(-3, 3)
        self.tick_spd = 100 // self.agi + rand

    def make_decision(self, target_list):
        if self.curr_hp < self.max_hp // 4 and self.items:
            action = random.choice(self.items)
            target = self
        else:
            action = random.choice(self.skills) # hox! remember to add magics to random.choices
            target = random.choice(target_list)
        return action, target

    def _load_data(self):
        data = load_file(ENEM_DB)
        for key, val in data.items():
            if key == self.name:
                self.proper_name = val['name']
                self.category = val['category']
                self.descr = val['descr']
                self.drops = val['drops']
                self._set_stats(val['stats'])
                # self._fetch_skills(val['tech'])
                # self._fetch_items(val['items'])
                self._set_skills(val['tech'])
                self.items = val['items']
                break

    # def _fetch_items(self, items):
    #     for item, qty in items.items():
    #         new_item = fetch_item(item)
    #         self.items.add(new_item, qty)
