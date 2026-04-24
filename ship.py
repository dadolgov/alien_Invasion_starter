"""ship controls and visuals
Author: Dmitrii Dolgov
Date: 4/9/2026
    """
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship:
    """Handles movement, weapon management, boundary checking and ship sprite rendering
    """
    def __init__(self, game:"AlienInvasion", arsenal:"Arsenal")->None:
        """references game settings and screen parameters,
        creates a ship at the starting position,
        loads and processes the ship sprite file,
        links to the Arsenal class

        Args:
            game (AlienInvasion): active game instance
            arsenal (Arsenal): the arsenal class for weapon handling
        """
        self.game=game
        self.settings=game.settings
        self.screen=game.screen
        self.boundaries=self.screen.get_rect()

        self.image=pygame.image.load(self.settings.ship_file)
        self.image=pygame.transform.scale(self.image, (self.settings.ship_w, self.settings.ship_h))

        self.rect=self.image.get_rect()
        self._center_ship()
        self.moving_right=False
        self.moving_left=False
        

        self.arsenal=arsenal

    def _center_ship(self):
        """resets the ship positioning
        """
        self.rect.midbottom=self.boundaries.midbottom
        self.x=float(self.rect.x)
    
    def update(self):
        """updating the position of the ship and weapon status"""
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        """moves the ship left or right within the screen boundaries
        """
        temp_speed=self.settings.ship_speed
        if self.moving_right and self.rect.right<self.boundaries.right:
            self.x+=temp_speed
        if self.moving_left and self.rect.left>self.boundaries.left:
            self.x-=temp_speed
        
        self.rect.x=self.x

    def draw(self)->None:
        """draws the ship and bullets on the screen
        """
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)
    
    def fire(self)->bool:
        """attempts to create a bullet on the screen.

        Returns:
            bool: True if the bullet was created. False if bullet wasn't created due to 
            bullet amount limits
        """
        return self.arsenal.fire_bullet()

    def check_collisions(self, other_group):
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        return False