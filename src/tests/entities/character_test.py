import unittest
import pygame as pg

from config import NATIVE_RESOLUTION
from database.initialise_db import initialise_db
from entities.character import Character

class TestCharacter(unittest.TestCase):
    def setUp(self):
        initialise_db()
        pg.init()
        pg.display.set_mode(NATIVE_RESOLUTION, pg.HIDDEN)
        self.char = Character('bob')

    def tearDown(self):
        pg.quit()

    def test_check_hp_within_limits(self):
        self.char.curr_hp = 50
        self.char.check_hp()
        self.assertEqual(self.char.curr_hp, 50)

    def test_check_hp_too_high(self):
        self.char.curr_hp = 200
        self.char.check_hp()
        self.assertEqual(self.char.curr_hp, self.char._stats.hp)

    def test_check_hp_negative(self):
        self.char.curr_hp = -1
        self.char.check_hp()
        self.assertEqual(self.char.curr_hp, 0)

    def test_char_dies_when_hp_is_zero(self):
        self.char.curr_hp = 0
        self.char.check_hp()
        self.assertFalse(self.char.alive)
