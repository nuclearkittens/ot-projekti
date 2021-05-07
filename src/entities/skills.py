from random import random, uniform

class Skill:
    '''Class for skill objects.

    attr:
        info: namedtuple; contains the name, category,
        subcategory and description of the skill
        attr: namedtuple; contains the element, hits, MP cost,
        multiplier, and critical rate of the skill
    '''
    def __init__(self, skill_id):
        '''Constructor for the skill class, Imports database methods to
        load relevant info (imported outside top-level to avoid circular
        import).

        args:
            skill_id: str; unique identifier for a skill
        '''
        from database.db_util import load_skill_info, load_skill_attr
        self._id = skill_id

        self._info = load_skill_info(self._id)
        self._attr = load_skill_attr(self._id)

    def use(self, user, target):
        '''Uses a skill against a target.

        args:
            user: Character object
            target: Character object
        '''
        mult = target.res[self._attr.element] * self._attr.multiplier
        if self._info.category == 'skills':
            atk, defs = user.atk, target.defs
        elif self._info.category == 'magic':
            atk, defs = user.mag, target.mdef
        else:
            atk, defs = 0, 0

        for i in range(self._attr.hits):
            if atk < defs // 2:
                dmg = 1
            else:
                dmg = self._calc_dmg(atk, defs, mult)
            target.curr_hp -= dmg

    def _calc_dmg(self, atk, defs, mult):
        '''Calculates the damage taken by the target.

        args:
            atk: int; user's physical/magical strength
            defs: int; target's physical/magical defense
            mult: float; multiplier based on the skill's element and
            the target's resistance to that element
        '''
        rand = uniform(0.8, 1.2)
        if self._is_critical():
            mult *= 1.5
        return int(rand * (mult * (atk - (defs / 2))))

    def _is_critical(self):
        '''Checks if the skill does critical damage.'''
        return random() < self._attr.crit_rate

    @property
    def mp_cost(self):
        '''Returns the MP cost of a skill.'''
        return self._attr.mp_cost

    @property
    def name(self):
        '''Returns the name of the skill.'''
        return self._info.name

    @property
    def category(self):
        '''Returns the category of the skill.'''
        return self._info.category
