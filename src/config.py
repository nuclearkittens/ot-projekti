import os.path

DIRNAME = os.path.dirname(__file__)

ITEMS_DB = os.path.join(DIRNAME, 'assets/db/items.json')
ATKS_DB = os.path.join(DIRNAME, 'assets/db/offensive_skills.json')
BLK_MAG_DB = os.path.join(DIRNAME, 'assets/db/black_magic.json')
ENEM_DB = os.path.join(DIRNAME, 'assets/db/monsters.json')
PARTY_DB = os.path.join(DIRNAME, 'assets/db/party.json')

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

FONT = os.path.join(DIRNAME, 'assets/fonts/m5x7.ttf')
FONT_SIZE = 32 * SCALE
MIN_FONT_SIZE = 4

BAR_W = 64 * SCALE
BAR_H = 4 * SCALE

CURSOR = '>'
CURSOR_SIZE = 32 * SCALE