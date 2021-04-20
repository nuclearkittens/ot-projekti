import pygame

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
        