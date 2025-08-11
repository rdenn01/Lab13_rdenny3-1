"""
Alien Class
Ryan Denny

This class represents an alien, handling its position, movement, and edge detection.

7/27/2025
"""

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """
    Handles drawing aliens, updating their position, and checking for edges.
    """
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load('Lab13_rdenny3-1\Assets\images\enemy_4.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    """
    Updates the position of the alien.
    """
    def update(self):
        self.y += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.y = self.y

    """
    Checks to see if the alien has hit the bottom or top edge of the screen.
    """
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.bottom >= screen_rect.bottom) or (self.rect.top <= 0)