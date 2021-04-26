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
        party_mbrs = party
        party_itms = party.items

        temp_options = []
        temp_actions = []
        temp_frames = []
        for itm, qty in party_itms.items():
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
            'item', party_mbrs, 'main',
            self._renderer, self._keys,
            temp_options, temp_actions, x, y
            )

        for button in new_menu.buttons:
            for frames in temp_frames:
                if button.text == frames[-1]:
                    frames.pop()
                    for frame in frames:
                        button.add_frame(frame)
                    frames = [None]
        return new_menu

    def create_main_menu(self, party):
        x = self._pos[0][0]
        y = self._pos[0][1]
        options = ['Attack', 'Skill', 'Magic', 'Item']
        actions = [option.lower() for option in options]
        return BattleMenu(
            'main', party, 'main',
            self._renderer, self._keys,
            options, actions, x, y
            )

    def _create_skill_options(self, char):
        temp_skills = {}
        for skill in char.skills:
            if skill != 'attack':
                info = self._skill_cntr.fetch_skill(skill)
                name, cost = info[0], info[5]
                temp_skills[skill] = (name, cost)
        return temp_skills

    def _create_mag_options(self, char):
        temp_mag = {}
        for mag in char.magics:
            info = self._magic_cntr.fetch_skill(mag)
            name, cost = info[0], info[5]
            temp_mag[mag] = (name, cost)
        return temp_mag

    def create_skill_menu(self, char):
        x = self._pos[1][0]
        y = self._pos[1][1]

        temp_options = []
        temp_actions = []
        temp_skills = self._create_skill_options(char)

        if not temp_skills:
            temp_skills['no action'] = ('no skills', ')--:')

        for skill, val in temp_skills.items():
            text = f'{val[0]:20}{val[1]}'
            temp_actions.append(skill)
            temp_options.append(text)
        new_menu = BattleMenu(
            'skill', [char], 'main',
            self._renderer, self._keys,
            temp_options, temp_actions, x, y
            )

        return new_menu

    def create_magic_menu(self, char):
        x = self._pos[1][0]
        y = self._pos[1][1]

        temp_options = []
        temp_actions = []
        temp_mag = self._create_mag_options(char)

        if not temp_mag:
            temp_mag['no action'] = ('no magic', ')--:')

        for mag, val in temp_mag.items():
            text = f'{val[0]:20}{val[1]}'
            temp_actions.append(mag)
            temp_options.append(text)
        new_menu = BattleMenu(
            'magic', [char], 'main',
            self._renderer, self._keys,
            temp_options, temp_actions, x, y
            )

        return new_menu
