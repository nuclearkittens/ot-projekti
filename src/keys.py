class Keys:
    def __init__(self):
        self.UP, self.DOWN = False, False
        self.RIGHT, self.LEFT = False, False
        self.SELECT, self.START = False, False
        self.BACK, self.PAUSE = False, False

    def reset_keys(self):
        self.UP, self.DOWN = False, False
        self.RIGHT, self.LEFT = False, False
        self.SELECT, self.START = False, False
        self.BACK, self.PAUSE = False, False