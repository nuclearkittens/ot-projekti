from skill import Skill

class OffensiveSkill(Skill):
    def __init__(self, name, descr, element, effects, hits, mp_cost, multiplier, crit_rate):
        Skill.__init__(self, name, descr, element, effects, hits, mp_cost, multiplier, crit_rate)

    def use(self, user, target):
        return self._use_offensive(user, target)