import os.path

SRC_DIR = os.path.dirname(__file__) # main directory
GFX_DIR = os.path.join(SRC_DIR, '/assets/gfx') # graphics
MON_DIR = os.path.join(SRC_DIR, '/assets/db/monsters') # monster files
SKILL_DIR = os.path.join(SRC_DIR, '/assets/db/skills')

TILE_SIZE = [32, 32]
SCREEN_W = 512
SCREEN_H = 448
NATIVE_RES = [512, 448]
SCALE = 1

FONT1 = 'assets/fonts/m5x7.ttf'

# colours
DARK_PURPLE = (66, 30, 66)
POWDER_ROSE = (201, 143, 143)
DARK_ROSE = (189, 113, 130)
HP_COLOUR = None
MP_COLOUR = None