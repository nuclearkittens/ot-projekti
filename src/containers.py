from util import load_file
from config import ITEMS_DB, ATKS_DB, BLK_MAG_DB
from item import Item
from techniques import OffensiveSkill
from magic import BlackMagic

class ItemContainer:
    def __init__(self):
        self._items = self._load_all_items()

    @property
    def items(self):
        return self._items

    def fetch_item(self, item):
        if item in self._items:
            return self._items[item].item
        return ValueError

    def _load_all_items(self):
        dct = {}
        data = load_file(ITEMS_DB)
        for item, val in data.items():
            new_item = Item(val['name'], val['category'], val['descr'], val['effects'])
            dct[item] = new_item
        return dct

class SkillContainer:
    def __init__(self, category):
        self.category = category
        self._skills = self._load_skills()

    @property
    def skills(self):
        return self._skills

    def fetch_skill(self, skill):
        if skill in self._skills:
            return self._skills[skill].skill
        return ValueError

    def _load_skills(self):
        if self.category == 'skill':
            skills = self._load_all_offensive_skills()
        elif self.category == 'blk_mag':
            skills = self._load_all_blk_magic()
        return skills

    def _load_all_offensive_skills(self):
        dct = {}
        data = load_file(ATKS_DB)
        for key, skill in data.items():
            new_skill = OffensiveSkill(
                skill['name'], skill['descr'], skill['element'],
                skill['effects'], skill['hits'], skill['mp_cost'],
                skill['multiplier'], skill['crit_rate']
                )
            dct[key] = new_skill
        return dct

    def _load_all_blk_magic(self):
        dct = {}
        data = load_file(BLK_MAG_DB)
        for key, skill in data.items():
            new_skill = BlackMagic(
                skill['name'], skill['descr'], skill['element'],
                skill['effects'], skill['hits'], skill['mp_cost'],
                skill['multiplier'], skill['crit_rate']
                )
            dct[key] = new_skill
        return dct
