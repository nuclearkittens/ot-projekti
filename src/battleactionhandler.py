class BattleActionHandler:
    def __init__(self, participants, items, skills, magics):
        self._participants = participants
        self._current = None
        self._target = None

        self._turns = {}
        self._generate_turns()

        self._items = items
        self._skills = skills
        self._magics = magics
        self._menus = ['skill', 'magic', 'item']

    def execute_action(self, action):
        if action in self._items:
            self.current.remove_item(action)
            self._items[action].use(self.target)
        elif action in self._skills:
            self._skills[action].use(self.current, self.target)
        elif action in self._magics:
            self._magics[action].use(self.current, self.target)
        elif action in self._menus:
            return False
        return True

    def _generate_turns(self):
        for char in self._participants:
            self._turns[char] = char.set_tick_speed()

    def tick(self):
        for counter in self._turns.values():
            if counter > 0:
                counter -= 1

    def check_turn(self):
        for char in self._turns:
            if self._turns[char] == 0:
                self._current = char
                self._reset_counter()
                return self._current

    def _reset_counter(self):
        self._turns[self._current] = self._current.set_tick_speed()

    def reset_current(self):
        self.current = None

    # def set_target(self, target):
    #     self.target = target

    def reset_target(self):
        self.target = None

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, new_target):
        self._target = new_target

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, new_current):
        self._current = new_current