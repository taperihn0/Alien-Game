import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from stars import Star
import random

from game_stats import GameStats
from time import sleep
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """
    Overall class to manage game assets 
    and behavior of game process
    """

    def __init__(self):
        """
        Initialize the game, and create 
        game resources
        """
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        self.game_stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self._create_fleet()
        self._create_stars()

        self.play_button = Button(self, "Play")

    def run_game(self):
        """ Main game loop """
        self.running = True
        while self.running:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """ Mouse and keyboard events control """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._checkup_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._checkup_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_play_button(pygame.mouse.get_pos())

    def _checkup_keydown_events(self, event):
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            self.running = False
        elif event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_p:
            self._check_play_button(None)

    def _checkup_keyup_events(self, event):
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False

    def _update_screen(self):
        """ Updating screen """
        if self.game_stats.game_active:
            self.ship.update()
        
        self._update_bullets()
        self._update_aliens()
        self._update_stars()
        self.screen.fill(self.settings.background_color)

        if self.game_stats.game_active:
            self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        for star in self.stars:
            star.draw_star()

        self.aliens.draw(self.screen)

        self.scoreboard.show_score()

        if not self.game_stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed and self.game_stats.game_active:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            
        if self.game_stats.game_active:
            self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        for alien in collisions.values():
            self.game_stats.score += self.settings.alien_points * len(alien)
        self.scoreboard.prep_score()
        self.scoreboard.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.ship.center_ship()

            self.game_stats.level += 1
            self.scoreboard.prep_level()

    def _create_fleet(self):
        new_alien = Alien(self)
        alien_width, alien_height  = new_alien.rect.size
        aliens_number_x = (self.settings.screen_width - 2 * alien_width) // (2 * alien_width)
        aliens_number_y = (self.settings.screen_height - 
            3 * alien_width - self.ship.rect.height) // (2 * alien_width)

        for row_number in range(aliens_number_y):
            for alien_number in range(aliens_number_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number: int, row_number: int):
        new_alien = Alien(self)
        alien_width, alien_height  = new_alien.rect.size
        new_alien.x = alien_width + 2 * alien_width * alien_number
        new_alien.y = alien_height + 2 * alien_height * row_number
        new_alien.rect.x = new_alien.x
        new_alien.rect.y = new_alien.y
        self.aliens.add(new_alien)

    def _create_stars(self):
        for star_distance in range(3):
            for i in range(10):
                self.stars.add(Star(self, star_distance, self.settings.background_speed 
                    + random.random() / 3 * star_distance))

    def _update_stars(self):
        self.stars.update()

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens) \
        or self._check_aliens_bottom():
            self._ship_hit()

    def _ship_hit(self):
        if self.game_stats.ship_left >= 1:
            self.game_stats.ship_left -= 1
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            self.scoreboard.prep_lives()
            sleep(0.2)
        
        if not self.game_stats.ship_left:
            self.game_stats.game_active = False
            self.settings.fleet_drop_speed = 0
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self) -> bool:
        for alien in self.aliens:
            if alien.rect.bottom >= self.screen.get_height():
                return True
        return False

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_play_button(self, mouse_pos):
        if (mouse_pos is None or self.play_button.rect.collidepoint(mouse_pos)) \
        and not self.game_stats.game_active:
            self.game_stats.game_active = True
            self.settings.fleet_drop_speed = self.settings.fleet_drop_speed_on
            self.settings.initialize_dynamic_settings()

            self.game_stats.reset_stats()
            self.aliens.empty()
            self.bullets.empty()
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_lives()

            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)

    def __del__(self):
        pygame.quit()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()