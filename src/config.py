import os.path

# rename to constants

DIRNAME = os.path.dirname(__file__)

DB_PATH = os.path.join(DIRNAME, 'assets/db/gamedata.db')
DB_INIT_CMDS = os.path.join(DIRNAME, 'assets/db/init_commands.sql')

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
