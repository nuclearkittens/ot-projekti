import pygame as pg

class EventHandler:
    def __init__(self, keys):
        self._keys = keys

    def check_input(self):
        for event in self._event_queue():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self._keys.START = True
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
            elif event.type == pg.MOUSEBUTTONDOWN:
                self._keys.SELECT = True
                self._keys.mouse_position = pg.mouse.get_pos()
                    
    def _event_queue(self):
        return pg.event.get()

    def quit(self):
        for event in self._event_queue():
            if event.type == pg.QUIT:
                return True
        return False
