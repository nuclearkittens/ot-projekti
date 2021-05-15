from random import seed

import unittest
import pygame as pg

from config import NATIVE_RESOLUTION
from database.initialise_db import initialise_db
from entities.monster import Monster

class TestMonster(unittest.TestCase):
    def setUp(self):
        initialise_db()
        pg.init()
        pg.display.set_mode(NATIVE_RESOLUTION, pg.HIDDEN)
        self.char = Monster('bob')
        self.char._skills.pop('attack', None)

    def tearDown(self):
        pg.quit()

    def test_set_default_action(self):
        default = self.char._set_default_action()
        self.assertEqual(default, 'test_skill')

    def test_set_default_action_no_zero_cost_skills(self):
        self.char._skills.pop('test_skill', None)
        default = self.char._set_default_action()
        self.assertIsNone(default)

    def test_set_tick_speed(self):
        seed(1)
        tick_speed = self.char.set_tick_speed()
        self.assertEqual(tick_speed, 15)

    def test_make_decision_empty_target_list(self):
        action, target = self.char.make_decision(list())
        self.assertIsNone(action)
        self.assertIsNone(target)

    def test_make_decision_less_than_quarter_hp(self):
        self.char.curr_hp = 20
        action, target = self.char.make_decision([self.char.battlesprite])
        self.assertEqual(
            (action, target), ('test_item1', self.char.battlesprite)
            )

    def test_make_decision_no_items(self):
        self.char.inventory = {}
        self.char.curr_hp = 20
        action, target = self.char.make_decision([self.char.battlesprite])
        self.assertEqual(
            (action, target), ('test_skill', self.char.battlesprite)
            )

    def test_make_decision_choose_skill(self):
        self.char._skills.pop('test_skill', None)
        action, target = self.char.make_decision([self.char.battlesprite])
        self.assertEqual(
            (action, target), ('test_magic', self.char.battlesprite)
        )

    def test_make_decision_not_enough_mp(self):
        self.char._skills.pop('test_skill', None)
        self.char.curr_mp = 0
        action, target = self.char.make_decision([self.char.battlesprite])
        self.assertEqual(
            (action, target), ('test_skill', self.char.battlesprite)
        )

    def test_return_name(self):
        self.assertEqual(self.char.name, 'Bob')
