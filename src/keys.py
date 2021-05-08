class Keys:
    '''A class for tracking player input.

    attr:
        UP, DOWN, RIGHT, LEFT: bool; directional keys; True if pressed, otherwise False
        SELECT, START, BACK, PAUSE: bool; selection keys; True if pressed, otherwise False
        QUIT: bool; True if user closes the Pygame window
    '''
    def __init__(self):
        '''Keys class constructor.'''
        self.UP, self.DOWN = False, False
        self.RIGHT, self.LEFT = False, False
        self.SELECT, self.START = False, False
        self.BACK, self.PAUSE = False, False

        self.QUIT = False

    def reset_keys(self):
        '''Resets all the directional and selection keys to False.'''
        self.UP, self.DOWN = False, False
        self.RIGHT, self.LEFT = False, False
        self.SELECT, self.START = False, False
        self.BACK, self.PAUSE = False, False
