from config import SCREEN_W, SCREEN_H
from containers import ItemContainer, SkillContainer
from menu import BattleMenu

class BattleMenuCreator:
    def __init__(self, renderer, keys):
        self._renderer = renderer
        self._keys = keys
        self._item_cntr = ItemContainer()
        self._skill_cntr = SkillContainer('skill')
        self._magic_cntr = SkillContainer('blk_mag')

        self._pos = self._calc_menu_placement()

    def _calc_menu_placement(self):
        pos = []
        c = SCREEN_W // 4
        x = 0
        y = 3 * SCREEN_H // 4
        for i in range(2):
            pos.append((x, y))
            x += c
        return pos

    def create_item_menu(self, party):
        x = self._pos[1][0]
        y = self._pos[1][1]
        party_mbrs = party.current_party
        party_itms = party.items

        temp_options = []
        temp_actions = []
        temp_frames = []
        for itm, qty in party_itms:
            info = self._item_cntr.fetch_item(itm)
            name = info[0]
            text = f'{name:20}{qty}'
            temp_options.append(text)
            temp_actions.append(itm)
            itm_frames = []
            for i in range(qty+1):
                text = f'{name:20}{i}'
                itm_frames.append(text)
            temp_frames.append(itm_frames)

        new_menu = BattleMenu(
            'item', party_mbrs,
            self._renderer, self._keys,
            temp_options, temp_actions, x, y
            )

        for button in new_menu.buttons:
            for frames in temp_frames:
                if button.text == frames[-1]:
                    frames.pop()
                    for frame in frames:
                        button.add_frame(frame)
                    frames = None
        return new_menu

    def create_main_menu(self, party):
        x = self._pos[0][0]
        y = self._pos[0][1]
        options = ['Attack', 'Skill', 'Magic', 'Item']
        actions = [option.lower() for option in options]
        return BattleMenu(
            'main', party,
            self._renderer, self._keys,
            options, actions, x, y
            )

    def _create_options(self, char):
        temp_skills = {}
        temp_mag = {}
        for skill in char.skills:
            if skill != 'attack':
                info = self._skill_cntr.fetch_skill(skill)
                name, cost = info[0], info[5]
                temp_skills[skill] = (name, cost)
        for mag in char.magics:
            info = self._magic_cntr.fetch_skill(mag)
            name, cost = info[0], info[5]
            temp_mag[mag] = (name, cost)
        return temp_skills, temp_mag

    def create_skill_and_magic_menus(self, char):
        x = self._pos[1][0]
        y = self._pos[1][1]

        temp_options = []
        temp_actions = []
        temp_skills, temp_mag = self._create_options(char)
        menu_list = []

        for skill, val in temp_skills.items():
            text = f'{val[0]:20}{val[1]}'
            temp_actions.append(skill)
            temp_options.append(text)
        new_menu = BattleMenu(
            'skill', [char], self._renderer, self._keys,
            temp_options, temp_actions, x, y
            )
        menu_list.append(new_menu)

        temp_options = []
        temp_actions = []
        for mag, val in temp_mag.items():
            text = f'{val[0]:20}{val[1]}'
            temp_actions.append(mag)
            temp_options.append(text)
        new_menu = BattleMenu(
            'magic', [char], self._renderer, self._keys,
            temp_options, temp_actions, x, y
            )
        menu_list.append(new_menu)

        return menu_list
        