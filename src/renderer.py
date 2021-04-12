import pygame

class Renderer:
    def __init__(self, game):
        self._game = game

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self._game.FONT_NAME, size)
        text_surf = font.render(text, True, self._game.POWDER_ROSE)
        text_rect = text_surf.get_rect()
        text_rect.center = (x,y)
        self._game.display.blit(text_surf, text_rect)