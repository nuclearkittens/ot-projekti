'''A module containing functions and methods for
preparing the demo.'''

import pygame as pg

from config import SCREEN_W, SCREEN_H
from database.db_util import load_inventory
from entities.monster import Monster
from entities.partymember import PartyMember

def initialise_demo_display():
    '''Initialises the Pygame display used in the demo.

    return:
        screen: Pygame display
    '''
    screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
    pg.display.set_caption('battle demo v666')
    return screen

def create_demo_party():
    '''Creates the party used in the demo.

    return:
        party: lst; list of party members available
    '''
    party = []
    party.append(PartyMember('ej'))
    party.append(PartyMember('witch'))
    inv = load_inventory('party')
    for member in party:
        member.inventory = inv

    return party

def create_demo_enemies():
    '''Creates enemies for the default demo battle.

    return:
        enemies: lst; list of Monster objects
    '''
    mons1 = Monster('ikorni')
    mons2 = Monster('ikorni')
    enemies = [mons1, mons2]
    return enemies
