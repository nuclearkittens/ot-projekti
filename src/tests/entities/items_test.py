import unittest

from database.initialise_db import initialise_db
from entities.items import Item

class StubCharacter:
    def __init__(self):
        self.id = 'bob'
        self.curr_hp = 100
        self.max_hp = 100
        self.curr_mp = 10
        self.max_mp = 10

class TestItem(unittest.TestCase):
    def setUp(self):
        initialise_db()
        self.target = StubCharacter()

    def use_other_item(self):
        test_item = Item('test_item3')
        test_info = test_item.use(self.target)
        self.assertFalse(test_info)

