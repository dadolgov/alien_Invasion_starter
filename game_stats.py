"""Game statistics class. Counts remaining player lives.
Author: Dmitrii Dolgov
Date: 4/18/2026
    """
#from pathlib import Path
import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class GameStats():
    """tracks and displays score, level and lives
    """
    def __init__(self, game: 'AlienInvasion'):
        """sets initial score, lives and level

        Args:
            game (AlienInvasion): reference to the game
        """
        self.game=game
        self.settings=game.settings
        self.max_score=0
        self.init_saved_scores()
        self.reset_stats()

    def init_saved_scores(self):
        """Loads the hi-score from the scores file, create it if file is empty.
        """
        self.path=self.settings.scores_file
        if self.path.exists() and self.path.stat.__sizeof__() > 20:
            contents=self.path.read_text()
            scores=json.loads(contents)
            self.hi_score=scores.get('hi_score', 0)
        else:
            self.hi_score=0
            self.save_scores()
    
    def save_scores(self):
        """save scores to the file
        """
        scores={
            'hi_score':self.hi_score
        }
        contents=json.dumps(scores, indent=4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f'File not found: {e}')

    def reset_stats(self):
        """Reset the score, level and life count
        """
        self.ships_left=self.settings.starting_ship_count
        self.score=0
        self.level=1
        
    def update(self, collisions):
        """update scores during the collision check

        Args:
            collisions (dict): dictionary of sprites that triggered a collision
        """
        self._update_score(collisions)
        self._update_max_score()
        self._update_hi_score()

    def _update_max_score(self):
        """update the current session max score
        """
        if self.score>self.max_score:
            self.max_score=self.score
    
    def _update_hi_score(self):
        """update the total hi score
        """
        if self.score>self.hi_score:
            self.hi_score=self.score

    def _update_score(self, collisions):
        """update current score

        Args:
            collisions (dict): dictionary of collisions
        """
        for alien in collisions.values():
            self.score+=self.settings.alien_points

    def update_level(self):
        """increment level
        """
        self.level+=1


