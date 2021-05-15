import unittest
import sqlite3

from config import DB_PATH
from database.initialise_db import drop_tables
from database.db_util import *

class TestDbUtilEmptyDb(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        drop_tables(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_load_stats(self):
        stats = load_stats('bob')
        self.assertIsNone(stats)

    def test_load_res(self):
        res = load_res('bob')
        self.assertIsNone(res)

    def test_load_skills(self):
        skills = load_skills('bob')
        self.assertFalse(skills)

    def test_load_party_info(self):
        info = load_party_info('bob')
        self.assertIsNone(info)

    def test_load_monster_info(self):
        info = load_monster_info('bob')
        self.assertIsNone(info)

    def test_load_inv(self):
        inv = load_inventory('bob')
        self.assertFalse(inv)

    def test_load_item_info(self):
        info = load_item_info('test_item1')
        self.assertIsNone(info)

    def test_load_item_effects(self):
        fx = load_item_effects('test_item1')
        self.assertFalse(fx)

    def test_load_skill_info(self):
        info = load_skill_info('test_skill')
        self.assertIsNone(info)

    def test_load_skill_attr(self):
        attr = load_skill_attr('test_item1')
        self.assertIsNone(attr)
