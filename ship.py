import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """
    A class to manage the player ship, including movement, rendering, and recentering its position.
    """
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        self.image = pygame.image.load('Lab13_rdenny3-1\Assets\images\ship.png')
        self.rect = self.image.get_rect()

        self.rect.midright = self.screen_rect.midright

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_up = False
        self.moving_down = False

    def update(self):
        """
        Updates the ship's position based on current movement directions.
        """
        if self.moving_up and self.rect.top > 0:
             self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.game.settings.screen_height - 15:
             self.y += self.settings.ship_speed

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def blitme(self):
        """
        Renders the ship at its current position.
        """
        rotated_image = pygame.transform.rotate(self.image, 90)
        self.screen.blit(rotated_image, self.rect)

    def center_ship(self):
        """
        Recenters the ship on the right side of the screen.
        """
        self.rect.midright = self.screen_rect.midright
        self.y = float(self.rect.y)