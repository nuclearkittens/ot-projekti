from database.db_util import load_stats, load_res, load_skills
from entities.battlesprite import BattleSprite

class Character:
    '''Main class for character objects.

    attr:
        stats: character stats stored as a namedtuple;
            hp: base (maximum) value for health points
            mp: base (maximum) value for magic points
            atk: physical strength
            defs: defense against physical attacks
            mag: magical strength
            mdef: defense against magical attacks
            agi: agility; determines how quickly character acts in a battle
        res: character's resistance to different attack types stored as a namedtuple;
            acceptable values for each element:
            -1.0: absorb element
            0.0: nullify element
            0.5: strong against element
            1.0: normal damage
            1.5: weak against element
        skills: dict; character's skills
        inventory: dict; character's items
        alive: bool; tells whether the character is alive or knocked out
        curr_hp: int; character's current health points
        curr_mp: int; character's current magic points
    '''
    def __init__(self, char_id):
        '''Character class constructor.
        args:
            char_id: str; a unique character id
        '''
        self._id = char_id

        self._stats = load_stats(self._id)
        self._res = load_res(self._id)
        self._skills = load_skills(self._id)
        self._inventory = {}

        self.battlesprite = BattleSprite(self)

        self.alive = True
        self.curr_hp = self._stats.hp
        self.curr_mp = self._stats.mp

    def check_hp(self):
        '''Checks that the current HP value is between 0 and maximum HP.
        Sets alive status to false and kills battlesprite if HP < 0.
        '''
        if self.curr_hp > self._stats.hp:
            self.curr_hp = self._stats.hp
        elif self.curr_hp < 0:
            self.curr_hp = 0
        if self.curr_hp == 0:
            self.alive = False
            self.battlesprite.dead()

    def check_mp(self):
        '''Checks that the current MP value doesn't exceed the maximum.'''
        if self.curr_mp > self._stats.mp:
            self.curr_mp = self._stats.mp

    def use_item(self, item_id, target):
        '''Uses item if it is in character's inventory, otherwise raises ValueError.
        Also performs a HP check for the target.

        args:
            item_id: str; id for the item to be used
            target: character object; the character the item is used on.

        return:
            info: lst; list for creating a DamageText object
        '''
        if item_id in self._inventory:
            if self._inventory[item_id][1] > 0:
                self._inventory[item_id][1] -= 1
                info = self._inventory[item_id][0].use(target)
                target.check_hp()
                return info
            raise ValueError(f'not enough {item_id}s in inventory!')
        raise ValueError(f'no item "{item_id}" in inventory!')

    def use_skill(self, skill_id, target):
        '''Uses skill if character has enough MP to execute it,
        otherwise raises ValueError. Reduces user's MP, and
        sets both user's and target's animation statuses accordingly.

        args:
            skill_id: str; id for the skill to be used
            target: character object; the character the skill is used on.

        return:
            info: lst; info for creating a DamageText object
        '''
        if self._skills[skill_id].mp_cost > self.curr_mp:
            raise ValueError('not enough mp!')
        self.curr_mp -= self._skills[skill_id].mp_cost
        info = self._skills[skill_id].use(self, target)
        self.battlesprite.attack()
        target.battlesprite.hurt()
        return info

    def get_item_qty(self, item_id):
        '''Returns how many of the specified item the character has left.'''
        return self._inventory[item_id][1]

    # gotta do sth abt all these properties, fix this later!
    @property
    def id(self):
        '''property: character id (str)'''
        return self._id

    @property
    def max_hp(self):
        '''property: character's HP cap (int)'''
        return self._stats.hp

    @property
    def max_mp(self):
        '''property: character's MP cap (int)'''
        return self._stats.mp

    @property
    def atk(self):
        '''property: character's physical attack strength (int)'''
        return self._stats.atk

    @property
    def defs(self):
        '''property: character's physical attack defense (int)'''
        return self._stats.defs

    @property
    def mag(self):
        '''property: character's magical attack strength (int)'''
        return self._stats.mag

    @property
    def mdef(self):
        '''property: character's magical defense (int)'''
        return self._stats.mdef

    @property
    def res(self):
        '''property: character's resistance to different attack types

        return:
            dict: key: element (str), value: resistance (float)
        '''
        return self._res._asdict()

    @property
    def skills(self):
        '''property: character's skills (dict)'''
        return self._skills

    @property
    def inventory(self):
        '''property: character's inventory (dict)'''
        return self._inventory

    @inventory.setter
    def inventory(self, new_inv):
        '''setter: replace character's inventory with a new one

        args:
            new_inv: dict
        '''
        self._inventory = new_inv
