from random import seed

import unittest
import pygame as pg

from config import NATIVE_RESOLUTION
from database.initialise_db import initialise_db
from entities.partymember import PartyMember

class TestMonster(unittest.TestCase):
    def setUp(self):
        initialise_db()
        pg.init()
        pg.display.set_mode(NATIVE_RESOLUTION, pg.HIDDEN)
        self.char = PartyMember('bob')

    def tearDown(self):
        pg.quit()

    def test_set_tick_speed(self):
        seed(1)
        tick_speed = self.char.set_tick_speed()
        self.assertEqual(tick_speed, 15)

    def test_add_item_in_inv(self):
        self.char.add_item('test_item1')
        self.char.add_item('test_item1')
        qty = self.char.get_item_qty('test_item1')
        self.assertEqual(qty, 2)

    def test_add_item_not_in_inv(self):
        self.char.add_item('test_item2', 2)
        self.assertTrue('test_item2' in self.char._inventory)

    def test_return_name(self):
        self.assertEqual(self.char.name, 'Bob')
