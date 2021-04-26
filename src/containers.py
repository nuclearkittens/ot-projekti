from util import load_file
from config import ITEMS_DB, ATKS_DB, BLK_MAG_DB
from item import Item
from techniques import OffensiveSkill
from magic import BlackMagic

class ItemContainer:
    def __init__(self):
        self._items = self._load_all_items()

    # def add(self, item, qty=1):
    #     if item not in self.items:
    #         self.items[item._name] = qty
    #         self.items_lst.append(item._name)
    #     else:
    #         self.items[item._name] += qty

    # def use(self, item, target):
    #     self.items[item._name] -= 1
    #     item.use(target)
    #     if self.items[item._name] == 0:
    #         self.items.pop(item._name)
    #         self.items_lst.remove(item)

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

    # def add(self, skill):
    #     if skill not in self.skills:
    #         self.skills.append(skill)

    # def use(self, skill, target):
    #     skill.use(self._owner, target)
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
        # print(data)
        for key, skill in data.items():
            # print(key, skill)
            new_skill = OffensiveSkill(
                skill['name'], skill['descr'], skill['element'],
                skill['effects'], skill['hits'], skill['mp_cost'],
                skill['multiplier'], skill['crit_rate']
                )
            dct[key] = new_skill
        # print(dct)
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
        # print(dct)
        return dct
        
if __name__ == "__main__":
    new_sc = SkillContainer('skill')
    print(new_sc.skills)

    new_ic = ItemContainer()
    print(new_ic.items)

    print(new_ic.fetch_item('potion'))

    print(new_sc.fetch_skill('dbl_claw'))