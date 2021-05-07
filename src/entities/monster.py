from random import randint, choice

from database.db_util import load_monster_info, load_inventory
from entities.character import Character
from entities.items import Item

class Monster(Character):
    '''A Character subclass for monster entities.

    attr:
        info: namedtuple containing the monster's name, category and description
        default_action: skill object; monster's default attack
    '''
    def __init__(self, char_id):
        '''Constructor for the monster class. Initialises a Character object.

        args:
            char_id: str; a unique id for the monster
            conn: game database connection
        '''
        Character.__init__(self, char_id)

        self._info = load_monster_info(self._id)
        self._inventory = load_inventory(self._id)

        self._default_action = self._set_default_action()

    # def _load_info(self):
    #     '''Loads monster info from the game database.'''
    #     Info = namedtuple('Info', ['name', 'category', 'descr'])
    #     cur = self._conn.cursor()
    #     cur.execute(
    #         '''SELECT name, category, descr FROM Monsters
    #         WHERE id=?''', (self._id,)
    #     )
    #     return Info._make(tuple(cur.fetchone()))

    # def _load_inv(self):
    #     '''Loads monster's inventory from the game database.'''
    #     cur = self._conn.cursor()
    #     cur.execute(
    #         '''SELECT item_id, qty FROM Inventory
    #         WHERE char_id=?''', (self._id,)
    #     )
    #     rows = cur.fetchall()
    #     for row in rows:
    #         item_id, qty = row[0], row[1]
    #         new_item = Item(item_id, self._conn)
    #         self._inventory[item_id] = [new_item, qty]

    def _set_default_action(self):
        '''Sets the default action in battle.'''
        for skill_id, skill in self._skills.items():
            if skill.mp_cost == 0:
                return skill_id
        return None

    def set_tick_speed(self):
        '''Sets the tick speed for the monster in battle.
        Dependable on the character's agility stat.
        '''
        rand = randint(-3, 3)
        return 100 // (self._stats.agi + rand) * 3

    def make_decision(self, target_list):
        '''Simple AI for making decisions in battle.

        args:
            target_list: spritegroup; list of possible targets for battle action

        return:
            action: str; action to execute
            target: sprite; target for the action
        '''
        if self.curr_hp < self._stats.hp // 4:
            choices = [key for key, val in self._inventory.items() if val[1] > 0]
            try:
                action = choice(choices)
                target = self.battlesprite
            except IndexError:
                action = self._default_action
                target = choice(target_list)
        else:
            choices = [key for key in self._skills]
            action = choice(choices)
            if self.curr_mp < self._skills[action].mp_cost:
                action = self._default_action
            target = choice(target_list)
        return action, target
