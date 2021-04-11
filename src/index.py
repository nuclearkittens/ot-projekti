import pygame as pg
from clock import Clock
from game import Game
from renderer import Renderer

DISPLAY_W = 512
DISPLAY_H = 448

FONT_NAME = '/assets/m5x7.ttf'
DARK_PURPLE = (66, 30, 66)
POWDER_ROSE = (201, 143, 143)
DARK_ROSE = (189, 113, 130)

def main():
    screen = pg.Surface((DISPLAY_W, DISPLAY_H))
    display = pg.display.set_mode((DISPLAY_W, DISPLAY_H))

    pg.set_caption("untitled rpg: battle demo")

    clock = Clock()
    renderer = Renderer(display)
    game = Game()

    pygame.init()
    game.start()

if __name__ == 'main':
    pass