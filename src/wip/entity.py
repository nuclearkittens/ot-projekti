import pygame

from attacks import Attack
from src.constants import DB_DIR
from src.load_util import load_img, load_file

dirname = f'{DB_DIR}/monsters'

class Entity(pygame.sprite.Sprite):
    def __init__(self, name):
        self.name = name
        self.type = None
        self.descr = None

        self.max_hp = None
        self.curr_hp = None
        self.max_mp = None
        self.curr_mp = None

        self.strgth = None
        self.mag = None
        self.agi = None
        self.acc = None
        self.eva = None
        self.lck = None

        self.affinities = {}
        self.attacks = []
        self.loot = {}
        self.imgs = {
            'idle1': None,
            'idle2': None,
            'hurt': None,
            'dead': None
        }

    def _load_imgs(self):
        for k, v in self.imgs.items():
            filename = f'{k}.png'
            self.imgs[k] = load_img(filename, 'sprite', self.name)

    def _load_data(self, filename):
        temp_atks = []
        data = load_file(filename)
        for mon in data:
                self.name = data['name']
                self.type = data['type']
                self.descr = data['description']
            for stat in data['stats']:
                self.max_hp = stat['hp']
                self.curr_hp = self.max_hp
                self.max_mp = stat['mp']
                self.curr_mp = self.max_mp
                self.strgth = stat['str']
                self.mag = stat['mag']
                self.defs = stat['def']
                self.mdef = stat['mdef']
                self.agi = stat['agi']
                self.acc = stat['acc']
                self.eva = stat['eva']
                self.lck = stat['lck']
            for aff, val in data['elemental affinities'].items():
                self.affinities[aff] = val
            for typ, val in data['loot']:
                self.loot[typ] = val
            for atk in data['attacks']:
                temp_atks.append(atk)

        for atk in temp_atks:
            _fetch_attack(atk)

    def _fetch_attack(self, atk):
        self.attacks[atk] = Attack(atk)


        


