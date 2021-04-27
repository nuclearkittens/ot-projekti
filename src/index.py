import pygame as pg

from ui.renderer import Renderer
from ui.eventhandler import EventHandler
from config import SCREEN_W, SCREEN_H
from clock import Clock
from keys import Keys
from battledemo import Demo

def main():
    pg.init()

    screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
    pg.display.set_caption('battle demo v2')

    clock = Clock()
    renderer = Renderer(screen)
    keys = Keys()
    eventhandler = EventHandler(keys)

    demo = Demo(clock, renderer, keys, eventhandler)
    demo.game_loop()

if __name__ == '__main__':
    main()