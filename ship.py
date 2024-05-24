import pygame

class Ship:
    """ Class of spaceship """

    def __init__(self, ai_game):
        """
        Initialization of spaceship 
        initial position
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images\\001-spaceship.png')
        self.rect = self.image.get_rect()
        
        self.center_ship()
        self.moving_right, self.moving_left = False, False
        self.moving_up, self.moving_down = False, False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x_pos += self.settings.ship_speed_x
        if self.moving_left and self.rect.left > 0:
            self.x_pos -= self.settings.ship_speed_x

        if self.moving_up and self.rect.top > 0:
            self.y_pos -= self.settings.ship_speed_y
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y_pos += self.settings.ship_speed_y

        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

    def blitme(self):
        """
        Displaying shipwreck at 
        current position
        """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x_pos, self.y_pos = float(self.rect.x), float(self.rect.y)