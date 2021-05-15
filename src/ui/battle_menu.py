import pygame as pg

from config import SCREEN_W, SCREEN_H
from ui.buttons import MenuButton, ItemButton
from ui.cursors import MenuCursor
from ui.menu import Menu

class BattleMenu(Menu):
    '''A class for battle menus; subclass of Menu.

    attr:
        menu_type: str; type of the menu (main, skill, magic, item)

    '''
    def __init__(self, menu_type, options, char=None):
        '''BattleMenu class constructor.

        args:
            menu_type: str; type of the menu (main, skill, magic or item)
            options: lst; options to choose from; used to create the menu buttons
            char: Character object; needed for creating item buttons
        '''
        gutter = SCREEN_W // 64
        w = SCREEN_W // 3 - gutter
        h = SCREEN_H // 4

        self.menu_type = menu_type

        Menu.__init__(self, options, gutter, w, h)

        self._cursor_pos = []
        self._create_bm_buttons(options, char)
        if self._cursor_pos:
            self._cursor = MenuCursor()
            self._cursor_current = self._cursor_pos[0]
        else:
            self._cursor = False
            self._cursor_current = None

    def update(self, keys):
        '''Updates the state of the menu. If menu is active, checks if
        a menu button has been pressed using sprite collision.

        args:
            keys: Keys object

        return:
            info: str; current position of cursor to tell what to update on info panel
            action: str or None; returns an action if one is chosen,
                otherwise returns None
        '''
        info = None
        action = None
        if self.active:
            self._move_cursor(keys)
            try:
                pos = pg.sprite.spritecollide(self._cursor, self._buttons, False)[0]
                info = pos.action
            except AttributeError:
                info = None
            if keys.SELECT:
                button = pg.sprite.spritecollide(self._cursor, self._buttons, False)[0]
                button.pressed = True
                self.active = False
                action = button.action
            elif keys.BACK:
                self.active = False
                self.reset_buttons()
                action = 'main'
            self.update_buttons()
        return info, action

    def _calc_position(self):
        '''Calculates the position of the menu panel depending on
        the menu type.
        '''
        if self.menu_type == 'main':
            n = 1
        else:
            n = 2
        x = (n-1) * self._panel_w + n * self._gutter
        y = SCREEN_H - self._panel_h - self._gutter
        self.rect.topleft = (x, y)

    def _create_bm_buttons(self, options, char):
        '''Creates buttons for the menu.

        args:
            options: lst; list of tuples specifying the buttons'
                attributes
            char: Character object (needed for
                creating item buttons)
        '''
        self._buttons.empty()
        x = self.rect.x + self._gutter
        y = self.rect.y
        for option in options:
            if self.menu_type == 'main':
                new_button = MenuButton(option, option, option)
            else:
                action = option[0]
                name = option[1]
                text = f'{option[1]} {option[2]:2}'
                if self.menu_type == 'item':
                    qty = option[2]
                    new_button = ItemButton(action, name, qty, char)
                else:
                    new_button = MenuButton(action, name, text)
            new_button.rect.topleft = (x, y)
            self._cursor_pos.append((x, y + (self._panel_h // 4)))
            self._buttons.add(new_button)
            y += self._panel_h // 4
