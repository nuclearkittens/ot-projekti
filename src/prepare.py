import pygame as pg

from config import SCREEN_W, SCREEN_H
from entities.items import Item
from entities.monster import Monster
from entities.partymember import PartyMember

def initialise_demo_display():
    screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
    pg.display.set_caption('battle demo v666')
    return screen

def create_demo_party(conn):
    def create_party_inventory(conn):
        inv = {}
        cur = conn.cursor()
        cur.execute(
            '''SELECT item_id, qty FROM Inventory
            WHERE char_id=?''', ('party',)
        )
        rows = cur.fetchall()
        for row in rows:
            item_id, qty = row[0], row[1]
            new_item = Item(item_id, conn)
            inv[item_id] = [new_item, qty]
        return inv

    party = []
    party.append(PartyMember('ej', conn))
    party.append(PartyMember('witch', conn))
    inv = create_party_inventory(conn)
    for member in party:
        member.inventory = inv

    return party

def create_demo_enemies(conn):
    mons1 = Monster('ikorni', conn)
    mons2 = Monster('ikorni', conn)
    enemies = [mons1, mons2]
    return enemies
