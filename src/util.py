# import json
import os.path
import pygame as pg

from config import DIRNAME, TILE_SIZE

def load_img(path):
    filename = os.path.join(DIRNAME, path)
    if os.path.exists(filename):
        return pg.image.load(filename).convert_alpha()
    return pg.Surface(TILE_SIZE)

# def load_file(path):
#     with open(path) as json_file:
#         data = json.load(json_file)
#     return data
