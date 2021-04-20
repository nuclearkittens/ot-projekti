import pygame
import random

from src.keys import Keys
from src.eventcheck import EventCheck
from src.gamestate import GameState
from src.renderer import Renderer
from src.constants import *
from src.load_util import load_img

class BattleDemo:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((SCREEN_W, SCREEN_H))

        self.gamestate = GameState()
        self.keys = Keys()
        self.renderer = Renderer(display)
        self.eventcheck = EventCheck(gamestate, keys)

        self.bg = load_img('battlebg1', 'background')
        self.bg_rect = self.bg.get_rect()

    def draw_bg(self):
        self.renderer.draw_img(self.bg, self.bg_rect)

