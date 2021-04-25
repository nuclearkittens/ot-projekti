import pygame as pg
from config import HP_GREEN, HP_YELLOW, HP_RED, MP_BLUE

class Bar(pg.sprite.Sprite):
    def __init__(self, w, h, center):
        pg.sprite.Sprite.__init__(self)
        self.w = w
        self.h = h
        self.image = None
        self.colour = None
        self.center = center

        self.base = pg.Surface((self.w, self.h))
        self.rect = self.base.get_rect()
        self.top_bar = pg.Surface((self.w, self.h))
        self.top_rect = self.top_bar.get_rect()

    def set_position(self, x, y):
        if self.center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)
        self.top_rect.topleft = self.rect.topleft

    def update(self):
        pass

    def draw(self):
        pass

class HPBar(Bar):
    def __init__(self, w, h, max_hp, curr_hp, center):
        Bar.__init__(self, w, h, center)
        self.colour = HP_GREEN
        self._max_hp = max_hp
        self._curr_hp = curr_hp

    def update(self):
        ratio = self._curr_hp / self._max_hp
        if ratio > 0.5:
            self.colour = HP_GREEN
        elif ratio < 0.2:
            self.colour = HP_RED
        else:
            self.colour = HP_YELLOW    
        new_w = int(ratio*self.w)
        pg.transform.scale(self.top_bar, (new_w, self.h))

class MPBar(Bar):
    def __init__(self, w, h, max_mp, curr_mp, center=False):
        Bar.__init__(self, w, h, center)
        self.colour = MP_BLUE
        self._max_mp = max_mp
        self._curr_mp = curr_mp

    def update(self):
        ratio = self._curr_mp / self._max_mp 
        new_w = int(ratio*self.w)
        pg.transform.scale(self.top_bar, (new_w, self.h))
