import pygame.font
from heart import Heart
from pygame.sprite import Group

class Scoreboard:
    """
    Player's game scores info
    """

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.game_stats = ai_game.game_stats

        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 37)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_lives()

    def prep_score(self):
        rounded_score = round(self.game_stats.score, -1)
        self.score_image = self.font.render("{:,}".format(rounded_score), True, 
            self.text_color, self.settings.background_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 14

    def prep_high_score(self):
        rounded_score = round(self.game_stats.high_score, -1)
        self.high_score_image = self.font.render("{:,}".format(rounded_score), True, 
            self.text_color, self.settings.background_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top + 14

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        self.lives.draw(self.screen)

    def check_high_score(self):
        if self.game_stats.high_score < self.game_stats.score:
            self.game_stats.high_score = self.game_stats.score
            self.prep_high_score()

    def prep_level(self):
        self.level_image = self.font.render(str(self.game_stats.level), True,
            self.text_color, self.settings.background_color)

        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.screen_rect.right - 20
        self.level_image_rect.top = self.score_rect.bottom + 20

    def prep_lives(self):
        self.lives = Group()
        for ship_number in range(self.game_stats.ship_left):
            heart = Heart(self.ai_game)
            heart.rect.x = 20 + ship_number * (heart.rect.width + 14)
            heart.rect.top = self.screen_rect.top + 14
            self.lives.add(heart)