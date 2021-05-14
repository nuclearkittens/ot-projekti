import unittest

from database.initialise_db import initialise_db
from entities.skills import Skill

class StubCharacter:
    def __init__(self):
        self.curr_hp = 100
        self.atk = 10
        self.defs = 5
        self.mag = 10
        self.mdef = 5
        self.res = {
            'physical': 1.0,
            'fire': 1.0,
            'ice': 1.0,
            'lightning': 1.0,
            'wind': 1.0,
            'light': 1.0,
            'dark': 1.0
        }

class TestSkill(unittest.TestCase):
    def setUp(self):
        initialise_db()

    def test_is_critical(self):
        test_skill = Skill('test_skill')
        self.assertTrue(test_skill._is_critical())

    def test_is_not_critical(self):
        test_skill = Skill('test_other')
        self.assertFalse(test_skill._is_critical())

    def test_calc_dmg_critical(self):
        test_skill = Skill('test_skill')
        atk, defs, mult = 2, 2, 1
        test_dmg = test_skill._calc_dmg(atk, defs, mult)
        self.assertEqual(test_dmg, 1)

    def test_calc_dmg_not_critical(self):
        test_skill = Skill('test_other')
        atk, defs, mult = 20, 20, 1
        test_dmg = test_skill._calc_dmg(atk, defs, mult)
        self.assertTrue(8 <= test_dmg <= 12)

    def test_use_skill(self):
        test_skill = Skill('test_skill')
        user = StubCharacter()
        target = StubCharacter()
        info = test_skill.use(user, target)
        self.assertEqual(len(info), 2)

    def test_use_magic(self):
        test_skill = Skill('test_magic')
        user = StubCharacter()
        target = StubCharacter()
        info = test_skill.use(user, target)
        self.assertEqual(len(info), 1)

    def test_use_other(self):
        test_skill = Skill('test_other')
        user = StubCharacter()
        target = StubCharacter()
        info = test_skill.use(user, target)
        self.assertFalse(info)

    def test_atk_lesser_than_defs(self):
        test_skill = Skill('test_skill')
        user = StubCharacter()
        user.atk = 1
        target = StubCharacter()
        test_skill.use(user, target)
        self.assertEqual(target.curr_hp, 98)

    def test_returns_mp_cost(self):
        test_skill = Skill('test_other')
        self.assertEqual(test_skill.mp_cost, 0)

    def test_returns_name(self):
        test_skill = Skill('test_other')
        self.assertEqual(test_skill.name, 'Unspecified Skill')

    def test_returns_category(self):
        test_skill = Skill('test_other')
        self.assertEqual(test_skill.category, 'other')

    def test_returns_description(self):
        test_skill = Skill('test_other')
        self.assertEqual(test_skill.description, 'A skill for testing')
