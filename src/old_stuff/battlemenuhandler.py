from battlemenucreator import BattleMenuCreator

class BattleMenuHandler:
    def __init__(self, keys, renderer, party):
        self._keys = keys
        self._renderer = renderer
        self._party = party

        self.main_menu = None
        self.item_menu = None

        self.all_menus = []
        self.skill_menus = []
        self.magic_menus = []

        self._create_menus()
        self.menu_actions = ['main', 'skill', 'magic', 'item']

        self.main_menu.active = True

    def _create_menus(self):
        menucreator = BattleMenuCreator(self._renderer, self._keys)

        self.main_menu = menucreator.create_main_menu(self._party.current_party)
        self.all_menus.append(self.main_menu)

        self.item_menu = menucreator.create_item_menu(self._party)
        self.all_menus.append(self.item_menu)

        for char in self._party.group:
            skill_menu = menucreator.create_skill_menu(char)
            magic_menu = menucreator.create_magic_menu(char)
            self.skill_menus.append(skill_menu)
            self.magic_menus.append(magic_menu)

    def get_action(self, current):
        action = None
        self.draw_main_menu()
        for menu in self.all_menus:
            if menu.active and current in menu.owners:
                action = menu.update()
                menu.active = False
        return action

    def draw_main_menu(self):
        self.main_menu.draw_menu()
