import pygame as pg

from config import SCREEN_W, SCREEN_H
from ui.buttons import BattleMenuButton, ItemButton
from ui.cursors import MenuCursor

class BattleMenu:
    '''A class for battle menus:

    attr:
        gutter: int; gutter between nested menus
        panel_w: int; width of a menu panel
        panel_h: int; height of a menu panel
        menu_type: str; type of the menu (main, skill, magic, item)
        panel: Surface; menu panel surface
        rect: Rect; bounding rectangle of the menu panel
        buttons: sprite Group; buttons associated with the menu
        cursor_pos: lst; list of coordinate tuples for the cursor
        cursor: MenuCursor object or None; cursor to move through the menu;
            None if the menu has no buttons
        cursor_current: tuple; current position of the cursor
    '''
    def __init__(self, menu_type, options, character=None):
        '''BattleMenu class constructor.

        args:
            menu_type: str; type of the menu (main, skill, magic or item)
            options: lst; options to choose from; used to create the menu buttons
            character: Character object; needed for creating item buttons
        '''
        self._gutter = SCREEN_W // 64
        self._panel_w = SCREEN_W // 3 - self._gutter
        self._panel_h = SCREEN_H // 4

        self.menu_type = menu_type
        self.active = False

        self._panel = pg.Surface((self._panel_w, self._panel_h))
        self.rect = self._panel.get_rect()

        self._calc_position()

        self._buttons = pg.sprite.Group()
        self._cursor_pos = []
        self._create_buttons(options, character)
        if self._cursor_pos:
            self._cursor = MenuCursor()
            self._cursor_current = self._cursor_pos[0]
        else:
            self._cursor = False
            self._cursor_current = None

    def draw(self, renderer):
        '''Draws the menu on screen.

        args:
            renderer: Renderer object
        '''
        renderer.fill(self._panel)
        renderer.blit(self._panel, self.rect)
        renderer.draw_sprites(self._buttons)
        if self._cursor:
            renderer.blit(self._cursor.image, self._cursor.rect)

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
        def move_cursor(keys):
            '''Moves the menu cursor according to player input, and updates its
            position.

            args:
                keys: Keys object
            '''
            if self._cursor:
                if keys.DOWN:
                    for idx, pos in enumerate(self._cursor_pos):
                        # print(idx, pos)
                        if self._cursor_current == pos:
                            if idx == len(self._cursor_pos)-1:
                                self._cursor_current = self._cursor_pos[0]
                            else:
                                self._cursor_current = self._cursor_pos[idx+1]
                            break
                elif keys.UP:
                    for idx, pos in enumerate(self._cursor_pos):
                        if self._cursor_current == pos:
                            if idx == 0:
                                self._cursor_current = self._cursor_pos[-1]
                            else:
                                self._cursor_current = self._cursor_pos[idx-1]
                            break
                self._cursor.rect.bottomleft = self._cursor_current

        info = None
        action = None
        if self.active:
            move_cursor(keys)
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

    def update_buttons(self):
        '''Updates the menu's buttons.'''
        self._buttons.update()

    def reset_cursor(self):
        '''Resets cursor to its default position (i.e. topmost menu button).'''
        self._cursor.rect.bottomleft = self._cursor_pos[0]
        self._cursor_current = self._cursor_pos[0]

    def reset_buttons(self):
        '''Resets buttons to unpressed status.'''
        for button in self._buttons:
            button.pressed = False

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

    def _create_buttons(self, options, character):
        '''Creates buttons for the menu.

        args:
            options: lst; list of tuples specifying the buttons'
                attributes
        '''
        x = self.rect.x + self._gutter
        y = self.rect.y
        for option in options:
            if self.menu_type == 'main':
                new_button = BattleMenuButton(option, option, option)
            else:
                action = option[0]
                name = option[1]
                text = f'{option[1]} {option[2]:2}'
                if self.menu_type == 'item':
                    qty = option[2]
                    new_button = ItemButton(action, name, qty, character)
                else:
                    new_button = BattleMenuButton(action, name, text)
            new_button.rect.topleft = (x, y)
            self._cursor_pos.append((x, y + (self._panel_h // 4)))
            self._buttons.add(new_button)
            y += self._panel_h // 4
