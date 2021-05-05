import unittest
import sqlite3
from collections import namedtuple

from config import DB_TEST_SCRIPT
from entities.character import Character

Stats = namedtuple('Stats', ['hp', 'mp', 'atk', 'defs', 'mag', 'mdef', 'agi'])
Res = namedtuple('Res', ['physical', 'fire', 'ice', 'lightning', 'wind', 'light', 'dark'])

def populate_mock_db(conn):
    cur = conn.cursor()
    sql_file = open(DB_TEST_SCRIPT, 'r')
    data = sql_file.read()
    sql_file.close()
    queries = data.split(';')
    for query in queries:
        try:
            cur.execute(query)
        except sqlite3.OperationalError:
            print(f'query "{query}" skipped')


class TestCharacter(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        populate_mock_db(self.conn)
        self.test_char = Character('bob', self.conn)

    def test_load_stats(self):
        expected = Stats(100, 10, 10, 10, 5, 5, 20)
        actual = self.test_char._load_stats()
        self.assertEqual(actual, expected)
        self.conn.close()

    def test_load_res(self):
        expected = Res(1.0, 0.0, 1.5, 1.0, 1.0, 0.5, -1.0)
        actual = self.test_char._load_res()
        self.assertEqual(actual, expected)
        self.conn.close()

    def test_load_skills(self):
        self.assertEqual(len(self.test_char._skills), 1)

    def test_check_hp_within_limits(self):
        self.test_char.curr_hp = 50
        self.test_char.check_hp()
        self.assertEqual(self.test_char.curr_hp, 50)

    def test_check_hp_over_max(self):
        self.test_char.curr_hp = 200
        self.test_char.check_hp()
        self.assertEqual(self.test_char.curr_hp, self.test_char._stats.hp)

    def test_check_hp_negative(self):
        self.test_char.curr_hp = -1
        self.test_char.check_hp()
        self.assertEqual(self.test_char.curr_hp, 0)

    def test_check_hp_is_alive(self):
        self.test_char.check_hp()
        self.assertTrue(self.test_char.alive)

    def test_check_hp_die_when_zero(self):
        self.test_char.curr_hp = 0
        self.test_char.check_hp()
        self.assertFalse(self.test_char.alive)

    def test_check_mp_within_limits(self):
        self.test_char.curr_mp = 5
        self.test_char.check_mp()
        self.assertEqual(self.test_char.curr_mp, 5)

    def test_check_mp_over_max(self):
        self.test_char.curr_mp = 20
        self.test_char.check_mp()
        self.assertEqual(self.test_char.curr_mp, self.test_char._stats.mp)

    def test_use_item(self):
        pass
