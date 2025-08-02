"""
Settings
Ryan Denny

This stores settings such as screen settings and bullets.

7/27/2025
"""

class Settings:
    """
    This class handles creating and storing all settings for the game, ranging
    from: screen properties, bullet properties, alien properties, ship properties,
    and scalors for speed and score.
    """

    def __init__(self):
        # Screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Bullets
        self.bullet_speed = 15.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Aliens
        self.alien_speed = 3.0
        self.drop_speed = 10
        self.fleet_direction = 1
    
        # Ship
        self.ship_limit = 3
        self.ship_speed = 3

        # Scales
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """
        This function handles initializing and resetting dynamic settings
        that change during gameplay.
        """
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0
        self.alien_points = 50

        self.fleet_direction

    def increase_speed(self):
        """
        This class handles increasing values according to given scalors.
        """
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)