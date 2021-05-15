class PlayerAction:
    '''A class for player action methods and functions.
    
    attr:
        curr: sprite; current character
        menu_stack: list; stack of current character's menus
    '''
    def __init__(self, menus, keys, target_cursor):
        '''PlayerAction class constructor.

        args:
            menus: dict; key: sprite, val: dict; character's menus
            keys: Keys object
            target_cursor: TargetCursor object
        '''
        self._menus = menus
        self._keys = keys
        self._cursor = target_cursor
        self._curr = None
        self._menu_stack = []

    def set_menu_stack(self):
        '''Creates a menu stack to handle moving between menus.'''
        self._menu_stack = []
        for char in self._menus:
            if char == self._curr:
                main_menu = self._menus[char]['main']
                main_menu.active = True
                self._menu_stack.append(main_menu)

    def _get_active_menu(self):
        '''Returns the menu that is currently active. If no menus are
        active, returns None.
        '''
        for char in self._menus:
            for menu in self._menus[char].values():
                if menu.active:
                    return menu
        return None

    def _set_active_menu(self, menu_type):
        '''Sets the current active menu.

        args:
            menu_type: str; either main, skill, magic or item
        '''
        for char in self._menus:
            if char == self._curr:
                self._menus[char][menu_type].active = True

    def check_menu(self):
        '''Checks if the current active menu is in the menu stack.

        return:
            menu: Menu object (or None)
        '''
        menu = self._get_active_menu()
        if menu is not None:
            if menu not in self._menu_stack:
                self._menu_stack.append(menu)

        return menu

    def check_action(self, menu):
        '''Handles the player action.

        args:
            menu: Menu object; menu that is currently active

        return:
            info: str; instructions for how to update the info panel
            action: str; action to be executed
        '''
        try:
            char = self._curr.character
        except AttributeError:
            return None, None

        info, action = menu.update(self._keys)
        if action is not None:
            if action == 'main' and len(self._menu_stack) > 1:
                self._menu_stack.pop()
                self._menu_stack[0].reset_buttons()
            self._keys.reset_keys()
            if action in self._menus[self._curr]:
                self._set_active_menu(action)
            elif action in char.skills or action in char.inventory:
                if (
                        action in char.skills and
                        char.get_skill_cost(action) > char.curr_mp
                    ):
                    info = 'Not enough MP!'
                elif (
                        action in char.inventory and
                        char.get_item_qty(action) == 0
                    ):
                    item = char.inventory[action][0].name.upper()
                    info = f'Not enough {item}s in inventory!'
                else:
                    self._cursor.active = True

        return info, action

    def check_target_selection(self):
        '''Sets the previous menu active if player did not choose a target.'''
        if self._keys.BACK:
            if len(self._menu_stack) > 1:
                menu = self._menu_stack.pop()
                menu.active = True
            else:
                self._set_active_menu('main')
                menu = self._get_active_menu()
            menu.update_buttons()
            menu.reset_buttons()

    def reset_cursors(self):
        '''Resets the menu cursors as well as target cursor.'''
        self._cursor.reset()
        for menu in self._menu_stack:
            menu.reset_cursor()
    
    def reset_menus(self):
        '''Sets all menus and menu buttons to inactive/unpressed state,
        resets keys to False.
        '''
        for dct in self._menus.values():
            for menu in dct.values():
                menu.active = False
                menu.reset_buttons()
        self._keys.reset_keys()

    def update_info(self, info):
        '''Updates the information to be displayed on the info panel.

        args:
            info: str
        '''
        text = ''
        try:
            char = self._curr.character
        except AttributeError:
            return text

        if (
                info in self._menus[self._curr] and
                info != 'attack'
            ):
            text = f' Choose {info}'
        elif info in char.skills:
            text = f' {char.skills[info].description}'
        elif info in char.inventory:
            text = f' {char.inventory[info][0].description}'
        elif info is not None:
            text = f' {info}'

        return text

    @property
    def menu_stack(self):
        '''Returns the menu stack.'''
        return self._menu_stack

    @property
    def current(self):
        '''Returns the current character battlesprite.'''
        return self._curr

    @current.setter
    def current(self, char):
        '''Sets the current character to another battlesprite.'''
        self._curr = char
