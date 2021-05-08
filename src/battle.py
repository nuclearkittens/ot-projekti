import pygame as pg

from config import FPS
from ui.battlegraphics import BattleGFX

class Battle:
    def __init__(self, clock, renderer, eventhandler, party):
        self._clock = clock
        self._renderer = renderer
        self._eventhandler = eventhandler
        self._keys = self._eventhandler.keys

        self._gfx = BattleGFX(party)
        self._turns = self._generate_turns()

    def loop(self):
        def execute_action(action, current, target):
            info = None
            if action in current.character.inventory:
                info = current.character.use_item(action, target.character)
                # self._gfx.dmg_text.add(button)
            elif action in current.character.skills:
                info = current.character.use_skill(action, target.character)
            if info is not None:
                for elem in info:
                    self._gfx.create_dmg_txt_button(elem[0], elem[1], target)

        running = True
        current = None
        action = None
        target = None

        # cooldown = 100
        # update_time = pg.time.get_ticks()

        while running:
            self._check_events()
            if self._keys.QUIT:
                running = False
            current = self._check_turn()
            # self._cooldown(current)
            print(f'current turn: {current}, turns: {self._turns}')
            if current in self._gfx.party:
                action, target = self._player_action_v1_5(current)
            elif current in self._gfx.enemies:
                action, target = current.character.make_decision(self._gfx.party)
                # self._cooldown(current)
            if current is not None:
                # self._cooldown(current)
                execute_action(action, current, target)
                # if action in current.character.inventory:
                #     current.character.use_item(action, target.character)
                # elif action in current.character.skills:
                #     current.character.use_skill(action, target.character)

                # while pg.time.get_ticks() - update_time < cooldown:
                #     self._gfx.update_sprites()
                #     self._gfx.update_target_list()
                #     self._render(current)
                # update_time = pg.time.get_ticks()
            # self._update(current)
            self._reset_menus()
            self._gfx.update_sprites()
            self._gfx.update_target_list()
            # self._tick()
            self._reset_menus()
            self._tick()
            self._clock.tick(FPS)
            self._render(current)

    def _update(self, current):
        self._reset_menus()
        self._gfx.update_sprites()
        self._gfx.update_target_list()
        self._tick()
        self._clock.tick(FPS)
        self._render(current)

    def _cooldown(self, current):
        cooldown = 100
        update_time = pg.time.get_ticks()
        while pg.time.get_ticks() - update_time < cooldown:
            self._update(current)

    def _render(self, current, menu_stack=None):
        # draw everything here
        self._gfx.render(self._renderer, current)
        if menu_stack is not None:
            for menu in menu_stack:
                menu.draw(self._renderer)
        self._gfx.draw_cursor(self._renderer)
        self._renderer.update_display()

    def _check_events(self):
        self._eventhandler.check_input()

    def _generate_turns(self):
        turns = {}
        for char in self._gfx.all:
            turns[char] = char.character.set_tick_speed()
        return turns

    def _tick(self):
        for char in self._turns:
            # if not char.alive():
            if char.character.curr_hp < 1:
                self._turns[char] = -1
            if self._turns[char] > 0:
                self._turns[char] -= 1

    def _check_turn(self):
        for char in self._turns:
            if self._turns[char] == 0:
                self._turns[char] = char.character.set_tick_speed()
                return char
        return None

    # def _execute_action(self, action, current, target):
    #     if action in current.character.inventory:
    #         current.character.use_item(action, target.character)
    #     elif action in current.character.skills:
    #         current.character.use_skill(action, target.character)

    def _reset_menus(self):
        for dct in self._gfx.menus.values():
            for menu in dct.values():
                menu.active = False
                menu.reset_buttons()
        self._keys.reset_keys()

    def _get_active_menu(self):
        for char in self._gfx.menus:
            for menu in self._gfx.menus[char].values():
                if menu.active:
                    return menu
        return None

    def _set_active_menu(self, current, menu_type):
        for char in self._gfx.menus:
            if char == current:
                self._gfx.menus[char][menu_type].active = True

    # def _player_action(self, current):
    # DO NOT DELETE! it works and the refactoring is under construction
    #     def set_menu_stack(current):
    #         stack = []
    #         self._reset_menus()
    #         for char in self._gfx.menus:
    #             if char == current:
    #                 main_menu = self._gfx.menus[char]['main']
    #                 main_menu.active = True
    #                 stack.append(main_menu)
    #         return stack

    #     player = True
    #     menu_stack = set_menu_stack(current)
    #     action_stack = []

    #     while player:
    #         self._check_events()
    #         if self._keys.QUIT:
    #             return None, None

    #         menu = self._get_active_menu()
    #         if menu is not None:
    #             if menu not in menu_stack:
    #                 menu_stack.append(menu)

    #             action = menu.update(self._keys)
    #             if action is not None:
    #                 if action == 'main' and len(menu_stack) > 1:
    #                     menu_stack.pop()
    #                     menu_stack[0].reset_buttons()
    #                 self._keys.reset_keys()

    #                 if action in self._gfx.menus[current]:
    #                     self._set_active_menu(current, action)
    #                 elif (
    #                         action in current.character.skills or
    #                         action in current.character.inventory
    #                     ):
    #                     action_stack.append(action)
    #                     self._gfx.target_cursor.active = True

    #         target = self._gfx.target_cursor.choose_target(self._keys, self._gfx.all)
    #         if target is not None:
    #             player = False
    #             self._reset_menus()

    #         # print(menu_stack)
    #         self._gfx.update_sprites()
    #         self._render(current, menu_stack)
    #         # self._gfx.draw_cursor(self._renderer)
    #         self._keys.reset_keys()
    #         self._clock.tick(FPS)

    #     for menu in menu_stack:
    #         menu.reset_cursor()

    #     return action_stack.pop(), target

    def _player_action_v1_5(self, current):
        def set_menu_stack(current):
            stack = []
            self._reset_menus()
            for char in self._gfx.menus:
                if char == current:
                    main_menu = self._gfx.menus[char]['main']
                    main_menu.active = True
                    stack.append(main_menu)
            return stack

        def check_menu(menu_stack):
            menu = self._get_active_menu()
            if menu is not None:
                if menu not in menu_stack:
                    menu_stack.append(menu)

            return menu

        def check_action(menu, menu_stack, current):
            action = menu.update(self._keys)
            if action is not None:
                if action == 'main' and len(menu_stack) > 1:
                    menu_stack.pop()
                    menu_stack[0].reset_buttons()
                self._keys.reset_keys()
                if action in self._gfx.menus[current]:
                    self._set_active_menu(current, action)
                elif (
                        action in current.character.skills or
                        action in current.character.inventory
                    ):
                    # action_stack.append(action)
                    self._gfx.target_cursor.active = True

            return action

        def check_target():
            return self._gfx.target_cursor.choose_target(self._keys, self._gfx.all)

        def update(current, menu_stack):
            self._gfx.update_sprites()
            # self._gfx.update_target_list()
            self._render(current, menu_stack)
            self._keys.reset_keys()
            self._clock.tick(FPS)

        player = True
        menu_stack = set_menu_stack(current)
        action = None

        while player:
            self._check_events()
            if self._keys.QUIT:
                return None, None
            menu = check_menu(menu_stack)
            if menu is not None:
                action = check_action(menu, menu_stack, current)
            target = check_target()
            if target is not None:
                player = False
                self._reset_menus()
            update(current, menu_stack)

        for menu in menu_stack:
            menu.reset_cursor()

        return action, target
