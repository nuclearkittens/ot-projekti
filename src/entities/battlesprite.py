import pygame as pg

from util import load_img
from ui.bar import HPBar, MPBar

class BattleSprite(pg.sprite.Sprite):
    '''Class for handling the character sprite in battle.

    attr:
        update_time: keeps track of animation update time
        anim_list: nested list for animation frames, grouped by action
        action: current animation state; possible values:
            0: idle, 1: attack, 2: hurt, 3: dead
        image: current image
        rect: rectangular area containing the sprite
        bars: hp (and mp) bar(s) associated with the character
    '''
    def __init__(self, character):
        '''Constructor for BattleSprite class.
        Takes associated character object as its argument.
        '''
        pg.sprite.Sprite.__init__(self)
        self._character = character
        self._update_time = pg.time.get_ticks()

        self._anim_list = []
        self._frame_idx = 0
        self._action = 0 # 0: idle, 1: attack, 2: hurt, 3: dead

        self._load_frames()

        self.image = self._anim_list[0][0]
        self.rect = self.image.get_rect()

        self._bars = {}

    def update(self):
        '''Checks the time passed since the last frame update,
        and updates the frame accordingly. Also checks hp and mp
        of the associated character.
        '''
        self._character.check_hp()
        self._character.check_mp()

        anim_cooldown = 250
        self.image = self._anim_list[self._action][self._frame_idx]
        if pg.time.get_ticks() - self._update_time > anim_cooldown:
            self._update_time = pg.time.get_ticks()
            self._frame_idx += 1
        if self._frame_idx >= len(self._anim_list[self._action]):
            if self._action == 3:
                self.kill()
            else:
                self._idle()

        for bar in self._bars.values():
            bar.update()

    def _idle(self):
        '''Resets the sprite animation to idle.'''
        self._action = 0
        self._frame_idx = 0
        self._update_time = pg.time.get_ticks()

    def attack(self):
        '''Changes the sprite animation to attack.'''
        self._action = 1
        self._frame_idx = 0
        self._update_time = pg.time.get_ticks()

    def hurt(self):
        '''Changes the sprite animation to taking damage.'''
        self._action = 2
        self._frame_idx = 0
        self._update_time = pg.time.get_ticks()

    def dead(self):
        '''Changes the sprite animation to dead.'''
        self._action = 3
        self._frame_idx = 0
        self._update_time = pg.time.get_ticks()

    def set_position(self, x, y):
        '''Places the midbottom of the image at the given coordinates.'''
        self.rect.midbottom = (x, y)

    def create_hp_bar(self, w, h):
        '''Creates a new HP bar of given dimensions for the character.'''
        self._bars['hp'] = HPBar(w, h, self._character)

    def create_mp_bar(self, w, h):
        '''Creates a new MP bar of given dimensions for the character.'''
        self._bars['mp'] = MPBar(w, h, self._character)

    def set_bar_position(self, x, y, center):
        '''Sets the position of the HP and MP bars.

        args:
            x: x-coordinate for HP bar
            y: y-coordinate for HP bar
            center: bool
        '''
        for attr, bar in self._bars.items():
            if attr == 'hp':
                if center:
                    bar.rect.center = (x, y)
                else:
                    bar.rect.bottomleft = (x, y)
            elif attr == 'mp':
                bar.rect.topleft = (x, y + bar.rect.h)

    def draw_bars(self, renderer):
        '''Blits the bars on the display.

        args:
            renderer: game renderer object
        '''
        for bar in self._bars.values():
            bar.draw(renderer)

    def _load_frames(self):
        '''Loads the frames for sprite animation.'''
        frames_lst = [
            ['idle1.png', 'idle2.png'],
            ['attack1.png', 'attack2.png', 'attack3.png', 'attack4.png'],
            ['idle1.png', 'hurt.png'],
            ['dead.png']
        ]
        for frames in frames_lst:
            temp = []
            for frame in frames:
                path = f'assets/gfx/sprites/{self._character.id}/{frame}'
                temp.append(load_img(path))
            self._anim_list.append(temp)

    @property
    def character(self):
        '''property: character object'''
        return self._character
