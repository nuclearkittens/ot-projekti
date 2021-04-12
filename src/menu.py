import pygame
from cursor import Cursor

class Menu:
    def __init__(self, game, w=512, h=448, offset=-100):
        self._game = game
        self._renderer = self._game._renderer
        self.mid_w = w // 2
        self.mid_h = h // 2
        self.offset = offset

        self.cursor = Cursor('>')

        self.run_menu = True


    # def draw_cursor(self):
    #     self._game._renderer.draw_text('>', 32, self.cursor.rect.x, self.cursor.rect.y)

    # def blit_screen(self):
    #     self._game._renderer.screen.blit(self._game.display, (0, 0))
    #     pygame.display.update()
    #     self._game.reset_keys()

    def blit(self):
        self._renderer.blit_screen()
        self._renderer.update()
        self._game.reset_keys()

