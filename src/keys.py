class Keys:
    def __init__(self):
        self.UP, self.DOWN = False, False
        self.RIGHT, self.LEFT = False, False
        self.SELECT, self.START = False, False
        self.BACK, self.PAUSE = False, False

        self._mouse_pos = None

    def reset_keys(self):
        self.UP, self.DOWN = False, False
        self.RIGHT, self.LEFT = False, False
        self.SELECT, self.START = False, False
        self.BACK, self.PAUSE = False, False

        self._mouse_pos = None

    @property
    def mouse_position(self):
        return self._mouse_pos

    @mouse_position.setter
    def mouse_position(self, pos):
        self._mouse_pos = pos

        