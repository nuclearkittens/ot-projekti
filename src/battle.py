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
            elif action in current.character.skills:
                info = current.character.use_skill(action, target.character)
            if info is not None:
                for elem in info:
                    self._gfx.create_dmg_txt_button(elem[0], elem[1], target)

        def tick():
            for char in self._turns:
                if not char.alive():
                    self._turns[char] = -1
                if self._turns[char] > 0:
                    self._turns[char] -= 1

        def check_turn():
            for char in self._turns:
                if self._turns[char] == 0:
                    self._turns[char] = char.character.set_tick_speed()
                    return char
            return None

        def update(current):
            self._reset_menus()
            self._gfx.update_sprites()
            self._gfx.update_target_list()
            tick()
            self._clock.tick(FPS)
            self._render(current)

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
            current = check_turn()
            if current in self._gfx.party:
                action, target = self._player_action(current)
            elif current in self._gfx.enemies:
                action, target = current.character.make_decision(self._gfx.party)
            if current is not None:
                execute_action(action, current, target)
            while pg.time.get_ticks() - update_time < cooldown:
                update(current)
            update_time = pg.time.get_ticks()

    def _player_action(self, current):
        def set_menu_stack(current):
            stack = []
            self._reset_menus()
            for char in self._gfx.menus:
                if char == current:
                    main_menu = self._gfx.menus[char]['main']
                    main_menu.active = True
                    stack.append(main_menu)
            return stack

        def get_active_menu():
            for char in self._gfx.menus:
                for menu in self._gfx.menus[char].values():
                    if menu.active:
                        return menu
            return None

        def set_active_menu(current, menu_type):
            for char in self._gfx.menus:
                if char == current:
                    self._gfx.menus[char][menu_type].active = True

        def check_menu(menu_stack):
            menu = get_active_menu()
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
                    set_active_menu(current, action)
                elif (
                        action in current.character.skills or
                        action in current.character.inventory
                    ):
                    self._gfx.target_cursor.active = True

            return action

        def check_target():
            return self._gfx.target_cursor.choose_target(self._keys, self._gfx.all)

        def update(current, menu_stack):
            self._gfx.update_sprites()
            self._clock.tick(FPS)
            self._render(current, menu_stack)
            self._keys.reset_keys()

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

        self._gfx.target_cursor.reset()

        return action, target

    def _render(self, current, menu_stack=None):
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

    def _reset_menus(self):
        for dct in self._gfx.menus.values():
            for menu in dct.values():
                menu.active = False
                menu.reset_buttons()
        self._keys.reset_keys()
