from database.db_util import load_stats, load_res, load_skills
from entities.battle_sprite import BattleSprite

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
        battlesprite: BattleSprite object; used to represent the character in battle
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
        '''Uses item if it is in character's inventory, otherwise returns ValueError.
        Also performs a HP check for the target.

        args:
            item_id: str; id for the item to be used
            target: character object; the character the item is used on.

        return:
            info: list; list for creating a DamageText object
        '''
        if item_id in self._inventory:
            if self._inventory[item_id][1] > 0:
                self._inventory[item_id][1] -= 1
                info = self._inventory[item_id][0].use(target)
                target.check_hp()
                return info
            return f'Not enough {self._inventory[item_id][0].name.upper()}s in inventory!'
        return ValueError(f'no item "{item_id}" in inventory!')

    def use_skill(self, skill_id, target):
        '''Uses skill if character has enough MP to execute it,
        otherwise gives an error message. Reduces user's MP, and
        sets both user's and target's animation statuses accordingly.

        args:
            skill_id: str; id for the skill to be used
            target: Character object; the character the skill is used on.

        return:
            info: list; info for creating a DamageText object
        '''
        if skill_id not in self._skills:
            return f'{self._id} does not know skill {skill_id}!'
        if self._skills[skill_id].mp_cost > self.curr_mp:
            return 'Not enough MP!'
        self.curr_mp -= self._skills[skill_id].mp_cost
        info = self._skills[skill_id].use(self, target)
        self.battlesprite.attack()
        target.battlesprite.hurt()
        return info

    def get_item_qty(self, item_id):
        '''Returns how many of the specified item the character has left.'''
        try:
            return self._inventory[item_id][1]
        except KeyError:
            return f'no item {item_id} in inventory!'

    def get_skill_cost(self, skill_id):
        '''Returns the MP cost of the specified skill.'''
        try:
            return self._skills[skill_id].mp_cost
        except KeyError:
            return f'{self._id} does not know skill {skill_id}!'

    # gotta do sth abt all these properties, fix this later!
    @property
    def id(self):
        '''Returns the character's identifier.'''
        return self._id

    @property
    def max_hp(self):
        '''Returns the character's HP cap.'''
        return self._stats.hp

    @property
    def max_mp(self):
        '''Returns the character's MP cap.'''
        return self._stats.mp

    @property
    def atk(self):
        '''Returns the character's physical attack strength.'''
        return self._stats.atk

    @property
    def defs(self):
        '''Returns the character's physical defense.'''
        return self._stats.defs

    @property
    def mag(self):
        '''Returns the character's magical attack strength.'''
        return self._stats.mag

    @property
    def mdef(self):
        '''Returns the character's magical defense.'''
        return self._stats.mdef

    @property
    def res(self):
        '''Character's resistance to different attack types.

        return:
            dict: key: element (str), value: resistance (float)
        '''
        return self._res._asdict()

    @property
    def skills(self):
        '''Returns a dictionary of character's skills.'''
        return self._skills

    @property
    def inventory(self):
        '''Returns the character's inventory.'''
        return self._inventory

    @inventory.setter
    def inventory(self, new_inv):
        '''Replaces the character's inventory with a new one.

        args:
            new_inv: dict
        '''
        self._inventory = new_inv
