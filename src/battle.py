from collections import deque
import pygame as pg

from config import FPS
from ui.battlegraphics import BattleGFX

class Battle:
    def __init__(self, clock, renderer, eventhandler, party):
        self._clock = clock
        self._renderer = renderer
        self._eventhandler = eventhandler
        self._keys = self._eventhandler.keys

        self._party = party
        self._gfx = BattleGFX(party)
        self._turns = self._generate_turns()

        self._gameover = False
        self._victory = False

        self.demo = False

    def loop(self):
        def execute_action(action, current, target):
            info = None
            if action in current.character.inventory:
                info = current.character.use_item(action, target.character)
            elif action in current.character.skills:
                info = current.character.use_skill(action, target.character)
            if isinstance(info, str):
                self._gfx.update_info(info)
            elif isinstance(info, list):
                for elem in info:
                    self._gfx.create_dmg_txt_button(elem[0], elem[1], target)

        def update_info(action, current, target):
            try:
                name_curr = current.character.name.upper()
                name_target = target.character.name.upper()
            except AttributeError:
                return
            if name_curr == name_target:
                name_target = 'THEMSELF'
            if action in current.character.inventory:
                action = current.character.inventory[action][0].name.upper()
            elif action in current.character.skills:
                action = current.character.skills[action].name.upper()

            text = f' {name_curr} used {action} on {name_target}!'
            self._gfx.update_info(text)

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

        def check_game_over():
            if not bool(self._gfx.enemies):
                self._gameover = True
                self._victory = True

            if not bool(self._gfx.party):
                self._gameover = True

        def get_current(queue):
            while True:
                current = queue.popleft()
                if current.character.alive:
                    return current

        def update():
            self._keys.reset_keys()
            self._gfx.update_sprites()
            self._gfx.update_target_list()
            tick()
            self._render()
            self._clock.tick(FPS)

        running = True
        current = None
        action = None
        target = None
        queue = deque()

        cooldown = 0
        wait = 50

        while running:
            self._check_events()
            if self._keys.QUIT:
                running = False
            current = check_turn()
            if current is not None:
                queue.append(current)
            if cooldown > wait:
                cooldown = 0
                current = get_current(queue)
                if current in self._gfx.party:
                    action, target = self._player_action(current)
                elif current in self._gfx.enemies:
                    action, target = current.character.make_decision(self._gfx.party.sprites())
                execute_action(action, current, target)
                update_info(action, current, target)
                self._reset_menus()
            cooldown += 1
            update()
            check_game_over()
            if self._gameover:
                running = False

        self._game_over()

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
            info, action = menu.update(self._keys)
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
                    if (
                            action in current.character.skills and
                            current.character.get_skill_cost(action) > current.character.curr_mp
                        ):
                        info = 'Not enough MP!'
                    elif (
                            action in current.character.inventory and
                            current.character.get_item_qty(action) == 0
                        ):
                        item = current.character.inventory[action][0].name.upper()
                        info = f'Not enough {item}s in inventory!'
                    else:
                        self._gfx.target_cursor.active = True

            return info, action

        def check_target(current, menu_stack):
            target, name = self._gfx.target_cursor.choose_target(self._keys, self._gfx.all)
            if self._keys.BACK:
                if len(menu_stack) > 1:
                    menu = menu_stack.pop()
                    menu.active = True
                else:
                    set_active_menu(current, 'main')
                    menu = get_active_menu()
                menu.update_buttons()
                menu.reset_buttons()
            return target, name

        def update(current, menu_stack):
            self._gfx.update_sprites()
            self._render(current, menu_stack)
            self._keys.reset_keys()
            self._clock.tick(FPS)

        def update_info(current, info):
            if (
                    info in self._gfx.menus[current] and
                    info != 'attack'
                ):
                text = f' Choose {info}'
            elif info in current.character.skills:
                text = f' {current.character.skills[info].description}'
            elif info in current.character.inventory:
                text = f' {current.character.inventory[info][0].description}'
            elif info is not None:
                text = f' {info}'
            try:
                self._gfx.update_info(text)
            except UnboundLocalError:
                pass

        player = True
        menu_stack = set_menu_stack(current)
        action = None

        while player:
            self._check_events()
            if self._keys.QUIT:
                return None, None
            menu = check_menu(menu_stack)
            if menu is not None:
                info, action = check_action(menu, menu_stack, current)
                update_info(current, info)
            target, name = check_target(current, menu_stack)
            if name is not None:
                update_info(current, name.upper())
            if target is not None:
                player = False
                self._reset_menus()
            update(current, menu_stack)

        for menu in menu_stack:
            menu.reset_cursor()

        self._gfx.target_cursor.reset()

        return action, target

    def _render(self, current=None, menu_stack=None):
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

    def _game_over(self):
        base, status, text = self._gfx.create_game_over_screen(
            self._renderer, self._victory
            )
        while self._gameover:
            self._check_events()
            if self._keys.QUIT or self._keys.SELECT:
                self._gameover = False
            self._gfx.render_game_over(
                self._renderer, base, status, text
            )
            self._renderer.update_display()

    def _pause(self):
        paused = True

        while paused:
            self._check_events()
            if self._keys.QUIT or self._keys.PAUSE:
                paused = False
                if self._keys.PAUSE:
                    self._keys.reset_keys()

