import pygame
from pygame.sprite import Sprite

class Heart(Sprite):
    """
    Hearts - lives of player
    """

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load('images\\001-heart.png').convert_alpha()
        self.rect = self.image.get_rect()