import pygame
from constants import *
from maingame import MainGame
from eventcheck import EventCheck
from battle import Battle
from gamestate import GameState
from titlescreen import TitleScreen
from helpmenu import HelpMenu
from creditsmenu import CreditsMenu
from renderer import Renderer
from keys import Keys

def main():
    pygame.init()

    display = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('untitled rpg: battle demo')

    gamestate = GameState()
    renderer = Renderer(display)
    keys = Keys()
    eventcheck = EventCheck(gamestate, keys)
    battle = Battle(gamestate, renderer, keys, eventcheck)
    titlescreen = TitleScreen(renderer, keys, gamestate, eventcheck)
    menu1 = HelpMenu(renderer, keys, gamestate, eventcheck)
    menu2 = CreditsMenu(renderer, keys, gamestate, eventcheck)

    game = MainGame(gamestate, renderer, keys, eventcheck, battle, titlescreen, menu1, menu2)
    game.new_game()


if __name__ == "__main__":
    main()