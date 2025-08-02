"""
Bullet Class
Ryan Denny

This handles logic for creating bullets, moving bullets, and drawing bullets.

7/27/2025
"""

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """
    Updates the ship's position based on current movement directions.
    """
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect(0, 0, self.settings.bullet_height, self.settings.bullet_width)
        self.rect.midbottom = game.ship.rect.midbottom
        self.rect.y -= 7 # So this guy stays centered

        self.x = float(self.rect.x)

    def update(self):
        """
        Handles the bullet's movement.
        """
        self.x -= self.settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self):
        """
        Renders the bullet.
        """
        pygame.draw.rect(self.screen, self.color, self.rect)