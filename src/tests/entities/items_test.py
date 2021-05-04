import unittest
import sqlite3

from entities.items import Item

def populate_mock_db(conn):
    queries = [
        'CREATE TABLE Items (id TEXT PRIMARY KEY, name TEXT, descr TEXT)',
        'CREATE TABLE ItemEffects (item_id TEXT, effect_id TEXT)',
        'CREATE TABLE Effects (id TEXT PRIMARY KEY, target_attr TEXT, effect TEXT, amount NUMERIC)',
        'INSERT INTO Items (id, name, descr) VALUES ("test_item1", "Test Item 1", "test item 1: set amount hp/mp heal")',
        'INSERT INTO Items (id, name, descr) VALUES ("test_item2", "Test Item 2", "test item 2: percentage hp/mp heal")',
        'INSERT INTO Items (id, name, descr) VALUES ("test_item3", "Test Item 3", "test item 3: no healing")',
        'INSERT INTO Effects (id, target_attr, effect, amount) VALUES ("hp20", "hp", "heal", 20)',
        'INSERT INTO Effects (id, target_attr, effect, amount) VALUES ("mp5", "mp", "heal", 5)',
        'INSERT INTO Effects (id, target_attr, effect, amount) VALUES ("hp25pc", "hp", "heal", 0.25)',
        'INSERT INTO Effects (id, target_attr, effect, amount) VALUES ("mp10pc", "mp", "heal", 0.1)',
        'INSERT INTO Effects (id, target_attr, effect, amount) VALUES ("other", "other", "other", 0)',
        'INSERT INTO ItemEffects (item_id, effect_id) VALUES ("test_item1", "hp20")',
        'INSERT INTO ItemEffects (item_id, effect_id) VALUES ("test_item2", "hp25pc")',
        'INSERT INTO ItemEffects (item_id, effect_id) VALUES ("test_item1", "mp5")',
        'INSERT INTO ItemEffects (item_id, effect_id) VALUES ("test_item2", "mp10pc")',
        'INSERT INTO ItemEffects (item_id, effect_id) VALUES ("test_item3", "other")'
    ]
    cur = conn.cursor()
    for query in queries:
        cur.execute(query)
        conn.commit()

class StubCharacter:
    def __init__(self):
        self.curr_hp = 0
        self.curr_mp = 0
        self.max_hp = 100
        self.max_mp = 20

class TestItem(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        populate_mock_db(self.conn)

    def test_load_info(self):
        test_item = Item('test_item3', self.conn)
        info = test_item._load_info()
        self.assertEqual(tuple(info), ('Test Item 3', 'test item 3: no healing'))
        self.conn.close()

    def test_load_effects(self):
        test_item = Item('test_item3', self.conn)
        effects = test_item._effects
        expected = [('other', 'other', 0)]
        self.assertEqual(effects, expected)
        self.conn.close()

    def test_use_set_amount_healing_item(self):
        test_item = Item('test_item1', self.conn)
        target = StubCharacter()
        test_item.use(target)
        expected = (20, 5)
        actual = (target.curr_hp, target.curr_mp)
        self.assertEqual(actual, expected)
        self.conn.close()

    def test_use_percentage_healing_item(self):
        test_item = Item('test_item2', self.conn)
        target = StubCharacter()
        test_item.use(target)
        expected = (25, 2)
        actual = (target.curr_hp, target.curr_mp)
        self.assertEqual(actual, expected)
        self.conn.close()

    def test_use_other_item(self):
        test_item = Item('test_item3', self.conn)
        target = StubCharacter()
        test_item.use(target)
        expected = (0, 0)
        actual = (target.curr_hp, target.curr_mp)
        self.assertEqual(actual, expected)
        self.conn.close()

    def test_property_name(self):
        test_item = Item('test_item3', self.conn)
        self.assertEqual(test_item.name, "Test Item 3")
        self.conn.close()

    def test_property_description(self):
        test_item = Item('test_item3', self.conn)
        self.assertEqual(test_item.description, "test item 3: no healing")
        self.conn.close()