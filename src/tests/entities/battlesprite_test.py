import unittest
import pygame as pg

from config import NATIVE_RESOLUTION
from entities.battlesprite import BattleSprite

class StubCharacter:
    def __init__(self, char_id):
        self.id = char_id
        self.alive = True

        self.curr_hp = 100
        self.max_hp = 100

        self.curr_mp = 10
        self.max_mp = 10

    def check_hp(self):
        pass

    def check_mp(self):
        pass

class TestBattleSprite(unittest.TestCase):
    def setUp(self):
        pg.init()
        pg.display.set_mode(NATIVE_RESOLUTION, pg.HIDDEN)
        self.char = StubCharacter('bob')
        self.sprite = BattleSprite(self.char)

    def tearDown(self):
        pg.quit()

    def test_update(self):
        self.sprite.update()
        max_idx = len(self.sprite._anim_list[self.sprite._action])
        self.assertLessEqual(self.sprite._frame_idx, max_idx)
        self.assertGreaterEqual(self.sprite._frame_idx, 0)

    def test_update_reset_to_idle(self):
        self.sprite._action = 1
        self.sprite._frame_idx = 4
        self.sprite.update()
        actual = (self.sprite._action, self.sprite._frame_idx)
        self.assertEqual(actual, (0, 0))

    def test_attack(self):
        self.sprite.attack()
        actual = (self.sprite._action, self.sprite._frame_idx)
        self.assertEqual(actual, (1, 0))

    def test_hurt(self):
        self.sprite.hurt()
        actual = (self.sprite._action, self.sprite._frame_idx)
        self.assertEqual(actual, (2, 0))

    def test_dead(self):
        test_group = pg.sprite.Group()
        test_group.add(self.sprite)
        self.sprite.dead()
        self.assertFalse(bool(test_group))

    def test_set_position(self):
        x, y = 10, 10
        self.sprite.set_position(x, y)
        self.assertEqual(self.sprite.rect.midbottom, (x, y))

    def test_create_hp_bar(self):
        self.sprite.create_hp_bar(100, 10)
        self.assertIsNotNone(self.sprite._bars['hp'])

    def test_create_mp_bar(self):
        self.sprite.create_mp_bar(100, 10)
        self.assertIsNotNone(self.sprite._bars['mp'])

    def test_set_bar_position_hp(self):
        self.sprite.create_hp_bar(100, 10)
        x, y = 100, 100
        self.sprite.set_bar_position(x, y, False)
        actual = self.sprite._bars['hp'].rect.bottomleft
        self.assertEqual(actual, (x, y))

    def test_set_bar_position_hp_center(self):
        self.sprite.create_hp_bar(100, 10)
        x, y = 100, 100
        self.sprite.set_bar_position(x, y, True)
        actual = self.sprite._bars['hp'].rect.center
        self.assertEqual(actual, (x, y))

    def test_set_bar_position_mp(self):
        self.sprite.create_mp_bar(100, 10)
        x, y = 100, 100
        self.sprite.set_bar_position(x, y, False)
        actual = self.sprite._bars['mp'].rect.topleft
        expected = (x, y + 10)
        self.assertEqual(actual, expected)

    def test_all_actions_in_anim_list(self):
        self.assertEqual(len(self.sprite._anim_list), 4)

    def test_all_frames_in_anim_list(self):
        frames = len([frame for action in self.sprite._anim_list for frame in action])
        self.assertEqual(frames, 9)

    def test_returns_character(self):
        self.assertEqual(self.sprite.character, self.char)
