from collections import deque

from config import FPS
from combat.player_action import PlayerAction
from ui.battle_graphics import BattleGFX

class Battle:
    '''Class for handling all the battle action.

    attr:
        keys: Keys object
        gfx: BattleGFX object; handles the graphic elements of battle
        plr: PlayerAction object; handles player action in battle
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
        self._plr = PlayerAction(
            self._gfx.menus, self._keys,
            self._gfx.target_cursor
        )
        self._turns = self._generate_turns()

        self._gameover = False
        self._victory = False

    def loop(self):
        '''The main battle loop.'''
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
            current = self._check_turn()
            if current is not None:
                queue.append(current)
            if cooldown > wait:
                cooldown = 0
                current = self._get_current(queue)
                if current in self._gfx.party:
                    action, target = self._player_loop(current)
                elif current in self._gfx.enemies:
                    action, target = current.character.make_decision(self._gfx.party.sprites())
                self._execute_action(action, current, target)
                self._update_info(action, current, target)
                # self._reset_menus()
            cooldown += 1
            self._update()
            self._check_game_over()
            if self._gameover:
                running = False

        self._game_over()

    def _generate_turns(self):
        '''Generates a turn count for battle participants.

        return:
            turns: dict; key: sprite, value: int (count until next turn)
        '''
        turns = {}
        for char in self._gfx.all:
            turns[char] = char.character.set_tick_speed()
        return turns

    def _get_current(self, queue):
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

    def _check_events(self):
        '''Looks for user input and changes the Keys object accordingly.'''
        self._eventhandler.check_input()

    def _check_turn(self):
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

    def _check_game_over(self):
        '''Checks if the any sprites are alive in either the party
        or enemy group. Sets the gameover and victory values accordingly.
        '''
        if not bool(self._gfx.enemies):
            self._gameover = True
            self._victory = True

        if not bool(self._gfx.party):
            self._gameover = True

    def _choose_target(self):
        '''Calls the target selection method, and returns the target.

        return:
            target: sprite (or None)
            name: str; name of the target (or None)
        '''
        return self._gfx.target_cursor.choose_target(self._keys, self._gfx.all)

    def _execute_action(self, action, current, target):
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

    def _tick(self):
        '''Decreases the turn counter for every character. Sets count to -1 if
        character is not alive.
        '''
        for char in self._turns:
            if not char.alive():
                self._turns[char] = -1
            if self._turns[char] > 0:
                self._turns[char] -= 1

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

    def _render_info(self, info):
        try:
            self._gfx.update_info(info)
        except UnboundLocalError:
            pass

    def _update(self, player=False):
        '''Updates the game state and display, plus updates menus
        if player's turn and turn count if not.
        
        args:
            player: bool; True if it is player's turn
        '''
        curr = self._plr.current if player else None
        stack = self._plr.menu_stack if player else None

        if not player:
            self._gfx.update_target_list()
            self._tick()
        self._gfx.update_sprites()
        self._render(curr, stack)
        self._keys.reset_keys()
        self._clock.tick(FPS)

    def _update_info(self, action, current, target):
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

    def _player_loop(self, current):
        '''Loop for handling player action.

        args:
            current: sprite; party member whose turn it is

        return:
            action: str; skill or item identifier (None if player closes the window)
            target: sprite; target of the action (None if player closes the window)
        '''

        self._plr.reset_menus()
        self._plr.current = current
        self._plr.set_menu_stack()
        action = None
        player = True

        while player:
            self._check_events()
            if self._keys.QUIT:
                return None, None
            if self._keys.PAUSE:
                self._pause()
            menu = self._plr.check_menu()
            if menu is not None:
                info, action = self._plr.check_action(menu)
                text = self._plr.update_info(info)
                self._render_info(text)
            target, name = self._choose_target()
            self._plr.check_target_selection()
            if name is not None:
                text = self._plr.update_info(info)
                self._render_info(text)
            if target is not None:
                player = False
                # self._plr.reset_menus()
            self._update(player)

        self._plr.reset_menus()
        self._plr.reset_cursors()

        return action, target

    def _game_over(self):
        '''Loop for a game over.'''
        self._gfx.render_game_over(self._renderer, self._victory)
        self._renderer.update_display()

        while self._gameover:
            self._check_events()
            if self._keys.QUIT or self._keys.SELECT:
                self._gameover = False
            self._clock.tick(FPS)
