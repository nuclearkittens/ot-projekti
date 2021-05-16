'''A module for utility functions, such as loading images.'''
import os.path
import pygame as pg

from config import DIRNAME, TILE_SIZE, SCALE

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
        img = pg.image.load(file_path)
        if SCALE > 1:
            new_w = img.get_width() * SCALE
            new_h = img.get_height() * SCALE
            img = pg.transform.scale(img, (new_w, new_h))
        return img.convert_alpha()
    return pg.Surface(TILE_SIZE).convert()
