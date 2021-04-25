import pygame as pg

class Clock:
    def __init__(self):
        self.clock = pg.time.Clock()

    def tick(self, fps=60):
        self.clock.tick(fps)

    def get_ticks(self):
        return pg.time.get_ticks()