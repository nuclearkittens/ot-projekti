import unittest
import sqlite3

from config import DB_PATH, DB_CMDS_PATH
from database.initialise_db import drop_tables
from database.db_util import *

def populate_mock_db(conn):
    cur = conn.cursor()
    sql_file = open(DB_CMDS_PATH, 'r')
    data = sql_file.read()
    sql_file.close()
    queries = data.split(';')
    for query in queries:
        try:
            cur.execute(query)
        except sqlite3.OperationalError:
            print(f'query "{query}" skipped')
    conn.commit()

class TestDbUtil(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        populate_mock_db(self.conn)

    def tearDown(self):
        drop_tables(self.conn)
        self.conn.close()

    def test_load_stats(self):
        test_stats = load_stats('bob')
        self.assertIsInstance(test_stats, Stats)

    def test_load_stats_char_not_in_db(self):
        test_stats = load_stats('birb')
        self.assertIsNone(test_stats)

    def test_load_res(self):
        test_res = load_res('bob')
        self.assertIsInstance(test_res, Res)

    def test_load_res_char_not_in_db(self):
        test_res = load_res('birb')
        self.assertIsNone(test_res)

    def test_load_skills(self):
        test_skills = load_skills('bob')
        self.assertIsInstance(test_skills, dict)

    def test_load_skills_char_not_in_db(self):
        test_skills = load_skills('birb')
        self.assertFalse(test_skills)

    def test_load_party_info(self):
        test_info = load_party_info('bob')
        actual = (test_info[0], test_info[1])
        self.assertEqual(actual, ('Bob', 1))

    def test_load_party_info_char_not_in_db(self):
        test_info = load_party_info('birb')
        self.assertIsNone(test_info)

    def test_load_monster_info(self):
        test_info = load_monster_info('bob')
        self.assertIsInstance(test_info, MonsterInfo)

    def test_load_monster_info_char_not_in_db(self):
        test_info = load_monster_info('birb')
        self.assertIsNone(test_info)

    def test_load_inventory(self):
        test_inv = load_inventory('bob')
        self.assertTrue(test_inv)

    def test_load_inventory_char_not_in_db(self):
        test_inv = load_inventory('birb')
        self.assertFalse(test_inv)

    def test_load_item_info(self):
        test_info = load_item_info('test_item1')
        self.assertEqual(
            (test_info[0], test_info[1]), ('Test Item 1', 'test item 1: set amount hp/mp heal')
            )

    def test_load_item_not_in_db(self):
        test_info = load_item_info('nothing')
        self.assertIsNone(test_info)

    def test_load_item_effects(self):
        test_fx = load_item_effects('test_item1')
        expected = [
            ('heal', 'hp', 20), ('heal', 'mp', 5)
        ]
        self.assertEqual(test_fx, expected)

    def test_load_item_effects_not_in_db(self):
        test_fx = load_item_effects('nothing')
        self.assertFalse(test_fx)

    def test_load_skill_info(self):
        test_info = load_skill_info('test_skill')
        self.assertIsInstance(test_info, SkillInfo)

    def test_load_skill_info_not_in_db(self):
        test_info = load_skill_info('energy_blst')
        self.assertIsNone(test_info)

    def test_load_skill_attr(self):
        test_attr = load_skill_attr('test_skill')
        self.assertIsInstance(test_attr, SkillAttributes)

    def test_load_skill_attr_not_in_db(self):
        test_attr = load_skill_attr('energy_blst')
        self.assertIsNone(test_attr)
