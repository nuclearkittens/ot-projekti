import unittest
import pygame as pg

from config import NATIVE_RESOLUTION, TILE_SIZE, TEST_IMG
from core.util import load_img
from database.initialise_db import initialise_db

class TestPrepare(unittest.TestCase):
    def setUp(self):
        initialise_db()
        pg.init()
        pg.display.set_mode(NATIVE_RESOLUTION, pg.HIDDEN)

    def tearDown(self):
        pg.quit()

    def test_load_image_no_image(self):
        img = load_img('bob.png')
        img_size = img.get_size()
        self.assertIsInstance(img, pg.Surface)
        self.assertEqual(img_size, TILE_SIZE)

    def test_load_existing_image(self):
        img = load_img(TEST_IMG)
        img_size = img.get_size()
        self.assertEqual(img_size, (64, 64))
