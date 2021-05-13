import unittest
import pygame as pg

from config import HP_GREEN, HP_YELLOW, HP_RED
from entities.bar import Bar, HPBar, MPBar, InfoBar

width = 100
height = 20

class StubCharacter:
    def __init__(self):
        self.max_hp = 100
        self.curr_hp = 100
        self.max_mp = 10
        self.curr_mp = 10

class TestBar(unittest.TestCase):
    def setUp(self):
        self.test_bar = Bar(width, height)

    def test_rect_is_right_size(self):
        expected = pg.Rect(0, 0, width, height)
        self.assertEqual(self.test_bar.rect, expected)

class TestHPBar(unittest.TestCase):
    def setUp(self):
        self.test_char = StubCharacter()
        self.test_bar = HPBar(width, height, self.test_char)

    def test_update_full_hp(self):
        self.test_bar.update()
        actual = (self.test_bar._colour, self.test_bar._top.get_width())
        expected = (HP_GREEN, 100)
        self.assertEqual(actual, expected)

    def test_update_more_than_half_hp(self):
        self.test_char.curr_hp = 70
        self.test_bar.update()
        actual = (self.test_bar._colour, self.test_bar._top.get_width())
        expected = (HP_GREEN, 70)
        self.assertEqual(actual, expected)

    def test_update_less_than_half_hp(self):
        self.test_char.curr_hp = 40
        self.test_bar.update()
        actual = (self.test_bar._colour, self.test_bar._top.get_width())
        expected = (HP_YELLOW, 40)
        self.assertEqual(actual, expected)

    def test_update_less_than_fifth_hp(self):
        self.test_char.curr_hp = 10
        self.test_bar.update()
        actual = (self.test_bar._colour, self.test_bar._top.get_width())
        expected = (HP_RED, 10)
        self.assertEqual(actual, expected)

    def test_update_negative_hp(self):
        self.test_char.curr_hp = -10
        self.test_bar.update()
        actual = (self.test_bar._colour, self.test_bar._top.get_width())
        expected = (HP_RED, 0)
        self.assertEqual(actual, expected)

class TestMPBar(unittest.TestCase):
    def setUp(self):
        self.test_char = StubCharacter()
        self.test_bar = MPBar(width, height, self.test_char)

    def test_update(self):
        self.test_char.curr_mp = 5
        self.test_bar.update()
        self.assertEqual(self.test_bar._top.get_width(), 50)

class TestInfoBar(unittest.TestCase):
    def setUp(self):
        pg.init()
        self.info = InfoBar()

    def tearDown(self):
        pg.quit()

    def test_update_no_scaling(self):
        self.info.update('STNAAV')
        self.assertLessEqual(self.info._top.get_width(), self.info._w)

    def test_update_scaling(self):
        long_str = '''Sleeping Tablets (Now as a Vinegar!) - with
        CHERRY flavour! LIMITED STOCK! Get yours TODAY'''
        self.info.update(long_str)
        self.assertEqual(self.info._top.get_width(), self.info._w)
