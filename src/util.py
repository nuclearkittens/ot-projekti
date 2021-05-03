# import json
import os.path
import pygame as pg

from config import DIRNAME

def load_img(path):
    return pg.image.load(os.path.join(DIRNAME, path)).convert_alpha()

# def load_file(path):
#     with open(path) as json_file:
#         data = json.load(json_file)
#     return data
