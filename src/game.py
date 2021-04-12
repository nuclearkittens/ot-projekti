import pygame
from renderer import Renderer
from titlescreen import TitleScreen
from helpmenu import HelpMenu
from creditsmenu import CreditsMenu


class Game:
    def __init__(self):
        self.running = True
        self.battle = False
        
        self.SCREEN_W = 512
        self.SCREEN_H = 448
        self.FONT_NAME = 'assets/m5x7.ttf'
        self.DARK_PURPLE = (66, 30, 66)
        self.POWDER_ROSE = (201, 143, 143)
        self.DARK_ROSE = (189, 113, 130)

        self.UP_K, self.DOWN_K, self.RIGHT_K, self.LEFT_K = False, False, False, False
        self.SELECT_K, self.START_K, self.BACK_K, self.PAUSE_K = False, False, False, False

        self.display = pygame.Surface((self.SCREEN_W,self.SCREEN_H))
        self.window = pygame.display.set_mode(((self.SCREEN_W,self.SCREEN_H)))

        self._renderer = Renderer(self)

        self.titlescreen = TitleScreen(self)
        self.help = HelpMenu(self)
        self.credits = CreditsMenu(self)
        self.current = self.titlescreen

    def game_loop(self):
        while self.battle:
            self.check_events()
            if self.START_K:
                self.battle = False
            self.display.fill(self.DARK_PURPLE)
            self._renderer.draw_text('battle', 32, self.SCREEN_W//2, self.SCREEN_H//2)
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.battle = False, False
                self.current.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_K = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_K = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_K = True
                if event.key == pygame.K_UP:
                    self.UP_K = True

    def reset_keys(self):
        self.UP_K, self.DOWN_K, self.RIGHT_K, self.LEFT_K = False, False, False, False
        self.SELECT_K, self.START_K, self.BACK_K, self.PAUSE_K = False, False, False, False



