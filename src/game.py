import pygame

class Game:
    def __init__(self, clock):
        self.running = True
        self.playing = False

        self._clock = clock
        self.DISPLAY_W = 512
        self.DISPLAY_H = 448

        self.FONT_NAME = '/assets/m5x7.ttf'
        self.DARK_PURPLE = (66, 30, 66)
        self.POWDER_ROSE = (201, 143, 143)
        self.DARK_ROSE = (189, 113, 130)

        self.screen = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.display = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))

        pygame.display.set_caption("untitled rpg: battle demo")

        self.UP, self.DOWN, self.RIGHT, self.LEFT = False, False, False, False
        self.SELECT, self.START, self.BACK, self.PAUSE = False, False, False, False

    def start(self):
        self.playing = True

    def game_loop(self):
        while self.playing:
            self.check_events()
            self.screen.fill(self.DARK_PURPLE)
            self.display.blit(self.screen, (0,0))
            pygame.display.udate()
            self.reset_keys()
            # self._clock.tick(60)
            
            
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.UP = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.DOWN = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.RIGHT = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.LEFT = True
                if event.key == pygame.K_RETURN:
                    self.SELECT = True
                if event.key == pygame.K_p:
                    self.PAUSE = True

    def reset_keys(self):
        self.UP, self.DOWN, self.RIGHT, self.LEFT = False, False, False, False
        self.SELECT, self.START, self.BACK, self.PAUSE = False, False, False, False



        