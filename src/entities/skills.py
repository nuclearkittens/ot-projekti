from collections import namedtuple
from random import random, uniform

class Skill:
    def __init__(self, skill_id, conn):
        self._id = skill_id
        self._conn = conn

        self._info = self._load_info()
        self._attr = self._load_attr()

    def use(self, user, target):
        mult = target.res[self._attr.element] * self._attr.multiplier
        # print(self._info.category)
        if self._info.category == 'skills':
            atk, defs = user.atk, target.defs
        elif self._info.category == 'magic':
            atk, defs = user.mag, target.mdef
        # print(atk, defs)
        for i in range(self._attr.hits):
            if atk < defs // 2:
                dmg = 1
            else:
                dmg = self._calc_dmg(atk, defs, mult)
            target.curr_hp -= dmg

    def _calc_dmg(self, atk, defs, mult):
        rand = uniform(0.8, 1.2)
        if self._is_critical():
            mult *= 1.5
        return int(rand * (mult * (atk - (defs / 2))))

    def _is_critical(self):
        return random() < self._attr.crit_rate

    def _load_info(self):
        Info = namedtuple('Info', ['name', 'category', 'subcategory', 'description'])
        cur = self._conn.cursor()
        cur.execute(
            '''SELECT name, category, subcategory, descr
            FROM Skills WHERE Skills.id=?''', (self._id,)
        )

        return Info._make(tuple(cur.fetchone()))


    def _load_attr(self):
        Attributes = namedtuple('Attributes', [
            'element', 'hits', 'mp_cost', 'multiplier', 'crit_rate'])
        cur = self._conn.cursor()
        cur.execute(
            '''SELECT element, hits, mp_cost, multiplier, crit_rate
            FROM Skills WHERE Skills.id=?''', (self._id,)
        )
        return Attributes._make(tuple(cur.fetchone()))

    @property
    def mp_cost(self):
        return self._attr.mp_cost

    @property
    def name(self):
        return self._info.name

    @property
    def category(self):
        return self._info.category
