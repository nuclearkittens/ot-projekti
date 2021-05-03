from random import randint

from entities.character import Character
from entities.items import Item

class PartyMember(Character):
    '''A Character subclass for playable characters.

    attr:
        name: str; party member's name
        lvl: int; party member's current level
    '''
    def __init__(self, char_id, conn):
        '''Constructor for the PartyMember class. Initialises a Character object.

        args:
            char_id: str; a unique id for the character
            conn: game database connection
        '''
        Character.__init__(self, char_id, conn)

        info = self._load_info()
        self._name = info[0]
        self._lvl = info[1]

    def _load_info(self):
        '''Loads character info from the game database.'''
        cur = self._conn.cursor()
        cur.execute('SELECT name, lvl FROM Party WHERE id=?', (self._id,))
        return cur.fetchone()

    def set_tick_speed(self):
        '''Sets the character's tick speed in battle.
        Dependable on the character's agility stat.
        '''
        rand = randint(-2, 2)
        return 100 // (self._stats.agi + rand) * 3

    def add_item(self, item_id, qty=1):
        '''Adds item to the character's inventory.

        args:
            item_id: str; id for the item to be added
            qty: int (default=1); quantity of items to add
        '''
        if item_id not in self._inventory:
            self._inventory[item_id] = [Item(item_id), qty]
        else:
            self._inventory[item_id][1] += qty
