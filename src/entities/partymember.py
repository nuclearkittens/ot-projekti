from random import randint

from database.db_util import load_party_info
from entities.character import Character
from entities.items import Item

class PartyMember(Character):
    '''A Character subclass for playable characters.

    attr:
        name: str; party member's name
        lvl: int; party member's current level
    '''
    def __init__(self, char_id):
        '''Constructor for the PartyMember class. Initialises a Character object.

        args:
            char_id: str; a unique id for the character
        '''
        Character.__init__(self, char_id)

        info = load_party_info(self._id)
        self._name = info[0]
        self._lvl = info[1]

    def set_tick_speed(self):
        '''Sets the character's tick speed in battle.
        Dependable on the character's agility stat.

        return:
            tick speed: int
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

    @property
    def name(self):
        '''Returns the name of the party member.'''
        return self._name