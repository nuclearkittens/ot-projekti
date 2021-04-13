import unittest
from gamestate import GameState

class TestGameState(unittest.TestCase):
    def setUp(self):
        self.gs = GameState()

    def test_initialise_gamestate(self):
        self.assertTrue(self.gs.running)
        self.assertTrue(self.gs.title)
        self.assertFalse(self.gs.battle)
        self.assertFalse(self.gs.menu1)
        self.assertFalse(self.gs.menu1)

    def test_set_all_false(self):
        self.gs.set_all_false()

        self.assertFalse(self.gs.running)
        self.assertFalse(self.gs.title)
        self.assertFalse(self.gs.battle)
        self.assertFalse(self.gs.menu1)
        self.assertFalse(self.gs.menu1)