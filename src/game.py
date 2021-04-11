import pygame as pg

class Game:
    def __init__(self):
        self.running = True
        self.playing = False

        self.DISPLAY_W = 512
        self.DISPLAY_H = 448
        self.display = pg.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pg.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))

        self.UP, self.DOWN, self.RIGHT, self.LEFT = False, False, False, False
        self.SELECT, self.START, self.BACK, self.PAUSE = False, False, False, False

        self.font_name = '/assets/m5x7.ttf'
        self.DARK_PURPLE = (66, 30, 66)
        self.POWDER_ROSE = (201, 143, 143)
        self.DARK_ROSE = (189, 113, 130)

    def game_loop(self):
        while self.playing:
            self.check_events()
            self.update()
            self.reset_keys()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running, self.playing = False, False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP or event.key == pg.K_W:
                    self.UP = True
                if event.key == pg.K_DOWN or event.key == pg.K_S:
                    self.DOWN = True
                if event.key == pg.K_RIGHT or event.key == pg.K_D:
                    self.RIGHT = True
                if event.key == pg.K_LEFT or event.key == pg.K_A:
                    self.LEFT = True
                if event.key == pg.K_RETURN:
                    self.SELECT = True
                if event.key == pg.K_P:
                    self.PAUSE = True

    def reset_keys(self):
        self.UP, self.DOWN, self.RIGHT, self.LEFT = False, False, False, False
        self.SELECT, self.START, self.BACK, self.PAUSE = False, False, False, False


        