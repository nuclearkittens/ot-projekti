import pygame as pg

class Renderer:
    def __init__(self, display):
        self._display = display
        

    def render(self):
        pg.display.update()