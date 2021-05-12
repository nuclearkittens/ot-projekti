import os.path
import pygame as pg

from config import DIRNAME, FONT, DARK_PURPLE, POWDER_ROSE

class Renderer:
    '''A class for handling all rendering on screen.

    attr:
        display: Pygame display
    '''
    def __init__(self, display):
        '''Renderer class constructor.

        args:
            display: current Pygame display
        '''
        self._display = display

    def blit(self, surf, pos=(0, 0)):
        '''Blits an image (or surface) on screen.

        args:
            surface: Surface; image/surface to be blitted
            pos: Rect/tuple; either rectangle or coordinate
                tuple to specify the position of the surface
        '''
        self._display.blit(surf, pos)

    def fill(self, surf, colour=DARK_PURPLE):
        '''Fills a surface with a colour.

        args:
            surf: Surface; surface to be filled
            colour: tuple; colour used in fillinf the surface;
                defaults to dark purple
        '''
        surf.fill(colour)

    def create_text(self, text, size, colour=POWDER_ROSE):
        '''Creates a surface with rendered text.

        args:
            text: str; text to be rendered
            size: int; font size
            colour: tuple; font colour

        return:
            Surface
        '''
        font = pg.font.Font(os.path.join(DIRNAME, FONT), size)
        return font.render(text, False, colour)

    # def draw_text(self, text, size, pos, colour):
    #     '''Blits a text surface on screen.

    #     args:
    #         text: str; text to be rendered
    #         size: int; font size;
    #         pos: tuple; coordinates for the center of the text
    #         colour: font colour
    #     '''
    #     text_surf = self.create_text(text, size, colour)
    #     text_rect = text_surf.get_rect()
    #     text_rect.center = pos
    #     self.blit(text_surf, text_rect)

    def draw_cursor(self, cursor, dest):
        '''Draws cursor on the surface specified.

        args:
            cursor: Cursor object (sprite)
            dest: Surface; destination surface
        '''
        dest.blit(cursor.image, cursor.rect)

    def draw_sprites(self, spritegroup):
        '''Draws a sprite Group on the display.

        args:
            spritegroup: sprite Group; sprites to be drawn
        '''
        spritegroup.draw(self._display)

    def update_display(self):
        '''Updates display. Should be called once in a loop.'''
        pg.display.update()
