class GameState:
    def __init__(self):
        self.running = True
        self.battle = False
        self.title = True
        self.menu1 = False
        self.menu2 = False

    def set_all_false(self):
        self.running = False
        self.battle = False
        self.title = False
        self.menu1 = False
        self.menu2 = False

