import pygame
from keys import Keys
from constants import *

class Battle:
    def __init__(self, gamestate, renderer, keys, eventcheck):
        self._gamestate = gamestate
        self._renderer = renderer
        self._keys = keys
        self._eventcheck = eventcheck

    def game_loop(self):
        while self._gamestate.battle:
            if self.check_events() == False:
                pygame.quit()
            if self._keys.START_K:
                self._gamestate.battle = False
                self._gamestate.title = True
            self._renderer.fill()
            self._renderer.draw_text('battle', 32, SCREEN_W//2, SCREEN_H//2)
            self._renderer.blit_screen()
            self._renderer.update()
            self._keys.reset_keys()

    def check_events(self):
        self._eventcheck.check()


    # def check_events(self):
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             self._gamestate.set_all_false()
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_RETURN:
    #                 self._keys.START_K = True
    #             if event.key == pygame.K_BACKSPACE:
    #                 self._keys.BACK_K = True
    #             if event.key == pygame.K_DOWN:
    #                 self._keys.DOWN_K = True
    #             if event.key == pygame.K_UP:
    #                 self._keys.UP_K = True




