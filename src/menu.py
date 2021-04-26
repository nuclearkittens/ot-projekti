import pygame as pg

from config import SCREEN_W, SCREEN_H, CURSOR_SIZE, FONT_SIZE, DARK_PURPLE, POWDER_ROSE
from buttons import Cursor, MenuButton

class Menu:
    def __init__(self, name, renderer, keys,
                 w, h, bg_colour,
                 parent, options, actions,
                 margin, gutter, x=0, y=0,
                 cursor_size=CURSOR_SIZE, cursor_colour=POWDER_ROSE
                ):
        self._renderer = renderer
        self._keys = keys

        self.name = name

        self.base = pg.Surface((w, h))
        self.rect = self.base.get_rect()
        self.rect.topleft = (x, y)
        self.margin = margin
        self.gutter = gutter
        self.bg_colour = bg_colour

        self.active = False
        self.parent = parent
        self.options = options
        self.actions = actions
        self.state = self.actions[0]

        self.buttons = pg.sprite.Group()
        self.cursor_pos = []
        self.cursor = Cursor(cursor_size, cursor_colour)
        self._create_buttons()

    def _create_buttons(self):
        for option in self.options:
            new_button = MenuButton(option, option, FONT_SIZE, POWDER_ROSE)
            self.buttons.add(new_button)
        self._calc_button_placement()

    def _calc_button_placement(self):
        area_h = self.rect.h
        qty = len(self.options)
        x_cursor = self.rect.x + self.margin
        x_button = x_cursor + self.cursor.rect.w + self.gutter
        y = area_h // qty
        for option in self.options:
            for button in self.buttons.sprites():
                if option == button.name:
                    button.set_position(x_button, y)
                    self.cursor_pos.append((x_cursor, y))
                    y += y

    def _move_cursor(self):
        n = len(self.options)
        if n > 1:
            if self._keys.DOWN:
                for i in range(n):
                    if self.state == self.actions[i]:
                        if i == n-1:
                            self.state = self.actions[0]
                            self.cursor.set_position(self.cursor_pos[0][0], self.cursor_pos[0][1])
                        else:
                            self.state = self.actions[i+1]
                            self.cursor.set_position(self.cursor_pos[i+1][0], self.cursor_pos[i+1][1])
                        break
            if self._keys.UP:
                for i in range(n):
                    if self.state == self.actions[i]:
                        if i == 0:
                            self.state = self.actions[-1]
                            self.cursor.set_position(self.cursor_pos[-1][0], self.cursor_pos[-1][1])
                        else:
                            self.state = self.actions[i-1]
                            self.cursor.set_position(self.cursor_pos[i-1][0], self.cursor_pos[i-1][1])
                        break

    def update(self):
        self._move_cursor()
        action = self._check_input()
        self.draw_menu()
        self._keys.reset_keys()
        return action

    def draw_menu(self):
        self.base.fill(self.bg_colour)
        self.buttons.draw(self.base)
        self._renderer.draw_cursor(self.cursor, self.base)
        self._renderer.blit(self.base, self.rect)

    def _check_input(self):
        return self.name

class BattleMenu(Menu):
    def __init__(self, name, owners, parent, renderer, keys, options, actions, x, y):
        w = SCREEN_W // 4
        h = SCREEN_H // 4
        bg_colour = DARK_PURPLE
        margin = int(0.1 * w)
        gutter = margin // 2
        Menu.__init__(
            self, name, renderer, keys,
            w, h, bg_colour,
            parent, options, actions,
            margin, gutter, x, y
            )
        self.owners = owners

    def _check_input(self):
        if self._keys.SELECT:
            return self.state
        elif self._keys.LEFT or self._keys.BACK:
            return self.parent
        return self.name
