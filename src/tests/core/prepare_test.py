import unittest
import pygame as pg

from config import SCREEN_H, SCREEN_W, SCREEN_CAPTION
from core.prepare import (
    initialise_demo_display, create_demo_party, create_demo_enemies
    )
from database.initialise_db import initialise_db

class TestPrepare(unittest.TestCase):
    def setUp(self):
        initialise_db()
        pg.init()
        pg.display.set_mode((SCREEN_W, SCREEN_W), pg.HIDDEN)

    def tearDown(self):
        pg.quit()

    def test_initialise_demo_display_dimensions(self):
        screen = initialise_demo_display()
        size = screen.get_size()
        self.assertEqual(size, (SCREEN_W, SCREEN_H))

    def test_initialise_demo_display_caption(self):
        screen = initialise_demo_display()
        caption = pg.display.get_caption()[0]
        self.assertEqual(caption, SCREEN_CAPTION)

    def test_create_demo_party(self):
        party = create_demo_party()
        test_member = party[0].name
        self.assertEqual(len(party), 1)
        self.assertEqual(test_member, 'Bob')

    def test_create_demo_party_loads_inv(self):
        party = create_demo_party()
        inv = bool(party[0].inventory)
        self.assertTrue(inv)

    def test_create_enemies(self):
        enemies = create_demo_enemies()
        test_enem = enemies[0].name
        self.assertEqual(len(enemies), 1)
        self.assertEqual(test_enem, 'Bob')
