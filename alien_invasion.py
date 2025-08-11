"""
Alien Invasion Game
Ryan Denny

This program includes game logic for a game where you control a spaceship, 
moving it up and down and pressing space to shoot.

7/27/2025
"""

import sys
import pygame
from pygame.sprite import Sprite
import time

from settings import Settings
from bullet import Bullet
from game_stats import GameStats
from scoreboard import Scoreboard
from alien import Alien
from button import Button
from ship import Ship
        

class AlienInvasion:
    """
    The main handler for all game logic, including the game loop, handling events,
    updating the screen, managing game states, and various other game objects.
    """
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.create_fleet()
        self.game_active = False

        self.play_button = Button(self, "Play")

    def game_loop(self):
        """
        The primary game loop that handles updating objects and ticks.
        """
        while True:
            self.check_events()

            if self.game_active:
                self.ship.update()
                self.update_bullets()
                self.update_aliens()
            self.update_screen()
            self.clock.tick(60)
    
    def update_screen(self):
            """
            Updates all graphical elements on the screen.
            """
            self.screen.fill(self.settings.bg_color)

            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

            self.ship.blitme()
            self.aliens.draw(self.screen)

            self.scoreboard.show_score()

            if not self.game_active:
                self.play_button.draw_button()

            pygame.display.flip()

    def update_bullets(self):
        """
        Assists in checking bullet collisions, removing bullets that go off-screen,
        and ensuring bullets are updated.
        """
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.left < 0:
                print("removing bullet")
                self.bullets.remove(bullet)

        self.check_bullet_alien_collisions()

    def check_bullet_alien_collisions(self):
        """
        Checks to see if bullets have hit aliens, removing hit aliens and bullets,
        updating the score, and creating new fleets if all aliens are killed.
        """
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()
            self.settings.increase_speed

            self.stats.level += 1
            self.scoreboard.prep_level()

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

    def update_aliens(self):
        """
        Updates the movement direction of aliens, checking if aliens hit the player,
        and if the aliens have reached the end of the screen.
        """
        self.check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()

        self.check_alien_bottom()

    def check_events(self):
        """
        Handles all player input events.
        """
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                     self.check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.check_play_button(mouse_pos)
                    

    def check_keydown_events(self, event):
        """
        Handles all input when a key is pressed down.
        """
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
             sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()

    def check_keyup_events(self, event):
        """
        Handles all input when a key is released.
        """
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def check_play_button(self, mouse_pos):
        """
        Starts or restarts the game when the play button is clicked.
        """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.game_active = True
            self.stats.reset_stats()
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()

            self.bullets.empty()
            self.aliens.empty()

            self.create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def check_fleet_edges(self):
        """
        Checks if any alien has reached the top or bottom of the screen.
        """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def check_alien_bottom(self):
        """
        Checks to see if any alienh as reached the edge of the screen.
        """
        for alien in self.aliens.sprites():
            if alien.rect.right >= self.settings.screen_width:
                self.ship_hit()
                break

    def change_fleet_direction(self):
        """
        Changes the bobbing direction of aliens when they hit the edge of the screen.
        """
        for alien in self.aliens.sprites():
            alien.rect.x += self.settings.drop_speed
        self.settings.fleet_direction *= -1

    def fire_bullet(self):
        """
        Handles bullet quantity limits and creates bullets.
        """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def ship_hit(self):
        """
        Handles the event of the ship being hit by an alien. It decreases the
        number of lives and resets the current game state.
        """
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            self.bullets.empty()
            self.aliens.empty()

            self.create_fleet()
            self.ship.center_ship()

            time.sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
    
    def create_fleet(self):
        """
        Handles creating fleets in available screen space.
        """
        alien = Alien(self)
        self.aliens.add(alien)

        alien_width, alien_height = alien.rect.width, alien.rect.height
        current_x, current_y = alien_width, alien_height

        col_limit = 8
        curr_col = 0

        while current_x < (self.settings.screen_width - 3 * alien_width) and curr_col < col_limit:
            while current_y < (self.settings.screen_height - 2 * alien_height):
                self.create_alien(current_x, current_y)
                current_y += 2 * alien_height
            current_y = alien_height
            current_x += 2 * alien_width
            curr_col += 1
    
    def create_alien(self, x_position, y_position):
        """
        Creates a new alien at the given position
        """
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.y = y_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


if __name__ == '__main__':
    game = AlienInvasion()
    game.game_loop()