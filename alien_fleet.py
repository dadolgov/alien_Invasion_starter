"""Contains the methods necessary to calculate the size, offsets and movements of the fleet
Author: Dmitrii Dolgov
Date 4/18/2026
    """

import pygame
from alien import Alien

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    

class AlienFleet:
    
    def __init__(self, game: "AlienInvasion"):
        self.game = game
        self.settings = game.settings
        self.fleet=pygame.sprite.Group()
        self.fleet_direction=self.settings.fleet_direction
        self.fleet_drop_speed=self.settings.fleet_drop_speed

        self.create_fleet()
    
    def create_fleet(self):
        """Calculates the size and positioning of alien fleet and puts it on the screen
        """
        alien_w=self.settings.alien_w
        alien_h=self.settings.alien_h
        screen_w=self.settings.screen_w
        screen_h=self.settings.screen_h

        fleet_w, fleet_h = self.calculate_fleet_size(alien_w, screen_w, alien_h, screen_h)  

        x_offset, y_offset = self.calculate_offsets(alien_w, alien_h, screen_w, fleet_w, fleet_h)
        self._create_rectangle_fleet(alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)

    def _create_rectangle_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):
        """creates rows and collumns of aliens in the rectangle area designated for the fleet

        Args:
            alien_w (int): width of the alien sprite
            alien_h (int): height of the alien sprite
            fleet_w (int): width of the fleet area
            fleet_h (int): height of the fleet area
            x_offset (int): horizontal offset of the fleet position
            y_offset (int): vertical offset of the fleet position
        """
        for row in range(fleet_h):
            for col in range(fleet_w):
                current_x=alien_w*col+x_offset
                current_y=alien_h*row+y_offset
                if col%2==0 or row%2==0:
                    continue
                self._create_alien(current_x, current_y)

    def calculate_offsets(self, alien_w, alien_h, screen_w, fleet_w, fleet_h):
        """Calculates the fleet offsets depending on fleet and screen sizes

        Args:
            alien_w (int): width of the alien sprite
            alien_h (int): height of the alien sprite
            screen_w (int): width of the screen
            fleet_w (int): width of the fleet area
            fleet_h (int): height of the fleet area

        Returns:
            int: tuple of horizontal and vertical offsets
        """
        half_screen=self.settings.screen_h//2

        fleet_horizontal_space=fleet_w*alien_w
        fleet_vertical_space=fleet_h*alien_h
        x_offset=int((screen_w-fleet_horizontal_space)//2)
        y_offset=int((half_screen-fleet_vertical_space)//2)
        return x_offset,y_offset


    def calculate_fleet_size(self, alien_w:int, screen_w:int, alien_h:int, screen_h:int):
        """calculates how many ships needed for the fleet to fill the half of
        the screen opposite from player

        Args:
            alien_w (int): width of alien sprite
            screen_w (int): width of the screen
            alien_h (int): height of the sprite
            screen_h (int): height of the screen

        Returns:
            int: tuple of fleet width and height
        """
        fleet_w=(screen_w//alien_w)
        fleet_h=(screen_h/2)//alien_h

        if fleet_w % 2==0:
            fleet_w-=1
        else:
            fleet_w-=2
        if fleet_h % 2 == 0:
            fleet_h-=1
        else:
            fleet_h-=2

        return int(fleet_w), int(fleet_h)
        
    def _create_alien(self, current_x:int, current_y:int):
        """Creates a single alien sprite

        Args:
            current_x (int): horizontal coordinate
            current_y (int): vertical coordinate
        """
        new_alien=Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        """When the fleet reaches the edge of the screen, it changes the movement direction
        and shifts closer to the player
        """
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction*=-1
                break
    
    def _drop_alien_fleet(self):
        """Moves the fleet closer to the player's ship
        """
        for alien in self.fleet:
            alien.y+=self.fleet_drop_speed

    def update_fleet(self):
        """Defines the alien fleet movement
        """
        self._check_fleet_edges()
        self.fleet.update()


    def draw(self):
        """Draws an alien sprite as a part of the fleet
        """
        alien: "Alien"
        for alien in self.fleet:
            alien.draw_alien()
    
    def check_collisions(self, other_group):
        """checks collision between alien fleet and other sprites

        Args:
            other_group (pygame.sprite.Group): group of alien sprites

        Returns:
            dict: A dictionary mapping each killed alien and the bullet it was hit with
        """
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)
    
    def check_fleet_bottom(self): #in project this should be left edge
        """checks if the fleet made it to the player's edge of a screen

        Returns:
            bool: True if the alien reached the player's edge of screen, causing player to lose a life,
            otherwise False
        """
        alien:Alien
        for alien in self.fleet:
            if alien.rect.bottom>=self.settings.screen_h:
                return True
        return False
    
    def check_destroyed_status(self):
        """checks if all the alien ships were destroyed

        Returns:
            bool: fleet status. True if fleet is empty(destroyed)
        """
        if not self.fleet:
            return not self.fleet