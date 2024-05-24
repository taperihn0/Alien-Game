import pygame
from pygame.sprite import Sprite
from random import randint

class Star(Sprite):
    """
    Background stars class
    """
    
    def __init__(self, ai_game, radius: int, speed: float):
        super().__init__()
        self.screen = ai_game.screen
        self.radius = radius
        self.speed = float(speed)
        self.star_pos = pygame.Vector2(randint(0, self.screen.get_width()), randint(0, self.screen.get_height()))
        self.y = float(self.star_pos.y)

    def update(self):
        self.y += self.speed
        self.star_pos.y = self.y
        if self.star_pos.y > self.screen.get_height():
            self.star_pos.y, self.y = 0, 0.0
            self.star_pos.x = randint(0, self.screen.get_width())

    def draw_star(self):
        pygame.draw.circle(self.screen, 'white', self.star_pos, self.radius)