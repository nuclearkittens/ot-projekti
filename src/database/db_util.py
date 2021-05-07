import sqlite3
from collections import namedtuple

from config import DB_PATH
from entities.skills import Skill
from entities.items import Item

Stats = namedtuple('Stats', ['hp', 'mp', 'atk', 'defs', 'mag', 'mdef', 'agi'])
Res = namedtuple('Res', ['physical', 'fire', 'ice', 'lightning', 'wind', 'light', 'dark'])
MonsterInfo = namedtuple('MonsterInfo', ['name', 'category', 'descr'])
SkillInfo = namedtuple('SkillInfo', ['name', 'category', 'subcategory', 'description'])
SkillAttributes = namedtuple('SkillAttributes', [
        'element', 'hits', 'mp_cost', 'multiplier', 'crit_rate'])

def get_db_connection(db=DB_PATH):
    '''Returns connection to the game database.'''
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

def load_stats(char_id):
    '''Connects to the game database and fetches the characters stats.

    return: Stats(namedtuple)
    '''
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        '''SELECT hp, mp, atk, defs,
        mag, mdef, agi FROM Stats
        WHERE char_id=?''', (char_id,)
    )

    stats = Stats._make(tuple(cur.fetchone()))
    conn.close()

    return stats

def load_res(char_id):
    '''Connects to the game database and fetches the character's resistance
    to different elements.

    return: Res(namedtuple)
    '''
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        '''SELECT physical, fire, ice, lightning,
        wind, light, dark FROM Resistance
        WHERE char_id=?''', (char_id,)
    )

    res = Res._make(tuple(cur.fetchone()))
    conn.close()

    return res

def load_skills(char_id):
    '''Connects to the game database and adds skills associated with character.'''
    conn = get_db_connection()
    cur = conn.cursor()
    skills = {}
    cur.execute(
        '''SELECT skill_id FROM CharSkills
        WHERE char_id=?''', (char_id,)
    )
    rows = cur.fetchall()
    conn.close()
    for row in rows:
        skill_id = row[0]
        new_skill = Skill(skill_id)
        skills[skill_id] = new_skill

    # conn.close()

    return skills

def load_party_info(char_id):
    '''Loads character info from the game database.'''
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, lvl FROM Party WHERE id=?', (char_id,))
    info = cur.fetchone()
    conn.close()
    return info

def load_monster_info(char_id):
    '''Loads monster info from the game database.'''
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        '''SELECT name, category, descr FROM Monsters
        WHERE id=?''', (char_id,)
    )

    info = MonsterInfo._make(tuple(cur.fetchone()))
    return info

def load_inventory(char_id):
    conn = get_db_connection()
    cur = conn.cursor()
    inv = {}

    cur.execute(
        '''SELECT item_id, qty FROM Inventory
        WHERE char_id=?''', (char_id,)
    )
    rows = cur.fetchall()
    conn.close()
    for row in rows:
        item_id, qty = row[0], row[1]
        new_item = Item(item_id)
        inv[item_id] = [new_item, qty]
    return inv

def load_item_info(item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, descr FROM Items WHERE id=?', (item_id,))
    info = cur.fetchone()
    conn.close()
    return info

def load_item_effects(item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    effects = []
    cur.execute(
        '''SELECT E.effect, E.target_attr, E.amount
        FROM Effects E, ItemEffects I
        WHERE E.id=I.effect_id AND I.item_id=?''', (item_id,)
        )
    rows = cur.fetchall()
    for row in rows:
        effects.append(tuple(row))

    conn.close()
    return effects

def load_skill_info(skill_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        '''SELECT name, category, subcategory, descr
        FROM Skills WHERE Skills.id=?''', (skill_id,)
    )
    info = SkillInfo._make(tuple(cur.fetchone()))
    conn.close()
    return info

def load_skill_attr(skill_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        '''SELECT element, hits, mp_cost, multiplier, crit_rate
        FROM Skills WHERE Skills.id=?''', (skill_id,)
    )
    attr = SkillAttributes._make(tuple(cur.fetchone()))
    conn.close()
    return attr
