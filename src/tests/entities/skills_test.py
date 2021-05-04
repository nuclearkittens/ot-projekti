import unittest
import sqlite3
from collections import namedtuple
from random import seed, random, uniform

from entities.skills import Skill

def populate_mock_db(conn):
    queries = '''CREATE TABLE Skills (id TEXT PRIMARY KEY, category TEXT,
        subcategory TEXT, name TEXT, descr TEXT, element TEXT, hits INTEGER,
        mp_cost INTEGER, multiplier REAL, crit_rate REAL);
        INSERT INTO Skills (id, category, subcategory, name, descr,
        element, hits, mp_cost, multiplier, crit_rate)
        VALUES ("test_skill", "skills", "physical", "Test Skill", "A skill for testing",
        "physical", 2, 0, 1.0, 1.0);
        INSERT INTO Skills (id, category, subcategory, name, descr,
        element, hits, mp_cost, multiplier, crit_rate)
        VALUES ("test_magic", "magic", "blk", "Test Spell", "A skill for testing",
        "fire", 1, 5, 1.2, 0.5);
        INSERT INTO Skills (id, category, subcategory, name, descr,
        element, hits, mp_cost, multiplier, crit_rate)
        VALUES ("test_other", "other", "other", "Unspecified Skill", "A skill for testing",
        "dark", 0, 0, 0.0, 0.0);
        '''
    cur = conn.cursor()
    for query in queries.split(';'):
        cur.execute(query)
        conn.commit()

Info = namedtuple('Info', ['name', 'category', 'subcategory', 'description'])
Attributes = namedtuple('Attributes', [
            'element', 'hits', 'mp_cost', 'multiplier', 'crit_rate'])

class StubCharacter:
    def __init__(self):
        self.res = {
            'physical': 1.0, 'fire': 1.5, 'ice': 0.0,
            'lightning': 0.0, 'wind': 0.0, 'light': 0.0,
            'dark': -1.0
        }
        self.atk = 10
        self.defs = 10
        self.mag = 10
        self.mdef = 10
        self.curr_hp = 100
        self.curr_mp = 10

class TestSkill(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        populate_mock_db(self.conn)
        # seed(621) #random: 0.31429...; uniform(0.8, 1.2): 1.04948...

    def test_load_attributes(self):
        test_skill = Skill('test_other', self.conn)
        expected = Attributes('dark', 0, 0, 0.0, 0.0)
        self.assertEqual(test_skill._attr, expected)
        self.conn.close()

    def test_load_info(self):
        test_skill = Skill('test_other', self.conn)
        expected = Info('Unspecified Skill', 'other', 'other', 'A skill for testing')
        self.assertEqual(test_skill._info, expected)
        self.conn.close()

    def test_is_critical(self):
        test_skill = Skill('test_skill', self.conn)
        self.assertTrue(test_skill._is_critical())
        self.conn.close()

    def test_is_not_critical(self):
        test_skill = Skill('test_other', self.conn)
        self.assertFalse(test_skill._is_critical())
        self.conn.close()

    def test_damage_calculation_normal(self):
        test_skill = Skill('test_other', self.conn)
        atk, defs = 10, 10
        mult = 1.0
        expected_lower = int(0.8 * mult * (atk - (defs / 2)))
        expected_upper = int(1.2 * mult * (atk - (defs / 2)))
        actual = test_skill._calc_dmg(atk, defs, mult)
        self.assertTrue(expected_lower <= actual <= expected_upper)
        self.conn.close()

    def test_damage_calculation_critical(self):
        test_skill = Skill('test_skill', self.conn)
        atk, defs = 10, 10
        mult = 1.0
        expected_lower = int(0.8 * ((1.5 * mult) * (atk - (defs / 2))))
        expected_upper = int(1.2 * ((1.5 * mult) * (atk - (defs / 2))))
        actual = test_skill._calc_dmg(atk, defs, mult)
        self.assertTrue(expected_lower <= actual <= expected_upper)
        self.conn.close()

    def test_use_skill_physical(self):
        test_skill = Skill('test_skill', self.conn)
        user = StubCharacter()
        target = StubCharacter()
        max_hp = target.curr_hp
        test_skill.use(user, target)
        self.assertLess(target.curr_hp, max_hp)
        self.conn.close()

    def test_use_skill_magical(self):
        test_skill = Skill('test_magic', self.conn)
        user = StubCharacter()
        target = StubCharacter()
        max_hp = target.curr_hp
        test_skill.use(user, target)
        self.assertLess(target.curr_hp, max_hp)
        self.conn.close()

    def test_use_skill_other(self):
        test_skill = Skill('test_other', self.conn)
        user = StubCharacter()
        target = StubCharacter()
        max_hp = target.curr_hp
        test_skill.use(user, target)
        self.assertEqual(target.curr_hp, max_hp)
        self.conn.close()

    def test_use_skill_atk_lesser_than_defs(self):
        test_skill = Skill('test_magic', self.conn)
        user = StubCharacter()
        target = StubCharacter()
        user.mag = 4
        expected = target.curr_hp - 1
        test_skill.use(user, target)
        self.assertEqual(target.curr_hp, expected)
        self.conn.close()

    def test_property_mp_cost(self):
        test_skill = Skill('test_other', self.conn)
        self.assertEqual(test_skill.mp_cost, 0)
        self.conn.close()

    def test_property_name(self):
        test_skill = Skill('test_other', self.conn)
        self.assertEqual(test_skill.name, 'Unspecified Skill')
        self.conn.close()

    def test_property_category(self):
        test_skill = Skill('test_other', self.conn)
        self.assertEqual(test_skill.category, 'other')
        self.conn.close()
