import unittest
from keys import Keys

class TestKeys(unittest.TestCase):
    def setUp(self):
        self.keys = Keys()

    def test_initialise_keys(self):
        self.assertFalse(self.keys.UP_K)
        self.assertFalse(self.keys.DOWN_K)
        self.assertFalse(self.keys.RIGHT_K)
        self.assertFalse(self.keys.LEFT_K)
        self.assertFalse(self.keys.SELECT_K)
        self.assertFalse(self.keys.START_K)
        self.assertFalse(self.keys.BACK_K)
        self.assertFalse(self.keys.PAUSE_K)

    def test_reset_keys(self):
        self.keys.UP_K, self.keys.DOWN_K = True, True
        self.keys.RIGHT_K, self.keys.LEFT_K = True, True
        self.keys.SELECT_K, self.keys.START_K = True, True
        self.keys.BACK_K, self.keys.PAUSE_K = True, True

        self.keys.reset_keys()

        self.assertFalse(self.keys.UP_K)
        self.assertFalse(self.keys.DOWN_K)
        self.assertFalse(self.keys.RIGHT_K)
        self.assertFalse(self.keys.LEFT_K)
        self.assertFalse(self.keys.SELECT_K)
        self.assertFalse(self.keys.START_K)
        self.assertFalse(self.keys.BACK_K)
        self.assertFalse(self.keys.PAUSE_K)




