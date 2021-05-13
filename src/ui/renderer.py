import os.path
import pygame as pg

from config import DIRNAME, FONT, DARK_PURPLE, POWDER_ROSE, SCREEN_W, SCREEN_H

class Renderer:
    '''A class for handling all rendering methods.

    attr:
        display: Pygame display
    '''
    def __init__(self, display):
        '''Renderer class constructor.

        args:
            display: current Pygame display
        '''
        self._display = display

    def screenshot(self):
        '''Takes a screenshot, returning it as a Surface object.'''
        return self._display.copy().convert()

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

    def create_transparent_surface(self, colour=DARK_PURPLE, size=(SCREEN_W, SCREEN_H)):
        '''Returns a Surface object with 50% opacity.

        args:
            colour: tuple; colour of the surface (defaults to dark purple)
            size: tuple; size of the surface (defaults to display size)

        return:
            surf: Surface
        '''
        surf = pg.Surface(size).convert()
        surf.set_alpha(128)
        self.fill(surf, colour)
        return surf

    def draw_sprites(self, spritegroup):
        '''Draws a sprite Group on the display.

        args:
            spritegroup: sprite Group; sprites to be drawn
        '''
        spritegroup.draw(self._display)

    def update_display(self):
        '''Updates display. Should be called once in a loop.'''
        pg.display.update()
