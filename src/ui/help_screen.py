import pygame as pg

from config import SCREEN_W, SCREEN_H, FONT_SIZE, DARK_ROSE

class HelpScreen:
    '''A class for a simple, static screen displaying controls info.

    attr:
        base: Surface; background for the screen
        info: list; list of items to be drawn on screen
    '''
    def __init__(self, renderer):
        '''HelpScreen class constructor.

        args:
            renderer: Renderer object
        '''
        self._renderer = renderer
        self._base = pg.Surface((SCREEN_W, SCREEN_H)).convert()
        self._info = self._create_info()

    def render(self):
        '''Blits the info on screen.'''
        self._renderer.fill(self._base)
        self._renderer.blit(self._base)
        for text in self._info:
            self._renderer.blit(text[0], text[1])

    def _create_info(self):
        '''Populates the info list.

        return:
            text: list; list of tuples containig a text surface
            and its bounding rectangle
        '''
        title = 'HELP'
        t_pos = (SCREEN_W // 2, SCREEN_H // 6)
        info = 'press BACK to return to title'
        i_pos = (SCREEN_W // 2, 5 * SCREEN_H // 6)
        options = ['move:', 'select:', 'back:', 'pause:']
        keys = ['ARROW KEYS', 'RETURN', 'BACKSPACE', 'P']

        text = []
        text.append(self._create_text(title, t_pos, True, 2 * FONT_SIZE))
        text.append(self._create_text(info, i_pos, True, FONT_SIZE))

        col_x = 2 * SCREEN_W // 7
        col_y = SCREEN_H // 3

        for i in range(4):
            pos_o = (col_x, col_y)
            pos_k = (SCREEN_W // 2, col_y)
            text.append(
                self._create_text(options[i], pos_o, False, FONT_SIZE)
                )
            text.append(
                self._create_text(keys[i], pos_k, False, FONT_SIZE, DARK_ROSE)
                )
            col_y += (SCREEN_H // 9)

        return text

    def _create_text(self, text, pos, center, size, colour=None):
        '''Creates a text surface.

        args:
            text: str; text to be written
            pos: tuple; x- and y-coordinates
            center: bool; tells if the text is centered or left-aligned
            colour: tuple; colour of the text; defaults to powder rose
            if not specified

        return:
            tuple: text surface and its bounding rectangle
        '''
        if colour:
            surf = self._renderer.create_text(text, size, colour)
        else:
            surf = self._renderer.create_text(text, size)
        
        if center:
            rect = surf.get_rect(center=pos)
        else:
            rect = surf.get_rect(midleft=pos)

        return (surf, rect)



