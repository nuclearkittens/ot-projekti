import unittest

from core.keys import Keys

class TestKeys(unittest.TestCase):
    def setUp(self):
        self.keys = Keys()
        self.keys.UP, self.keys.DOWN = True, True
        self.keys.RIGHT, self.keys.LEFT = True, True
        self.keys.SELECT, self.keys.START = True, True
        self.keys.BACK, self.keys.PAUSE = True, True

    def test_reset_keys_up(self):
        self.keys.reset_keys()
        self.assertFalse(self.keys.UP)

    def test_reset_keys_down(self):
        self.keys.reset_keys()
        self.assertFalse(self.keys.DOWN)

    def test_reset_keys_right(self):
        self.keys.reset_keys()
        self.assertFalse(self.keys.RIGHT)

    def test_reset_keys_left(self):
        self.keys.reset_keys()
        self.assertFalse(self.keys.LEFT)

    def test_reset_keys_select(self):
        self.keys.reset_keys()
        self.assertFalse(self.keys.SELECT)

    def test_reset_keys_start(self):
        self.keys.reset_keys()
        self.assertFalse(self.keys.START)

    def test_reset_keys_back(self):
        self.keys.reset_keys()
        self.assertFalse(self.keys.BACK)

    def test_reset_keys_pause(self):
        self.keys.reset_keys()
        self.assertFalse(self.keys.PAUSE)
