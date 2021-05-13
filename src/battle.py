from collections import deque

from config import FPS
from ui.battlegraphics import BattleGFX

class Battle:
    '''Class for handling all the battle action.

    attr:
        keys: Keys object
        gfx: BattleGFX object; handles the graphic elements of battle
        turns: dict; keeps track of whose turn it is
        gameover: bool; tells if the battle is over
        victory: bool; tells if the party won the battle
        demo: bool; True if running demo
    '''
    def __init__(self, clock, renderer, eventhandler, party):
        '''Battle class constructor.

        args:
            clock: Pygame Clock
            renderer: Renderer object
            eventhandler: EventHandler object
            party: list; list of party members available for battle
        '''
        self._clock = clock
        self._renderer = renderer
        self._eventhandler = eventhandler
        self._keys = self._eventhandler.keys

        self._gfx = BattleGFX(party)
        self._turns = self._generate_turns()

        self._gameover = False
        self._victory = False

        self.demo = False

    def loop(self):
        '''The main battle loop.'''
        def execute_action(action, current, target):
            '''Executes an action, and relays info to either update the
            info panel or create DamageText buttons.

            args:
                action: str; action to be executed; skill or item identifier
                current: sprite; the character battlesprite whose turn it is
                target: sprite; target of the action
            '''
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
            '''Updates text to be blitted on the info panel.

            args:
                action: str; current action
                current: sprite; character whose turn it is
                target: sprite; target of the action
            '''
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
            '''Decreases the turn counter for every character. Sets count to -1 if
            character is not alive.
            '''
            for char in self._turns:
                if not char.alive():
                    self._turns[char] = -1
                if self._turns[char] > 0:
                    self._turns[char] -= 1

        def check_turn():
            '''Checks whose turn it is, and resets the counter if it hits 0.

            return:
                char: sprite; character whose turn is next or
                    None if no counters have hit zero
            '''
            for char in self._turns:
                if self._turns[char] == 0:
                    self._turns[char] = char.character.set_tick_speed()
                    return char
            return None

        def check_game_over():
            '''Checks if the any sprites are alive in either the party
            or enemy group. Sets the gameover and victory values accordingly.
            '''
            if not bool(self._gfx.enemies):
                self._gameover = True
                self._victory = True

            if not bool(self._gfx.party):
                self._gameover = True

        def get_current(queue):
            '''Returns the character who has their turn next.

            args:
                queue: deque; container for the current turn order

            return:
                current: sprite
            '''
            while True:
                current = queue.popleft()
                if current.character.alive:
                    return current

        def update():
            '''Updates the game state and display.'''
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
            if self._keys.PAUSE:
                self._pause()
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
        '''Loop for handling player action.

        args:
            current: sprite; party member whose turn it is

        return:
            action: str; skill or item identifier (None if player closes the window)
            target: sprite; target of the action (None if player closes the window)
        '''
        def set_menu_stack(current):
            '''Creates a menu stack to handle moving between menus.

            args:
                current: sprite

            return:
                stack: list; stack containing the current character's main menu
            '''
            stack = []
            self._reset_menus()
            for char in self._gfx.menus:
                if char == current:
                    main_menu = self._gfx.menus[char]['main']
                    main_menu.active = True
                    stack.append(main_menu)
            return stack

        def get_active_menu():
            '''Returns the menu that is currently active. If no menus are
            active, returns None.
            '''
            for char in self._gfx.menus:
                for menu in self._gfx.menus[char].values():
                    if menu.active:
                        return menu
            return None

        def set_active_menu(current, menu_type):
            '''Sets the current active menu.

            args:
                current: sprite
                menu_type: str; either main, skill, magic or item
            '''
            for char in self._gfx.menus:
                if char == current:
                    self._gfx.menus[char][menu_type].active = True

        def check_menu(menu_stack):
            '''Checks if the current active menu is in the menu stack.

            args:
                menu_stack: list; stack of menus

            return:
                menu: Menu object (or None)
            '''
            menu = get_active_menu()
            if menu is not None:
                if menu not in menu_stack:
                    menu_stack.append(menu)

            return menu

        def check_action(menu, menu_stack, current):
            '''Handles the player action.

            args:
                menu: Menu object; menu that is currently active
                menu_stack: list
                current: sprite

            return:
                info: str; instructions for how to update the info panel
                action: str; action to be executed
            '''
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
            '''Calls the target selection method, and either returns the target or sets the
            previous menu active if player did not choose a target.

            args:
                current: sprite
                menu_stack: list

            return:
                target: sprite
                name: str; name of the target
            '''
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
            '''Updates the sprites and keys, and renders everything on screen.

            args:
                current: sprite
                menu_stack: list
            '''
            self._gfx.update_sprites()
            self._render(current, menu_stack)
            self._keys.reset_keys()
            self._clock.tick(FPS)

        def update_info(current, info):
            '''Updates the information to be displayed on the info panel.

            args:
                current: sprite;
                info: str
            '''
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
            if self._keys.PAUSE:
                self._pause()
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
        '''Renders everything and updates the display. If it's the
        player's turn, takes the current character sprite and its
        menu_stack as arguments.
        '''
        self._gfx.render(self._renderer, current)
        if menu_stack is not None:
            for menu in menu_stack:
                menu.draw(self._renderer)
        self._gfx.draw_cursor(self._renderer)
        self._renderer.update_display()

    def _check_events(self):
        '''Looks for user input and changes the Keys object accordingly.'''
        self._eventhandler.check_input()

    def _generate_turns(self):
        '''Generates a turn count for battle participants.

        return:
            turns: dict; key: sprite, value: int (count until next turn)
        '''
        turns = {}
        for char in self._gfx.all:
            turns[char] = char.character.set_tick_speed()
        return turns

    def _reset_menus(self):
        '''Sets all menus and menu buttons to inactive/unpressed state,
        resets keys to False.
        '''
        for dct in self._gfx.menus.values():
            for menu in dct.values():
                menu.active = False
                menu.reset_buttons()
        self._keys.reset_keys()

    def _game_over(self):
        '''Loop for a game over.'''
        self._gfx.render_game_over(self._renderer, self._victory)
        self._renderer.update_display()

        while self._gameover:
            self._check_events()
            if self._keys.QUIT or self._keys.SELECT:
                self._gameover = False
            self._clock.tick(FPS)

    def _pause(self):
        '''Loop for a paused game.'''
        paused = True
        self._keys.reset_keys()
        self._gfx.render_pause_screen(self._renderer)
        self._renderer.update_display()

        while paused:
            self._check_events()
            if self._keys.QUIT or self._keys.PAUSE:
                paused = False
                if self._keys.PAUSE:
                    self._keys.reset_keys()
            self._clock.tick(FPS)
