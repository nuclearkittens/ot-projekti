import pygame
from game import Game

def main():
    pygame.init()

    game = Game()

    while game.running:
        game.current.display_menu()
        game.game_loop()


if __name__ == "__main__":
    main()