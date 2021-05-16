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

DEMO_PARTY = (
    [elem for elem in os.getenv('DEMO_PARTY').split(',')]
    or ['ej', 'witch']
    )
DEMO_ENEMIES = (
    [elem for elem in os.getenv('DEMO_ENEMIES').split(',')]
    or ['ikorni', 'ikorni']
    )
PARTY_INV = os.getenv('PARTY_INV') or 'party'

DARK_PURPLE = (
    tuple(int(val) for val in os.getenv('DARK_PURPLE').split(','))
    or (66, 30, 66)
    )
POWDER_ROSE = (
    tuple(int(val) for val in os.getenv('POWDER_ROSE').split(','))
    or (201, 143, 143)
    )
DARK_ROSE = (
    tuple(int(val) for val in os.getenv('DARK_ROSE').split(','))
    or (189, 113, 130)
    )
HP_GREEN = (
    tuple(int(val) for val in os.getenv('HP_GREEN').split(','))
    or (112, 161, 143)
    )
HP_YELLOW = (
    tuple(int(val) for val in os.getenv('HP_YELLOW').split(','))
    or (230, 207, 161)
    )
HP_RED = (
    tuple(int(val) for val in os.getenv('DARK_ROSE').split(','))
    or (189, 113, 130)
    )
MP_BLUE = (
    tuple(int(val) for val in os.getenv('MP_BLUE').split(','))
    or (99, 124, 143)
    )

SCALE = int(os.getenv('SCALE')) or 1 # has to be integer
NATIVE_RESOLUTION = (
    tuple(int(val) for val in os.getenv('NATIVE_RESOLUTION').split(','))
    or (512, 448)
    )

SCREEN_W = (int(os.getenv('SCREEN_W')) or 512) * SCALE
SCREEN_H = (int(os.getenv('SCREEN_H')) or 448) * SCALE
SCREEN_CAPTION = 'fractured loop: battle demo'

TILE = (int(os.getenv('TILE')) or 32) * SCALE
TILE_SIZE = (TILE, TILE)

FPS = int(os.getenv('FPS')) or 60
BATTLE_WAIT = int(os.getenv('BATTLE_WAIT')) or 50

FONT_NAME = os.getenv('FONT_NAME') or 'm5x7.ttf'
FONT = os.path.join(DIRNAME, 'assets/fonts', FONT_NAME)
FONT_SIZE = (int(os.getenv('FONT_SIZE')) or 32) * SCALE
MIN_FONT_SIZE = int(os.getenv('MIN_FONT_SIZE')) or 8

BAR_W = (int(os.getenv('BAR_W')) or 64) * SCALE
BAR_H = (int(os.getenv('BAR_H')) or 4) * SCALE

MENU_CURSOR = os.getenv('MENU_CURSOR') or '>'
TARGET_CURSOR = os.getenv('TARGET_CURSOR') or '<'
CURSOR_SIZE = (int(os.getenv('CURSOR_SIZE')) or 32) * SCALE

BATTLE_BG = os.getenv('BATTLE_BG') or 'battlebg1.png'
TEST_IMG = os.getenv('TEST_IMG') or 'test_img.png'
BATTLE_BG_PATH = os.path.join(DIRNAME, 'assets/gfx/backgrounds', BATTLE_BG)
TEST_IMG_PATH = os.path.join(DIRNAME, 'assets/gfx', TEST_IMG)
