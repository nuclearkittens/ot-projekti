'''A module for utility functions, such as loading images.'''
import os.path
import pygame as pg

from config import DIRNAME, TILE_SIZE

def load_img(path):
    '''Loads an image from game files.

    args:
        path: str; relative path of the image to be loaded

    return:
        Surface; returns a per-pixel alpha conversion of
        the loaded image if the image exists, otherwise returns
        a default tile-sized surface
    '''
    filename = os.path.join(DIRNAME, path)
    if os.path.exists(filename):
        return pg.image.load(filename).convert_alpha()
    return pg.Surface(TILE_SIZE).convert()
