import pygame as pg

from config import MENU_CURSOR, TARGET_CURSOR, CURSOR_SIZE, POWDER_ROSE
from ui.buttons import Button


class MenuCursor(Button):
    '''A Button subclass for menu cursors.'''
    def __init__(self):
        '''MenuCursor class constructor.'''
        Button.__init__(self, MENU_CURSOR, CURSOR_SIZE, POWDER_ROSE)

class TargetCursor(Button):
    '''A Button subclass for target selection cursor.

    attr:
        pos: lst; a list of coordinate tuples
        current_pos: tuple; current position of the cursor
        active: bool; indicator of whether target selection is active
    '''
    def __init__(self):
        '''TargetCursor class constructor.'''
        Button.__init__(self, TARGET_CURSOR, CURSOR_SIZE, POWDER_ROSE)

        self.pos = []
        self.current_pos = None
        self.active = False

    def _move_cursor(self, keys):
        '''Moves the target cursor according to player input by updating
        the current position.

        args:
            keys: Keys object'''
        if keys.RIGHT:
            for idx, pos in enumerate(self.pos):
                if self.current_pos == pos:
                    if idx == len(self.pos)-1:
                        self.current_pos = self.pos[0]
                    else:
                        self.current_pos = self.pos[idx+1]
                    break
        elif keys.LEFT:
            for idx, pos in enumerate(self.pos):
                if self.current_pos == pos:
                    if idx == 0:
                        self.current_pos = self.pos[-1]
                    else:
                        self.current_pos = self.pos[idx-1]
                    break
        self.rect.midtop = self.current_pos

    def choose_target(self, keys, spritegroup):
        '''Chooses target by checking collisions if the cursor is active.

        args:
            keys: Keys object
            spritegroup: sprite Group object

        return:
            target: sprite object
        '''
        target = None
        if self.active:
            self._move_cursor(keys)
            if keys.SELECT:
                target = pg.sprite.spritecollide(self, spritegroup, False)[0]
                print(target)
                self.active = False
            elif keys.BACK:
                self.active = False
        return target
