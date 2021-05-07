import pygame as pg

from config import SCREEN_W, SCREEN_H
from database.db_util import load_inventory
# from entities.items import Item
from entities.monster import Monster
from entities.partymember import PartyMember

def initialise_demo_display():
    screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
    pg.display.set_caption('battle demo v666')
    return screen

def create_demo_party():
    # def create_party_inventory(conn):
    #     inv = {}
    #     cur = conn.cursor()
    #     cur.execute(
    #         '''SELECT item_id, qty FROM Inventory
    #         WHERE char_id=?''', ('party',)
    #     )
    #     rows = cur.fetchall()
    #     for row in rows:
    #         item_id, qty = row[0], row[1]
    #         new_item = Item(item_id, conn)
    #         inv[item_id] = [new_item, qty]
    #     return inv

    party = []
    party.append(PartyMember('ej'))
    party.append(PartyMember('witch'))
    inv = load_inventory('party')
    for member in party:
        member.inventory = inv

    return party

def create_demo_enemies():
    mons1 = Monster('ikorni')
    mons2 = Monster('ikorni')
    enemies = [mons1, mons2]
    return enemies
