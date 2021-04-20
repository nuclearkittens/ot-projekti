import pygame

from entity import Entity
from src.constants import DB_DIR
from src.load_util import load_file, load_img
from attacks import Attack
from entity import Entity

class Player(Entity):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__()
        Entity.__init__()

        filename = f'{DB_DIR}/party/{self.name}.json'
        _load_data(filename)
        _load_imgs()

        self.main_img = self.imgs['idle1']
        self.rect = self.main_img.get_rect()