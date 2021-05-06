from database.db_util import load_stats, load_res, load_skills
from entities.skills import Skill
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
        curr_hp: character's current health points
        curr_mp: character's current magic points
    '''
    def __init__(self, char_id, conn):
        '''Character class constructor.
        args:
            char_id: str; a unique character id
            conn: connection to the game database
        '''
        self._id = char_id
        self._conn = conn

        self._stats = load_stats(self._id)
        self._res = load_res(self._id)
        self._skills = load_skills(self._id)
        self._inventory = {}

        # self._load_skills()

        self.battlesprite = BattleSprite(self)

        self.alive = True
        self.curr_hp = self._stats.hp
        self.curr_mp = self._stats.mp

    # def _load_stats(self):
    #     '''Connects to the game database and fetches the characters stats.

    #     return: Stats(namedtuple)
    #     '''
    #     # Stats = namedtuple('Stats', ['hp', 'mp', 'atk', 'defs', 'mag', 'mdef', 'agi'])
    #     # cur = self._conn.cursor()
    #     # cur.execute(
    #     #     '''SELECT hp, mp, atk, defs,
    #     #     mag, mdef, agi FROM Stats
    #     #     WHERE char_id=?''', (self._id,)
    #     # )
    #     # return Stats._make(tuple(cur.fetchone()))
    #     return load_character_stats(self._id)

    # def _load_res(self):
    #     '''Connects to the game database and fetches the character's resistance
    #     to different elements.

    #     return: Res(namedtuple)
    #     '''
    #     # Res = namedtuple('Res', ['physical', 'fire', 'ice', 'lightning', 'wind', 'light', 'dark'])
    #     # cur = self._conn.cursor()
    #     # cur.execute(
    #     #     '''SELECT physical, fire, ice, lightning,
    #     #     wind, light, dark FROM Resistance
    #     #     WHERE char_id=?''', (self._id,)
    #     # )
    #     return load_character_resistance(self._id)

    def _load_info(self):
        '''Hook for loading other character data; overwritten in subclasses.'''
        pass

    # def _load_skills(self):
    #     '''Connects to the game database and adds skills associated with character.'''
    #     cur = self._conn.cursor()
    #     cur.execute(
    #         '''SELECT skill_id FROM CharSkills
    #         WHERE char_id=?''', (self._id,)
    #     )
    #     rows = cur.fetchall()
    #     for row in rows:
    #         skill_id = row[0]
    #         new_skill = Skill(skill_id, self._conn)
    #         self._skills[skill_id] = new_skill

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
        '''
        if item_id in self._inventory:
            if self._inventory[item_id][1] > 0:
                self._inventory[item_id][1] -= 1
                self._inventory[item_id][0].use(target)
                target.check_hp()
            else:
                raise ValueError(f'not enough {item_id}s in inventory!')
        else:
            raise ValueError(f'no item "{item_id}" in inventory!')

    def use_skill(self, skill_id, target):
        '''Uses skill if character has enough MP to execute it,
        otherwise raises ValueError. Reduces user's MP, and
        sets both user's and target's animation statuses accordingly.

        args:
            skill_id: str; id for the skill to be used
            target: character object; the character the skill is used on.
        '''
        if self._skills[skill_id].mp_cost > self.curr_mp:
            raise ValueError('not enough mp!')
        self.curr_mp -= self._skills[skill_id].mp_cost
        self._skills[skill_id].use(self, target)
        self.battlesprite.attack()
        target.battlesprite.hurt()

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

            return: dict: key: element (str), value: resistance (float)
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
