import sqlite3
from collections import namedtuple

from config import DB_PATH
from entities.skills import Skill
from entities.items import Item

Stats = namedtuple('Stats', ['hp', 'mp', 'atk', 'defs', 'mag', 'mdef', 'agi'])
Res = namedtuple('Res', ['physical', 'fire', 'ice', 'lightning', 'wind', 'light', 'dark'])

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
    for row in rows:
        skill_id = row[0]
        new_skill = Skill(skill_id, conn)
        skills[skill_id] = new_skill

    conn.close()

    return skills