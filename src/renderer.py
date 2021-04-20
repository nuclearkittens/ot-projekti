import pygame
from load_util import load_font
from constants import *

class Renderer:
    def __init__(self, display):
        self._display = display
        self.screen = pygame.display.get_surface()

    def draw_text(self, text, size, x, y, colour=None):
        if not colour:
            colour = POWDER_ROSE
        font = load_font(FONT1, size)
        text_surf = font.render(text, False, colour)
        text_rect = text_surf.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text_surf, text_rect)

    def draw_cursor(self, cursor, size=32):
        self.draw_text(cursor.cursor, size, cursor.rect.x, cursor.rect.y)

    def blit_screen(self):
        self._display.blit(self.screen, (0,0))

    def update(self):
        pygame.display.update()

    def fill(self, colour=None):
        if not colour:
            colour = DARK_PURPLE
        self.screen.fill(colour)

    def draw_img(self, image, x=0, y=0):
        self.screen.blit(image, (x, y))
    
    def draw_rect(self, x, y, w, h, colour=DARK_PURPLE):
        pygame.draw.rect(self.screen, colour, (x, y, w, h))