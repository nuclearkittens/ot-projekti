class Item:
    def __init__(self, name, category, descr, effects):
        self._name = name
        self._category = category
        self._descr = descr
        self._effects = effects

    def use(self, target):
        if self._category == 'healing':
            self._use_healing_item(target)

    def _use_healing_item(self, target):
        if 'hp' in self._effects:
            amount = self._effects['hp']
            if amount > 1:
                target.curr_hp += amount
            else:
                target.curr_hp += amount * target.max_hp

        if 'mp' in self._effects:
            amount = self._effects['mp']
            if amount > 1:
                target.curr_mp += amount
            else:
                target.curr_mp += amount * target.max_mp
                