import pygame
import random

from entity import Entity
from src.constants import DB_DIR
from src.load_util import load_file, load_img
from attacks import Attack
from entity import Entity

class Monster(Entity):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__()
        Entity.__init__()

        filename = f'{DB_DIR}/monsters/{self.name}.json'
        _load_data(filename)
        _load_imgs()

        self.main_img = self.imgs['idle1']
        self.rect = self.main_img.get_rect()

    def attack(self, target):
        n = random.randint(0, len(self.attacks)-1)
        dmg = 

