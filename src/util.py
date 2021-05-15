'''A module for utility functions, such as loading images.'''
import os.path
import pygame as pg

from config import DIRNAME, TILE_SIZE

def load_img(fname):
    '''Loads an image from game files.

    args:
        fname: str; relative path of the image to be loaded

    return:
        Surface; returns a per-pixel alpha conversion of
        the loaded image if the image exists, otherwise returns
        a default tile-sized surface
    '''
    file_path = os.path.join(DIRNAME, fname)
    if os.path.exists(file_path):
        return pg.image.load(file_path).convert_alpha()
    return pg.Surface(TILE_SIZE).convert()
