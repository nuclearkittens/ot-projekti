import pygame as pg
from config import HP_GREEN, HP_YELLOW, HP_RED, MP_BLUE, DARK_PURPLE

class Bar(pg.sprite.Sprite):
    def __init__(self, w, h, center):
        pg.sprite.Sprite.__init__(self)
        self.w = w
        self.h = h
        self.colour = None
        self.center = center

        self.base = pg.Surface((self.w, self.h))
        self.base.fill(DARK_PURPLE)
        self.base_rect = self.base.get_rect()
        self.image = pg.Surface((self.w, self.h))
        self.rect = self.image.get_rect()

    def set_position(self, x, y):
        if self.center:
            self.base_rect.center = (x, y)
        else:
            self.base_rect.topleft = (x, y)
        self.rect.topleft = self.rect.topleft

    def update(self):
        pass

    def draw(self):
        pass

class HPBar(Bar):
    def __init__(self, owner, w, h, max_hp, center):
        Bar.__init__(self, w, h, center)
        self._owner = owner
        self.colour = HP_GREEN
        self._max_hp = max_hp
        self._curr_hp = max_hp

    def update(self):
        self._curr_hp = self._owner.hp
        ratio = self._curr_hp / self._max_hp
        if ratio > 0.5:
            self.colour = HP_GREEN
        elif ratio < 0.2:
            self.colour = HP_RED
        else:
            self.colour = HP_YELLOW
        new_w = int(ratio*self.w)
        self.image = pg.Surface((new_w, self.h))
        self.image.fill(self.colour)
        # top_rect = top_bar.get_rect()
        # top_rect.topleft = self.rect.topleft
        # self.image.blit(top_bar, self.rect)
        

class MPBar(Bar):
    def __init__(self, owner, w, h, max_mp, center=False):
        Bar.__init__(self, w, h, center)
        self._owner = owner
        self.colour = MP_BLUE
        self._max_mp = max_mp
        self._curr_mp = max_mp

    def update(self):
        # self.image.fill(DARK_PURPLE)
        self._curr_mp = self._owner.mp
        ratio = self._curr_mp / self._max_mp
        new_w = int(ratio*self.w)
        # pg.transform.scale(self.top_bar, (new_w, self.h))
        self.image = pg.Surface((new_w, self.h))
        self.image.fill(MP_BLUE)
        # top_rect = top_bar.get_rect()
        # top_rect.topleft = self.rect.topleft
        # self.image.blit(top_bar, self.rect)
