from random import randint, choice

from database.db_util import load_monster_info, load_inventory
from entities.character import Character

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
        '''
        Character.__init__(self, char_id)

        self._info = load_monster_info(self._id)
        self._inventory = load_inventory(self._id)

        self._default_action = self._set_default_action()

    def _set_default_action(self):
        '''Sets the default action in battle.

        return:
            skill_id: str or None if character has no zero-cost skills
        '''
        for skill_id, skill in self._skills.items():
            if skill.mp_cost == 0:
                return skill_id
        return None

    def set_tick_speed(self):
        '''Sets the tick speed for the monster in battle.
        Dependable on the character's agility stat.

        return:
            tick speed (int)
        '''
        rand = randint(-3, 3)
        return 100 // (self._stats.agi + rand) * 3

    def make_decision(self, target_list):
        '''Simple AI for making decisions in battle. Returns default action if
        no items or MP are left.

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

    @property
    def name(self):
        '''Returns the name of the monster.'''
        return self._info.name

    @name.setter
    def name(self, new_name):
        '''Sets a new name for the monster.'''
        self._info._replace(name=new_name)
