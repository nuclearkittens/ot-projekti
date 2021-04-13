import pygame
import unittest

class StubKeys:
    def __init__(self):
        self.UP_K, self.DOWN_K = False, False
        self.RIGHT_K, self.LEFT_K = False, False
        self.SELECT_K, self.START_K = False, False
        self.BACK_K, self.PAUSE_K = False, False

    def reset_keys(self):
        pass

