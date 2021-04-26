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
        self._menus = ['main', 'skill', 'magic', 'item']

    def execute_action(self, action):
        if action in self._items:
            self._current.remove_item(action)
            self._items[action].use(self._target)
            return True
        elif action in self._skills:
            self._skills[action].use(self._current, self._target)
            return True
        elif action in self._magics:
            self._magics[action].use(self._current, self._target)
            return True
        return False

    def check_action(self, action):
        if action in self._menus or action == 'no action':
            return True
        return False

    def _generate_turns(self):
        for char in self._participants:
            self._turns[char] = char.set_tick_speed()

    def tick(self):
        for counter in self._turns.values():
            if counter > 0:
                counter -= 1

    def check_turn(self):
        self._reset_current()
        self._reset_target()
        for char in self._turns:
            if self._turns[char] == 0:
                self._current = char
                self._reset_counter()

    def _reset_counter(self):
        self._turns[self._current] = self._current.set_tick_speed()

    def _reset_current(self):
        self._current = None

    # def set_target(self, target):
    #     self.target = target

    def _reset_target(self):
        self._target = None

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