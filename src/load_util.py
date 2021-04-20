import pygame
import json
import os.path
from constants import *

def load_img(filename, img_class, spritename=None):
    if img_class == 'background':
        relative_path = f'backgrounds/{filename}'
    elif img_class == 'sprite':
        relative_path = f'sprites/{spritename}/{filename}'
    return pygame.image.load(os.path.join(GFX_DIR, relative_path)).convert_alpha

def load_font(filename, size):
    return pygame.font.Font(os.path.join(SRC_DIR, filename), size)

def load_file(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

