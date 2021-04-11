import pygame
from clock import Clock
from game import Game
from renderer import Renderer

def main():
    pygame.init()

    clock = Clock()
    # renderer = Renderer(display)
    game = Game(clock)

    game.start()
    while game.running:
        game.game_loop()

if __name__ == 'main':
    main()