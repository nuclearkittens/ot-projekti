from collections import namedtuple
from sqlite3 import OperationalError

from database.db_connection import get_db_connection
from entities.skills import Skill
from entities.items import Item

Stats = namedtuple('Stats', ['hp', 'mp', 'atk', 'defs', 'mag', 'mdef', 'agi'])
Res = namedtuple('Res', ['physical', 'fire', 'ice', 'lightning', 'wind', 'light', 'dark'])
MonsterInfo = namedtuple('MonsterInfo', ['name', 'category', 'descr'])
SkillInfo = namedtuple('SkillInfo', ['name', 'category', 'subcategory', 'description'])
SkillAttributes = namedtuple('SkillAttributes', [
        'element', 'hits', 'mp_cost', 'multiplier', 'crit_rate'])

def load_stats(char_id):
    '''Connects to the game database and fetches the characters stats.

    args:
        char_id: str
        db: str; path to game database, defaults to configured one

    return:
        stats: Stats object (namedtuple)
    '''
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            '''SELECT hp, mp, atk, defs,
            mag, mdef, agi FROM Stats
            WHERE char_id=?''', (char_id,)
        )
        stats = Stats._make(tuple(cur.fetchone()))
    except OperationalError:
        stats = None
    except TypeError:
        stats = None

    conn.close()

    return stats

def load_res(char_id):
    '''Connects to the game database and fetches the character's resistance
    to different elements.

    args:
        char_id: str
        db: str; path to game database, defaults to configured one

    return:
        res: Res object (namedtuple)
    '''
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            '''SELECT physical, fire, ice, lightning,
            wind, light, dark FROM Resistance
            WHERE char_id=?''', (char_id,)
        )

        res = Res._make(tuple(cur.fetchone()))
    except OperationalError:
        res = None
    except TypeError:
        res = None

    conn.close()

    return res

def load_skills(char_id):
    '''Connects to the game database and adds skills associated with character.

    args:
        char_id: str; a unique id for a character
        db: str; path to game database, defaults to configured one

    return:
        skills: dict; key: skill_id (str), val: skill (Skill object)'''
    conn = get_db_connection()
    cur = conn.cursor()
    skills = {}

    try:
        cur.execute(
            '''SELECT skill_id FROM CharSkills
            WHERE char_id=?''', (char_id,)
        )
    except OperationalError:
        conn.close()
        return skills

    rows = cur.fetchall()

    for row in rows:
        skill_id = row[0]
        new_skill = Skill(skill_id)
        skills[skill_id] = new_skill

    conn.close()

    return skills

def load_party_info(char_id):
    '''Loads character info from the game database.

    args:
        char_id: str
        db: str; path to game database, defaults to configured one

    return:
        info: SQLite Row object
    '''
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute('SELECT name, lvl FROM Party WHERE id=?', (char_id,))
        info = cur.fetchone()
    except OperationalError:
        info = None

    conn.close()
    return info

def load_monster_info(char_id):
    '''Loads monster info from the game database.

    args:
        char_id: str
        db: str; path to game database, defaults to configured one

    return:
        info: MonsterInfo object (namedtuple)
    '''
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            '''SELECT name, category, descr FROM Monsters
            WHERE id=?''', (char_id,)
        )
        info = MonsterInfo._make(tuple(cur.fetchone()))
    except OperationalError:
        info = None
    except TypeError:
        info = None

    conn.close()

    return info

def load_inventory(char_id):
    '''Loads character's default inventory from the game database.

    args:
        char_id: str
        db: str; path to game database, defaults to configured one

    return:
        inv: dict;
            key: item_id (str), val: item (Item object), qty: int; quantity
    '''
    conn = get_db_connection()
    cur = conn.cursor()
    inv = {}

    try:
        cur.execute(
            '''SELECT item_id, qty FROM Inventory
            WHERE char_id=?''', (char_id,)
        )
        rows = cur.fetchall()
    except OperationalError:
        conn.close()
        return inv

    conn.close()

    for row in rows:
        item_id, qty = row[0], row[1]
        new_item = Item(item_id)
        inv[item_id] = [new_item, qty]

    return inv

def load_item_info(item_id):
    '''Loads item info from the game database.

    args:
        item_id: str
        db: str; path to game database, defaults to configured one

    return:
        info: SQLite Row object
    '''
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute('SELECT name, descr FROM Items WHERE id=?', (item_id,))
        info = cur.fetchone()
    except OperationalError:
        info = None

    conn.close()
    return info

def load_item_effects(item_id):
    '''Loads item effects from the game database.

    args:
        item_id: str
        db: str; path to game database, defaults to configured one

    return:
        effects: lst (of tuples)
    '''
    conn = get_db_connection()
    cur = conn.cursor()
    effects = []

    try:
        cur.execute(
            '''SELECT E.effect, E.target_attr, E.amount
            FROM Effects E, ItemEffects I
            WHERE E.id=I.effect_id AND I.item_id=?''', (item_id,)
            )
    except OperationalError:
        conn.close()
        return effects

    rows = cur.fetchall()

    for row in rows:
        effects.append(tuple(row))

    conn.close()

    return effects

def load_skill_info(skill_id):
    '''Loads skill info from the game database.

    args:
        skill_id: str
        db: str; path to game database, defaults to configured one

    return:
        info: SkillInfo object (namedtuple)
    '''
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            '''SELECT name, category, subcategory, descr
            FROM Skills WHERE Skills.id=?''', (skill_id,)
        )
        info = SkillInfo._make(tuple(cur.fetchone()))
    except OperationalError:
        info = None
    except TypeError:
        info = None

    conn.close()

    return info

def load_skill_attr(skill_id):
    '''Loads skill attributes from the game database.

    args:
        skill_id: str
        db: str; path to game database, defaults to configured one

    return:
        attr: SkillAttributes object (namedtuple)
    '''
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            '''SELECT element, hits, mp_cost, multiplier, crit_rate
            FROM Skills WHERE Skills.id=?''', (skill_id,)
        )
        attr = SkillAttributes._make(tuple(cur.fetchone()))
    except OperationalError:
        attr = None
    except TypeError:
        attr = None

    conn.close()

    return attr
