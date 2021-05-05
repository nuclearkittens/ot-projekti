import unittest
import sqlite3

from config import DB_TEST_SCRIPT
from database.initialise_db import (
    execute_script_from_file,
    drop_tables
)

tables = [
    'Items', 'Skills', 'Effects', 'ItemEffects',
    'SkillEffects', 'Monsters', 'Party',
    'Stats', 'Resistance', 'CharSkills', 'Loot',
    'Inventory'
    ]
get_tables = '''SELECT name FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY 1
            '''

class TestInitialiseDb(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row

    def test_execute_script_from_file(self):
        cursor = self.conn.cursor()
        execute_script_from_file(cursor, DB_TEST_SCRIPT)
        cursor.execute(get_tables)
        itms = [row[0] for row in cursor.fetchall()]
        self.assertEqual(list(itms), sorted(tables))
        self.conn.close()

    def test_drop_tables_db_empty(self):
        drop_tables(self.conn)
        cursor = self.conn.cursor()
        cursor.execute(get_tables)
        itms = cursor.fetchall()
        self.assertEqual(len(itms), 0)
        self.conn.close()

    def test_drop_tables_db_not_empty(self):
        cursor = self.conn.cursor()
        execute_script_from_file(cursor, DB_TEST_SCRIPT)
        drop_tables(self.conn)
        cursor.execute(get_tables)
        itms = cursor.fetchall()
        self.assertEqual(len(itms), 0)
        self.conn.close()
