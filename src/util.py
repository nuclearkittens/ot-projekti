import os.path
import json
import pygame as pg

from techniques import OffensiveSkill
from magic import BlackMagic
from item import Item
from config import DIRNAME, ITEMS_DB, ATKS_DB, BLK_MAG_DB

def load_file(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

def load_img(relative_path):
    return pg.image.load(os.path.join(DIRNAME, relative_path)).convert_alpha()

def fetch_item(item):
    data = load_file(ITEMS_DB)
    if item in data:
        data = data[item]
        return Item(data['name'], data['category'], data['descr'], data['effects'])
    else:
        raise KeyError

def fetch_skill(skill):
    data = load_file(ATKS_DB)
    if skill in data:
        data = data[skill]
        return OffensiveSkill(
            data['name'], data['descr'], data['element'],
            data['effects'], data['hits'], data['mp_cost'],
            data['multiplier'], data['crit_rate']
            )
    else:
        raise KeyError

def fetch_blk_spell(skill):
    data = load_file(BLK_MAG_DB)
    if skill in data:
        data = data[skill]
        return BlackMagic(
            data['name'], data['descr'], data['element'],
            data['effects'], data['hits'], data['mp_cost'],
            data['multiplier'], data['crit_rate']
            )
    else:
        raise KeyError
