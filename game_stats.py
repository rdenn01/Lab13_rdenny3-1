"""
Settings
Ryan Denny

This represents stat handling and resetting stats.

7/27/2025
"""

class GameStats:
    """
    Handles how many ships are left, the score, high score, and level.
    """
    def __init__(self, game):
        self.settings = game.settings
        self.reset_stats()

        self.high_score = 0

    def reset_stats(self):
        """
        Resets stats to baseline.
        """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1