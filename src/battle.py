from config import FPS
import pygame as pg

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
        running = True
        current = None
        action = None
        target = None

        cooldown = 100
        update_time = pg.time.get_ticks()

        while running:
            self._check_events()
            if self._keys.QUIT:
                running = False
            current = self._check_turn()
            print(f'current turn: {current}, turns: {self._turns}')
            if current in self._gfx.party:
                action, target = self._player_action(current)
            elif current in self._gfx.enemies:
                action, target = current.character.make_decision(self._gfx.party)
            if current is not None:
                # self._execute_action(action, current, target)
                if action in current.character.inventory:
                    current.character.use_item(action, target.character)
                elif action in current.character.skills:
                    current.character.use_skill(action, target.character)
                while pg.time.get_ticks() - update_time < cooldown:
                    self._gfx.update_sprites()
                    self._gfx.update_target_list()
                    self._render(current)
                update_time = pg.time.get_ticks()

            self._reset_menus()
            self._tick()
            self._clock.tick(FPS)

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
            if not char.alive():
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

    def _player_action(self, current):
        player = True
        menu_stack = []
        action_stack = []

        self._reset_menus()
        for char in self._gfx.menus:
            if char == current:
                main_menu = self._gfx.menus[char]['main']
                main_menu.active = True
                menu_stack.append(main_menu)

        while player:
            self._check_events()
            if self._keys.QUIT:
                return None, None
            menu = self._get_active_menu()
            if menu is not None:
                if menu not in menu_stack:
                    menu_stack.append(menu)
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
                        action_stack.append(action)
                        self._gfx.target_cursor.active = True
            target = self._gfx.target_cursor.choose_target(self._keys, self._gfx.all)
            if target is not None:
                player = False
                self._reset_menus()
            # print(menu_stack)
            self._gfx.update_sprites()
            self._render(current, menu_stack)
            # self._gfx.draw_cursor(self._renderer)
            self._keys.reset_keys()
            self._clock.tick(FPS)
        for menu in menu_stack:
            menu.reset_cursor()
        return action_stack.pop(), target
