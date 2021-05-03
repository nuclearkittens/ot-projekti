import pygame as pg

from config import (
    FONT, FONT_SIZE, MENU_CURSOR, TARGET_CURSOR,
    CURSOR_SIZE, DARK_ROSE, POWDER_ROSE
)

# TO DO: move cursors to their own class

class Button(pg.sprite.Sprite):
    def __init__(self, text, size, colour):
        pg.sprite.Sprite.__init__(self)
        self.image = self._create_button(text, size, colour)
        self.rect = self.image.get_rect()

    def _create_button(self, text, size, colour):
        font = pg.font.Font(FONT, size)
        return font.render(text, False, colour)

class MenuCursor(Button):
    def __init__(self):
        Button.__init__(self, MENU_CURSOR, CURSOR_SIZE, POWDER_ROSE)

class TargetCursor(Button):
    def __init__(self):
        Button.__init__(self, TARGET_CURSOR, CURSOR_SIZE, POWDER_ROSE)

        self.pos = []
        self.current_pos = None
        self.active = False

    def _move_cursor(self, keys):
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

class BattleMenuButton(Button):
    def __init__(self, name, text):
        self._size = FONT_SIZE
        self._name = name
        self._text = f'  {text}'
        Button.__init__(self, self._text, self._size, POWDER_ROSE)

        self.pressed = False
        self._passive_img = self._create_button(
            self._text, self._size, POWDER_ROSE
        )
        self._active_img = self._create_button(
            self._text, self._size, DARK_ROSE
        )

    @property
    def action(self):
        return self._name

    def update(self):
        if self.pressed:
            self.image = self._active_img
        else:
            self.image = self._passive_img

class ItemButton(Button):
    def __init__(self, name, qty):
        self._size = FONT_SIZE
        self._name = name.lower()
        self._qty = qty
        self._text = self._update_text()
        Button.__init__(self, self._text, self._size, POWDER_ROSE)

        self.pressed = False
        self._passive_img = self._create_button(
            self._text, self._size, POWDER_ROSE
        )
        self._active_img = self._create_button(
            self._text, self._size, DARK_ROSE
        )

    def _update_text(self):
        return f'  {self._name}{self._qty:2}'

    def update(self):
        if self.pressed:
            if self._qty > 0:
                self._qty -= 1
                self._text = self._update_text()
                self._passive_img = self._create_button(
                    self._text, self._size, POWDER_ROSE
                )
                self._active_img = self._create_button(
                    self._text, self._size, DARK_ROSE
                )
            self.image = self._active_img
        else:
            self.image = self._passive_img

    @property
    def action(self):
        return self._name
