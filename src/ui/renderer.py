import os.path
import pygame as pg

from config import DIRNAME, FONT, DARK_PURPLE

class Renderer:
    def __init__(self, display):
        self._display = display

    def blit(self, surf, pos):
        self._display.blit(surf, pos)

    def fill(self, surf, colour=DARK_PURPLE):
        surf.fill(colour)

    def create_text(self, text, size, colour):
        font = pg.font.Font(os.path.join(DIRNAME, FONT), size)
        return font.render(text, False, colour)

    def draw_text(self, text, size, pos, colour):
        text_surf = self.create_text(text, size, colour)
        text_rect = text_surf.get_rect()
        text_rect.center = pos
        self.blit(text_surf, text_rect)

    def draw_cursor(self, cursor, dest):
        dest.blit(cursor.image, cursor.rect)

    def draw_sprites(self, spritegroup):
        spritegroup.draw(self._display)

    def update_display(self):
        pg.display.update()
