import pygame as pg

from config import SCREEN_H, FONT, FONT_SIZE, DARK_ROSE, POWDER_ROSE

class Button(pg.sprite.Sprite):
    '''A general class for buttons. Inherits Pygame's sprite class.

    attr:
        image: a rendered text box
        rect: bounding rectangle for the image
    '''
    def __init__(self, text, size, colour):
        '''Button class constructor.

        args:
            text: str; text to be drawn as the button image
            size: int; font size
            colour: tuple; colour of the text
        '''
        pg.sprite.Sprite.__init__(self)
        self.image = self._create_button(text, size, colour)
        self.rect = self.image.get_rect()

    def _create_button(self, text, size, colour):
        '''Creates a new button.

        args:
            text: str; text to be written
            size: int; font size
            colour: tuple; font colour
        '''
        font = pg.font.Font(FONT, size)
        return font.render(text, False, colour)

class MenuButton(Button):
    '''Button subclass for action buttons in a battle menu.

    attr:
        size: int; font size
        name: str; name of the button action
        text: str; text to be drawn on the button image
        pressed: bool; tells whether the button has been pressed
        passive_img: Surface; button shown when it has not been pressed
        active_img: Surface; button shown when it has been pressed
    '''
    def __init__(self, action, name, text):
        '''MenuButton class constructor.

        args:
            action: str; action associated with the button; can be
                a menu action or skill identifier
            name: str: name of the button action
            text: str: text to be shown on the button
        '''
        self.action = action
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

    def update(self):
        '''Updates the sprite image according to whether the
        button has been pressed.
        '''
        if self.pressed:
            self.image = self._active_img
        else:
            self.image = self._passive_img

class ItemButton(Button):
    '''Button subclass for the item menu buttons on the battle menu.

    attr:
        action: str; item identifier
        size: int; font size
        name: str; item name
        qty: int; item quantity in character's inventory
        text: str; text to be drawn on the button
        pressed: bool; indicator of whether the button has been pressed
        passive_img: Surface: button to be drawn on screen when it is not pressed
        active_img: Surface: button to be drawn on screen when it has been pressed
    '''
    def __init__(self, action, name, qty, character):
        '''ItemButton class constructor.

        args:
            action: str; item identifier
            name: str; item name
            qty: int; item quantity
        '''
        self.action = action
        self._size = FONT_SIZE
        self._name = name
        self._qty = qty
        self._character = character
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
        '''Returns an updated button text.'''
        return f'  {self._name.lower()}{self._qty:2}'

    def update(self):
        '''Updates the sprite image, as well as item quantity if
        an item has been used.
        '''
        prev_qty = self._qty
        self._qty = self._character.get_item_qty(self.action)
        if prev_qty > self._qty:
            self._text = self._update_text()
            self._passive_img = self._create_button(
                self._text, self._size, POWDER_ROSE
            )
            self._active_img = self._create_button(
                self._text, self._size, DARK_ROSE
            )
        if self.pressed:
            if self._qty >= 0:
                self.image = self._active_img
        else:
            self.image = self._passive_img

class DamageText(Button):
    '''A button subclass for displaying damage taken in battle.'''
    def __init__(self, amount, colour, pos):
        '''Class constructor for damage text.

        args:
            amount: str; damage taken/amount healed as string
            colour: tuple; text colour (green for hp heal, red
                for damage, blue for mp heal)
            pos: tuple; character sprite position
        '''
        Button.__init__(self, amount, FONT_SIZE, colour)
        self.rect.center = pos

    def update(self):
        '''Moves the button up and makes it disappear when
        it hits the top of the screen.'''
        self.rect.y -= 1
        if self.rect.y == SCREEN_H // 4:
            self.kill()
