import unittest
import pygame as pg

from config import NATIVE_RESOLUTION
from database.initialise_db import initialise_db
from database.db_util import load_inventory
from entities.character import Character

class TestCharacter(unittest.TestCase):
    def setUp(self):
        initialise_db()
        pg.init()
        pg.display.set_mode(NATIVE_RESOLUTION, pg.HIDDEN)
        self.char = Character('bob')
        self.char.inventory = load_inventory('bob')

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

    def test_check_mp_within_limits(self):
        self.char.curr_mp = 5
        self.char.check_mp()
        self.assertEqual(self.char.curr_mp, 5)

    def test_check_mp_too_high(self):
        self.char.curr_mp = 20
        self.char.check_mp()
        self.assertEqual(self.char.curr_mp, self.char._stats.mp)

    def test_use_item_in_inv(self):
        test_info = self.char.use_item('test_item1', self.char)
        expected = [('hp', 20), ('mp', 5)]
        self.assertEqual(test_info, expected)

    def test_use_item_not_enough_in_inv(self):
        self.char.use_item('test_item1', self.char)
        test_info = self.char.use_item('test_item1', self.char)
        expected = 'Not enough TEST ITEM 1s in inventory!'
        self.assertEqual(test_info, expected)

    def test_use_item_not_in_inv(self):
        test_info = self.char.use_item('slp_tblt', self.char)
        self.assertIsInstance(test_info, ValueError)

    def test_use_skill_info_is_ok(self):
        target = Character('bob')
        test_info = self.char.use_skill('test_skill', target)
        self.assertEqual(len(test_info), 2)

    def test_use_skill_battlesprites_ok(self):
        target = Character('bob')
        self.char.use_skill('test_skill', target)
        actual = (self.char.battlesprite._action, target.battlesprite._action)
        self.assertEqual(actual, (1, 2))

    def test_use_skill_uses_mp(self):
        target = Character('bob')
        self.char.use_skill('test_magic', target)
        self.assertLess(self.char.curr_mp, self.char._stats.mp)

    def test_use_skill_not_enough_mp(self):
        self.char.curr_mp = 0
        target = Character('bob')
        test_info = self.char.use_skill('test_magic', target)
        self.assertEqual(test_info, 'Not enough MP!')

    def test_use_skill_not_in_char_skills(self):
        target = Character('bob')
        test_info = self.char.use_skill('energy_blst', target)
        self.assertEqual(test_info, 'bob does not know skill energy_blst!')

    def test_get_item_qty_in_inv(self):
        test_qty = self.char.get_item_qty('test_item1')
        self.assertEqual(test_qty, 1)

    def test_get_item_qty_not_in_inv(self):
        test_qty = self.char.get_item_qty('slp_tblt')
        self.assertEqual(test_qty, 'no item slp_tblt in inventory!')

    def test_get_skill_cost_not_in_char_skills(self):
        test_cost = self.char.get_skill_cost('energy_blst')
        self.assertEqual(test_cost, 'bob does not know skill energy_blst!')

    def test_get_skill_cost(self):
        test_cost = self.char.get_skill_cost('test_skill')
        self.assertEqual(test_cost, 0)

    def test_propeties(self):
        test_properties = [
            self.char.id, self.char.max_hp, self.char.max_mp,
            self.char.atk, self.char.defs, self.char.mag, self.char.mdef
        ]
        expected = ['bob', 100, 10, 10, 10, 5, 5]
        self.assertEqual(test_properties, expected)

    def test_res(self):
        expected = {
            'physical': 1.0, 'fire': 0.0, 'ice': 1.5,
            'lightning': 1.0, 'wind': 1.0, 'light': 0.5, 'dark': -1.0
        }
        self.assertEqual(self.char.res, expected)

    def test_skills(self):
        self.assertIsInstance(self.char.skills, dict)

    def test_inventory(self):
        self.assertIsInstance(self.char.inventory, dict)

    def test_inventory_setter(self):
        self.char.inventory = {}
        self.assertFalse(self.char.inventory)
