from collections import deque

import unittest
import pygame as pg

from combat.battle import Battle
from database.initialise_db import initialise_db
from ui.renderer import Renderer
from config import NATIVE_RESOLUTION
from prepare import create_demo_party
from keys import Keys

class StubEventHandler:
    def __init__(self):
        self.keys = Keys()

    def check_input(self):
        pass

class StubClock:
    def tick(self, FPS):
        pass

def init_test_battle():
    screen = pg.display.set_mode(NATIVE_RESOLUTION, pg.HIDDEN)
    renderer = Renderer(screen)
    party = create_demo_party()
    events = StubEventHandler()
    clock = StubClock()
    return Battle(clock, renderer, events, party)

class TestPlayerAction(unittest.TestCase):
    def setUp(self):
        initialise_db()
        pg.init()
        self.battle = init_test_battle()
        self.plr = self.battle._plr
        self.curr = self.battle._gfx.party.sprites()[0]
        self.plr.current = self.curr

    def tearDown(self):
        pg.quit()

    def test_check_menu_in_stack(self):
        self.plr.set_menu_stack()
        menu = self.plr.check_menu()
        self.assertIsNotNone(menu)

    def test_check_menu_not_in_stack(self):
        self.plr.set_menu_stack()
        self.plr.reset_menus()
        self.plr._set_active_menu('item')
        menu = self.plr.check_menu()
        self.assertIsNotNone(menu)
        self.assertEqual(len(self.plr._menu_stack), 2)

    def test_check_menu_not_active(self):
        menu = self.plr.check_menu()
        self.assertIsNone(menu)

    def test_check_action_current_is_none(self):
        self.plr.set_menu_stack()
        menu = self.plr._get_active_menu()
        self.plr.current = None
        info, action = self.plr.check_action(menu)
        self.assertIsNone(info)
        self.assertIsNone(action)

    def test_check_action_menu_inactive(self):
        self.plr.set_menu_stack()
        menu = self.plr._get_active_menu()
        menu.active = False
        info, action = self.plr.check_action(menu)
        self.assertIsNone(info)
        self.assertIsNone(action)

    def test_check_action_skill(self):
        self.plr.set_menu_stack()
        menu = self.plr._get_active_menu()
        self.plr._keys.SELECT = True
        info, action = self.plr.check_action(menu)
        self.assertEqual((info, action), ('attack', 'attack'))
        self.assertTrue(self.plr._cursor.active)

    def test_check_action_no_mp_left(self):
        self.plr.set_menu_stack()
        menu = self.plr._get_active_menu()
        menu.active = False
        self.plr._set_active_menu('magic')
        self.plr._curr.character.curr_mp = 0
        self.plr._keys.SELECT = True
        menu = self.plr._get_active_menu()
        info, action = self.plr.check_action(menu)
        expected = ('Not enough MP!', 'test_magic')
        self.assertEqual((info, action), expected)

    def test_check_action_no_items_in_inv(self):
        self.plr.set_menu_stack()
        menu = self.plr._get_active_menu()
        menu.active = False
        self.plr._set_active_menu('item')
        self.plr._curr.character.use_item(
            'test_item1', self.plr._curr.character
            )
        self.plr._keys.SELECT = True
        menu = self.plr._get_active_menu()
        info, action = self.plr.check_action(menu)
        expected = ('Not enough TEST ITEM 1s in inventory!', 'test_item1')
        self.assertEqual((info, action), expected)

    def test_check_action_in_menus(self):
        self.plr.set_menu_stack()
        menu = self.plr._get_active_menu()
        self.plr._keys.DOWN = True
        self.plr._keys.SELECT = True
        info, action = self.plr.check_action(menu)
        self.assertEqual((info, action), ('skill', 'skill'))

    def test_check_action_back_to_main(self):
        self.plr.set_menu_stack()
        menu = self.plr._get_active_menu()
        menu.active = False
        self.plr._set_active_menu('magic')
        self.plr.check_menu()
        self.plr._curr.character.curr_mp = 0
        self.plr._keys.BACK = True
        menu = self.plr._get_active_menu()
        info, action = self.plr.check_action(menu)
        self.assertEqual((info, action), ('test_magic', 'main'))
        self.assertEqual(len(self.plr.menu_stack), 1)

    def test_check_target_selection(self):
        self.plr._keys.BACK = True
        menu1 = self.plr._get_active_menu()
        self.plr.check_target_selection()
        menu2 = self.plr._get_active_menu()
        self.assertIsNone(menu1)
        self.assertIsNotNone(menu2)

    def test_check_target_selection_pop_from_stack(self):
        self.plr.set_menu_stack()
        menu = self.plr._get_active_menu()
        menu.active = False
        self.plr._set_active_menu('skill')
        self.plr.check_menu()
        len1 = len(self.plr.menu_stack)
        self.plr._keys.BACK = True
        self.plr.check_target_selection()
        len2 = len(self.plr.menu_stack)
        self.assertLess(len2, len1)

    def test_set_menu_stack(self):
        self.plr.set_menu_stack()
        self.assertEqual(len(self.plr.menu_stack), 1)

    def test_reset_cursors(self):
        self.plr._cursor.current_pos = self.plr._cursor.pos[-1]
        self.plr.set_menu_stack()
        menu = self.plr._get_active_menu()
        menu._cursor_current = menu._cursor_pos[-1]
        self.plr.reset_cursors()
        self.assertEqual(self.plr._cursor.current_pos, self.plr._cursor.pos[0])
        self.assertEqual(menu._cursor_current, menu._cursor_pos[0])

    def test_reset_menus(self):
        self.plr.set_menu_stack()
        menu = self.plr._get_active_menu()
        self.plr._keys.SELECT = True
        self.plr.reset_menus()
        self.assertFalse(menu.active)
        self.assertFalse(self.plr._keys.SELECT)

    def test_update_info_curr_is_none(self):
        self.plr._curr = None
        text = self.plr.update_info('birb')
        self.assertFalse(text)

    def test_update_info_none(self):
        text = self.plr.update_info(None)
        self.assertFalse(text)

    def test_update_info_is_str(self):
        text = self.plr.update_info('birb')
        self.assertEqual(text, ' birb')

    def test_update_info_menu_action(self):
        text = self.plr.update_info('magic')
        self.assertEqual(text, ' Choose magic')

    def test_update_info_skill(self):
        text = self.plr.update_info('test_magic')
        self.assertEqual(text, ' A skill for testing')

    def test_update_info_item(self):
        text = self.plr.update_info('test_item1')
        self.assertEqual(text, ' test item 1: set amount hp/mp heal')

    def test_get_active_menu_no_stack(self):
        menu = self.plr._get_active_menu()
        self.assertIsNone(menu)

    def test_get_active_menu(self):
        self.plr.set_menu_stack()
        menu = self.plr._get_active_menu()
        self.assertIsNotNone(menu)

    def test_set_active_menu(self):
        self.plr._set_active_menu('item')
        menu = self.plr._get_active_menu()
        self.assertIsNotNone(menu)

    def test_set_active_menu_key_error(self):
        self.plr._set_active_menu('menu')
        menu = self.plr._get_active_menu()
        self.assertIsNone(menu)

    def test_menu_stack_getter(self):
        self.assertEqual(self.plr._menu_stack, self.plr.menu_stack)

    def test_current_getter(self):
        self.assertEqual(self.plr._curr, self.plr.current)

    def test_current_setter(self):
        start = self.plr.current
        self.plr.current = None
        end = self.plr.current
        self.assertNotEqual(end, start)
