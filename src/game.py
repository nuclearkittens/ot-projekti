import pygame
from renderer import Renderer
from titlescreen import TitleScreen
from helpmenu import HelpMenu
from creditsmenu import CreditsMenu


class Game:
    def __init__(self):
        self.running = True
        self.battle = False

        self.UP_K, self.DOWN_K, self.RIGHT_K, self.LEFT_K = False, False, False, False
        self.SELECT_K, self.START_K, self.BACK_K, self.PAUSE_K = False, False, False, False

        self._renderer = Renderer()
        self._screen_w = self._renderer.SCREEN_W
        self._screen_h = self._renderer.SCREEN_H

        self._titlescreen = TitleScreen(self)
        self._help = HelpMenu(self)
        self._credits = CreditsMenu(self)
        self.current = self._titlescreen

    def game_loop(self):
        while self.battle:
            self.check_events()
            if self.START_K:
                self.battle = False
            self._renderer.fill()
            self._renderer.draw_text('battle', 32, self._screen_w//2, self._screen_h//2)
            self._renderer.blit_screen()
            self._renderer.update()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.battle = False, False
                self.current.run_menu = False
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



