import pygame as pg

from config import SCREEN_W, SCREEN_H
from ui.buttons import BattleMenuButton, ItemButton, MenuCursor

class BattleMenu:
    def __init__(self, menu_type, options):
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
        self._create_buttons(options)
        if self._cursor_pos:
            self._cursor = MenuCursor()
            self._cursor_current = self._cursor_pos[0]
        else:
            self._cursor = False
            self._cursor_current = None

    def _calc_position(self):
        if self.menu_type == 'main':
            n = 1
        else:
            n = 2
        x = (n-1) * self._panel_w + n * self._gutter
        y = SCREEN_H - self._panel_h - self._gutter
        self.rect.topleft = (x, y)

    def draw(self, renderer):
        renderer.fill(self._panel)
        renderer.blit(self._panel, self.rect)
        renderer.draw_sprites(self._buttons)
        if self._cursor:
            renderer.blit(self._cursor.image, self._cursor.rect)

    def _create_buttons(self, options):
        x = self.rect.x + self._gutter
        y = self.rect.y
        for option in options:
            if self.menu_type == 'main':
                new_button = BattleMenuButton(option, option)
            else:
                name = option[0]
                text = f'{option[0]} {option[1]:2}'
                # name, attr = option[0], option[1]
                if self.menu_type == 'item':
                    qty = option[1]
                    new_button = ItemButton(name, qty)
                else:
                    new_button = BattleMenuButton(name, text)
            new_button.rect.topleft = (x, y)
            self._cursor_pos.append((x, y + (self._panel_h // 4)))
            self._buttons.add(new_button)
            y += self._panel_h // 4

    def _move_cursor(self, keys):
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

    def update(self, keys):
        action = None
        if self.active:
            self._move_cursor(keys)
            if keys.SELECT:
                button = pg.sprite.spritecollide(self._cursor, self._buttons, False)[0]
                button.pressed = True
                self.active = False
                print(button.action)
                action = button.action
            elif keys.BACK:
                self.active = False
                self.reset_buttons()
                action = 'main'
        self._buttons.update()
        return action

    def reset_cursor(self):
        self._cursor.rect.bottomleft = self._cursor_pos[0]
        self._cursor_current = self._cursor_pos[0]

    def reset_buttons(self):
        for button in self._buttons:
            button.pressed = False
