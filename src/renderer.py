import os.path
import pygame as pg

from config import DIRNAME, FONT, DARK_PURPLE

class Renderer:
    def __init__(self, display):
        self._display = display

    def load_img(self, relative_path):
        return pg.image.load(os.path.join(DIRNAME, relative_path)).convert_alpha()

    def blit(self, surf, pos=(0, 0)):
        self._display.blit(surf, pos)

    def fill(self, surf, colour=DARK_PURPLE):
        surf.fill(colour)

    def draw_text(self, text, size, pos, colour):
        font = pg.font.Font(os.path.join(DIRNAME, FONT), size)
        text_surf = font.render(text, False, colour)
        text_rect = text_surf.get_rect()
        text_rect.center = pos
        self.blit(text_surf, text_rect)

    def draw_cursor(self, cursor):
        self.blit(cursor.image, cursor.rect)

    def draw_bar(self, bar):
        self.fill(bar.base, DARK_PURPLE)
        self.blit(bar.base, bar.rect)
        self.fill(bar.top_bar, bar.colour)
        self.blit(bar.top_bar, bar.top_rect)
