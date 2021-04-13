import pygame
import os

dirname = os.path.dirname(__file__)

def load_img(filename):
    return pygame.image.load(os.path.join(dirname, 'assets', filename)).convert_alpha()

def load_font(filename):
    return os.path.join(dirname, 'assets', filename)