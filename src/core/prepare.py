'''A module containing functions and methods for
preparing the demo.'''

import pygame as pg

from config import (
    SCREEN_W, SCREEN_H, SCREEN_CAPTION,
    DEMO_ENEMIES, DEMO_PARTY, PARTY_INV)
from database.db_util import load_inventory
from entities.monster import Monster
from entities.party_member import PartyMember

def initialise_demo_display():
    '''Initialises the Pygame display used in the demo.

    return:
        screen: Pygame display
    '''
    screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
    pg.display.set_caption(SCREEN_CAPTION)
    return screen

def create_demo_party():
    '''Creates the party used in the demo.

    return:
        party: list; list of party members available
    '''
    party = []
    for member in DEMO_PARTY:
        party.append(PartyMember(member))

    inv = load_inventory(PARTY_INV)
    for member in party:
        member.inventory = inv

    return party

def create_demo_enemies():
    '''Creates enemies for the default demo battle.

    return:
        enemies: list; list of Monster objects
    '''
    enemies = []
    for enem in DEMO_ENEMIES:
        enemies.append(Monster(enem))
    return enemies
