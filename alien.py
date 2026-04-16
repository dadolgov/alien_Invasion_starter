"""methods and settings related to alien ship
Author: Dmitrii Dolgov
Date: 4/9/2026
    """
import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Alien(Sprite):
    """Holds settings and methods for a standard bullet

    Args:
        Sprite : image of a bullet, .png
    """
    def __init__(self, fleet:"AlienFleet", x:float, y:float)->None:
        """references the screen and game settings, links the sprites,
        sets up the size of the sprite used

        Args:
            game (AlienInvasion): active game instance
            x (float): horizontal coordinate
            y(float): vertical coordinate
        """
        super().__init__()

        self.fleet=fleet
        self.screen=fleet.game.screen
        self.boundaries=fleet.game.screen.get_rect()
        self.settings=fleet.game.settings

        self.image=pygame.image.load(self.settings.alien_file)
        self.image=pygame.transform.scale(self.image,(self.settings.alien_w, self.settings.alien_h))

        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self)->None:
        """updates the position of an alien
        """
        temp_speed=self.settings.fleet_speed

        self.x+=temp_speed * self.fleet.fleet_direction
        self.rect.x=self.x
        self.rect.y=self.y
    
    def check_edges(self):
        return(self.rect.right>=self.boundaries.right or self.rect.left<=self.boundaries.left)
    
    def draw_alien(self)->None:
        """draws the bullet on a screen
        """
        self.screen.blit(self.image, self.rect)