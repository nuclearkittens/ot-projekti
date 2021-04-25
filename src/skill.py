class Skill:
    def __init__(self, name, descr, element, effects, hits, mp_cost, multiplier, crit_rate):
        self._name = name
        self._descr = descr
        self._element = element
        self._effects = effects
        self._hits = hits
        self._mp_cost = mp_cost
        self._multiplier = multiplier
        self._crit_rate = crit_rate

        self.magic = False

    def use(self, user, target):
        pass
    
    def _use_offensive(self, user, target):
        if self._check_mp(user):
            mult = target.res[self._element] * self._multiplier
            for i in range(self._hits):
                if self.magic:
                    atk, defs = user.mag, target.mdef
                else:
                    atk, defs = user.str, target.defs
                if atk < defs:
                    dmg = 1
                else:
                    dmg = self._calc_damage(atk, defs, mult)
                target.curr_hp -= dmg
            return True
        return False

    def _use_defensive(self, user, target):
        pass

    def _check_mp(self, user):
        return self._mp_cost <= user.curr_mp

    def _calc_damage(self, atk, defs, mult):
        rand = random.uniform(0.8, 1.2)
        if self._is_critical(crit_rate):
            mult *= 1.5
        return int(rand * (mult * (atk-defs)))

    def _is_critical(self):
        return random.random() < self.crit_rate