class Settings:
    """
    Storage of all the 
    game settings
    """

    def __init__(self):
        """
        Initialization of static
        game settings
        """
        self.screen_width = 1200
        self.screen_height = 800
        self.background_color = 'black'

        self.bullet_width = 2 #15
        self.bullet_height = 10
        self.bullet_color = 'orange'
        self.bullets_allowed = 3

        self.fleet_drop_speed = 0
        self.fleet_drop_speed_on = 25

        self.ship_limit = 3

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_x = 0.68 #0.85
        self.ship_speed_y = self.screen_height / self.screen_width * self.ship_speed_x
        self.background_speed = 0.07

        self.alien_speed = 0.13
        self.fleet_direction = 1

        self.bullet_speed = 0.5

        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_x *= self.speedup_scale - 0.05
        self.ship_speed_y *= self.speedup_scale - 0.05
        self.background_speed *= self.speedup_scale

        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale - 0.05

        self.alien_points = int(self.alien_points * self.score_scale)
