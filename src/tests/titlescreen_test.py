import unittest
import pygame

class StubEvent:
    def __init__(self, event_type, key):
        self.type = event_type
        self.key = key
        
