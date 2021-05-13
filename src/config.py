'''Module for specifying the environmental variables.

TO DO: Create an actual configuration file.
'''
import os
from dotenv import load_dotenv

DIRNAME = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(DIRNAME, '..', '.env'))
except FileNotFoundError:
    pass

DB_NAME = os.getenv('DB_NAME') or 'gamedata.db'
DB_CMDS = os.getenv('DB_CMDS') or 'init_commands.sql'
DB_PATH = os.path.join(DIRNAME, 'assets/db', DB_NAME)
DB_CMDS_PATH = os.path.join(DIRNAME, 'assets/db', DB_CMDS)

DARK_PURPLE = (66, 30, 66)
POWDER_ROSE = (201, 143, 143)
DARK_ROSE = (189, 113, 130)
HP_GREEN = (112, 161, 143)
HP_YELLOW = (230, 207, 161)
HP_RED = DARK_ROSE
MP_BLUE = (99, 124, 143)

SCALE = 1 # has to be integer
NATIVE_RESOLUTION = (512, 448)

SCREEN_W = 512 * SCALE
SCREEN_H = 448 * SCALE

TILE_SIZE = (32 * SCALE, 32 * SCALE)

FPS = 60

FONT = os.path.join(DIRNAME, 'assets/fonts/m5x7.ttf')
FONT_SIZE = 32 * SCALE
MIN_FONT_SIZE = 4

BAR_W = 64 * SCALE
BAR_H = 4 * SCALE

MENU_CURSOR = '>'
TARGET_CURSOR = '<'
CURSOR_SIZE = 32 * SCALE

BATTLE_BG = os.path.join(DIRNAME, 'assets/gfx/backgrounds/battlebg1.png')
