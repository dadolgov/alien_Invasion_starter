"""Alien Invasion. A 2D spcae shootemup game.
Author: Dmitrii Dolgov / Gabriel Walters
Date: 4/9/2026
Starter code by Gabriel Walters https://github.com/RedBeard41/alien_Invasion_starter
    """


import sys
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from arsenal import Arsenal
#from alien import Alien
from alien_fleet import AlienFleet
from button import Button

from time import sleep

class AlienInvasion:
    """Main game class. Contains methods for core systems: events, sound and picture
    """
    def __init__(self)->None:
        """initializes the game, settings, screen and sound, controls and events
        """
        pygame.init()
        self.settings=Settings()
        self.game_stats=GameStats(self.settings.starting_ship_count)

        self.screen=pygame.display.set_mode((self.settings.screen_w, self.settings.screen_h))
        pygame.display.set_caption(self.settings.name)

        self.bg=pygame.image.load(self.settings.bg_file)
        self.bg=pygame.transform.scale(self.bg, (self.settings.screen_w, self.settings.screen_h))        

        self.running=True
        self.clock=pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound=pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)

        self.impact_sound=pygame.mixer.Sound(self.settings.impact)
        self.impact_sound.set_volume(0.7)

        self.ship=Ship(self, Arsenal(self))
        self.alien_fleet=AlienFleet(self)
        self.alien_fleet.create_fleet()

        self.play_button=Button(self,"Play")
        self.game_active=False
    
    def _check_collisions(self):
        """Checks collisions between player and aliens, bullets and aliens, 
        aliens and screen bottom
        """
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_status()
        
        if self.alien_fleet.check_fleet_bottom():
            self._check_game_status()
        
        collisions=self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(500)
        
        if self.alien_fleet.check_destroyed_status():
            self._reset_level()

    def _check_game_status(self):
        """resets the level or ends the game depending on remaining lives
        """
        if self.game_stats.ships_left>0:
            self.game_stats.ships_left-=1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active=False

        print(self.game_stats.ships_left)

    def _reset_level(self):
        """Erases the bullets and the fleet, generates a new one
        """
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()

    def restart_game(self)->None:
        #set up dynamic settings
        #reset Game stats
        #update hud scores
        self._reset_level()
        self.ship._center_ship()
        self.game_active=True
        pygame.mouse.set_visible(False)
    

    def run_game(self)->None:
        """Main game loop. Checks for events and updates the screen
        """
        #game loop
        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()

            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _update_screen(self)->None:
        """updates background and ship sprite
        """
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        self.alien_fleet.draw()

        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)

        pygame.display.flip()

    def _check_events(self)->None:
        """gets and processes game events: keypresses and window closing
        """
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running=False
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_event(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self):
        mouse_pos=pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()

    def _check_keydown_event(self, event):
        """processes the key press events. Arrows move the ship, Q closes the game,
        SPACE fires the lasers

        Args:
            event (pygame): KEYDOWN event
        """
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key==pygame.K_SPACE:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(250)

        elif event.key==pygame.K_q:
            self.running=False
            pygame.quit()
            sys.exit()
            

    def _check_keyup_event(self, event):
        """Processes the release of buttons. Releasing move buttons stops the movement of the ship

        Args:
            event (pygame): KEYUP event
        """
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False


if __name__ == '__main__':
    ai=AlienInvasion()
    ai.run_game()
