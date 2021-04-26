from config import SCREEN_W, SCREEN_H
from menu import BattleMenu
from containers import ItemContainer, SkillContainer

class BattleMenuHandler:
    def __init__(self, keys, renderer, items, skills, magics, party):
        self._keys = keys
        self._renderer = renderer
        self._items = items
        self._skills = skills
        self._magics = magics
        self._party = party

        self.menu_pos = self._calc_menu_placement()
        self.all_menus = []
        self.menu_actions = ['skill', 'magic', 'item']

        self.main_menu = self._create_main_menu()
        self.all_menus.append(self.main_menu)
        self.main_menu.active = True
        # self.current_menu = self.main_menu

        self.skill_menus = {}
        self.magic_menus = {}
        self.item_menu = self._create_item_menu()
        self.all_menus.append(self.item_menu)

        self._create_char_menus()

    def draw_menus(self, current):
        action = None
        self.main_menu.draw_menu()
        for menu in self.all_menus:
            if menu.active:
                action = menu.update()
                menu.active = False
                if action in self.menu_actions:
                    if action == self.menu_actions[0]:
                        self.skill_menus[current].active = True
                    elif action == self.menu_actions[1]:
                        self.magic_menus[current].active = True
                    else:
                        self.item_menu.active = True
        return action