import pygame as pg

from ui.buttons import MenuButton
from ui.cursors import MenuCursor

class Menu:
    '''A class for menus.

    attr:
        gutter: int; gutter between nested menus
        panel_w: int; width of a menu panel
        panel_h: int; height of a menu panel
        panel: Surface; menu panel surface
        rect: Rect; bounding rectangle of the menu panel
        buttons: sprite Group; buttons associated with the menu
        cursor_pos: lst; list of coordinate tuples for the cursor
        cursor: MenuCursor object or None; cursor to move through the menu;
            None if the menu has no buttons
        cursor_current: tuple; current position of the cursor
    '''
    def __init__(self, options, gutter, w, h, x=0, y=0):
        '''Menu class constructor.

        args:
            options: lst options to choose from; used to create the menu buttons
            gutter: int; gutter between nested menus
            w: int; width of a menu panel
            h: int; height of a menu panel
            x, y: int; coordinates for the first option
        '''
        self._gutter = gutter
        self._panel_w = w
        self._panel_h = h

        self.active = False

        self._panel = pg.Surface((self._panel_w, self._panel_h))
        self.rect = self._panel.get_rect()

        self._calc_position()

        self._buttons = pg.sprite.Group()
        self._cursor_pos = []
        self._create_buttons(options, (x, y))
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
            action: str or None; returns an action if one is chosen,
                otherwise returns None
        '''
        action = None
        if self.active:
            self._move_cursor(keys)
            if keys.SELECT:
                button = pg.sprite.spritecollide(self._cursor, self._buttons, False)[0]
                button.pressed = True
                self.active = False
                action = button.action
            self.update_buttons()
        return action

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
        '''Calculates the position of the menu panel.'''
        self.rect.topleft = (self._gutter, self._gutter)

    def _create_buttons(self, options, coord):
        '''Creates buttons for the menu.

        args:
            options: lst; list of tuples specifying the buttons'
                attributes
            coord: tuple; tuple of a coordinate pair.
        '''
        n = len(options)
        x = self.rect.x if coord[0] == 0 else coord[0]
        y = self.rect.y if coord[1] == 0 else coord[1]
        for option in options:
            new_button = MenuButton(option[0], option[1], option[2])
            new_button.rect.center = (x, y)
            self._cursor_pos.append((x, y))
            self._buttons.add(new_button)
            y += self._panel_h // n

    def _move_cursor(self, keys):
        '''Moves the menu cursor according to player input, and updates its
        position.

        args:
            keys: Keys object
        '''
        if self._cursor:
            if keys.DOWN:
                for idx, pos in enumerate(self._cursor_pos):
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
