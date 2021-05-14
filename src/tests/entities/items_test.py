import unittest

from database.initialise_db import initialise_db
from entities.items import Item

class StubCharacter:
    def __init__(self):
        self.id = 'bob'
        self.curr_hp = 0
        self.max_hp = 100
        self.curr_mp = 0
        self.max_mp = 10

class TestItem(unittest.TestCase):
    def setUp(self):
        initialise_db()
        self.target = StubCharacter()

    def test_use_healing_item_hp_set_amount(self):
        test_item = Item('test_item1')
        test_item.use(self.target)
        self.assertEqual(self.target.curr_hp, 20)

    def test_use_healing_item_hp_percentage(self):
        test_item = Item('test_item2')
        test_item.use(self.target)
        self.assertEqual(self.target.curr_hp, 25)

    def test_use_healing_item_mp_set_amount(self):
        test_item = Item('test_item1')
        test_item.use(self.target)
        self.assertEqual(self.target.curr_mp, 5)

    def test_use_healing_item_mp_percentage(self):
        test_item = Item('test_item2')
        test_item.use(self.target)
        self.assertEqual(self.target.curr_mp, 1)

    def test_info_healing_set_amount(self):
        test_item = Item('test_item1')
        test_info = test_item.use(self.target)
        expected_info = [('hp', 20), ('mp', 5)]
        self.assertEqual(test_info, expected_info)

    def test_info_healing_percentage(self):
        test_item = Item('test_item2')
        test_info = test_item.use(self.target)
        expected_info = [('hp', 25), ('mp', 1)]
        self.assertEqual(test_info, expected_info)

    def test_use_other_item(self):
        test_item = Item('test_item3')
        test_info = test_item.use(self.target)
        self.assertFalse(test_info)

    def test_return_name(self):
        test_item = Item('test_item3')
        self.assertEqual(test_item.name, 'Test Item 3')

    def test_return_descr(self):
        test_item = Item('test_item3')
        self.assertEqual(test_item.description, 'test item 3: no healing')
