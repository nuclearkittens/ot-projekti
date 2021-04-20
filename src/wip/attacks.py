import json
import os.path
from constants import SKILL_DIR

class Attack:
    def __init__(self, name):
        self.name = name
        with open(os.path.join(SKILL_DIR, 'attacks')) as f:
            data = json.load(f)
            for atk in data:
                if self.name == atk['name']:
                    self.mp = atk['mp']
                    self.base_dmg = atk['base_dmg']
                    self.type = atk['type']
                    self.hits = atk['hits']

    def use_skill(self, user, target, modifiers=None):
        # TODO: formulas that take other stats into consideration
        
        if user.curr_mp < self.mp:
            raise ValueError('not enough mp to use skill')
        else:
            user.curr_mp -= self.mp
        
        # fyi, none of these formulas have been tested yet, so might not work
        # old dmg formulas for ??? found in one of my notebooks so yeah
        dmg_c = (((user.strgth ** 3) // 32) * self.base_dmg // 32) // 2
        def_c = ((((target.defs - 280) ** 2) // 110) + 16) // 2
        dmg = dmg_c * def_c // 380

        if self.type != 'normal':
            elem_c = target.affinities[self.type]
            dmg *= elem_c
        
        return [dmg] * self.hits

        
