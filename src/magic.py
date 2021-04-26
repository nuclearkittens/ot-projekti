from skill import Skill

class BlackMagic(Skill):
    def __init__(self, name, descr, element, effects, hits, mp_cost, multiplier, crit_rate):
        Skill.__init__(self, name, descr, element, effects, hits, mp_cost, multiplier, crit_rate)
        self.magic = True

    def use(self, user, target):
        return self._use_offensive(user, target)

class WhiteMagic(Skill):
    def __init__(self, name, descr, element, effects, hits, mp_cost, multiplier, crit_rate):
        Skill.__init__(self, name, descr, element, effects, hits, mp_cost, multiplier, crit_rate)
        self.magic = True

    def use(self, user, target):
        return self._use_defensive(user, target)
        