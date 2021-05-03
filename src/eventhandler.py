import pygame as pg

class EventHandler:
    def __init__(self, keys):
        self._keys = keys

    def check_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._keys.QUIT = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self._keys.SELECT = True
                if event.key == pg.K_BACKSPACE:
                    self._keys.BACK = True
                if event.key == pg.K_DOWN:
                    self._keys.DOWN = True
                if event.key == pg.K_UP:
                    self._keys.UP = True
                if event.key == pg.K_LEFT:
                    self._keys.LEFT = True
                if event.key == pg.K_RIGHT:
                    self._keys.RIGHT = True

    @property
    def keys(self):
        return self._keys
