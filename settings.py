"""game settings, asset links and gameplay constants
Author: Dmitrii Dolgov
Date: 4/9/2026
    """
from pathlib import Path
class Settings:
    """sets up the screen size and name, path to image and sound files, constant gameplay parameters.
    """
    def __init__(self):
        self.name: str="Alien Invasion"
        self.screen_w:int=1200
        self.screen_h:int=800
        self.fps:int=60
        self.bg_file=Path.cwd()/"Assets"/"images"/"Starbasesnow.png"
        self.difficulty_scale=1.1
        self.scores_file=Path.cwd()/"Assets"/"file"/"scores.json"

        self.ship_file=Path.cwd()/"Assets"/"images"/"ship2(no bg).png"
        self.ship_w=40
        self.ship_h=60
        
        self.bullet_file=Path.cwd()/"Assets"/"images"/"laserBlast.png"
        self.laser_sound=Path.cwd()/"Assets"/"sound"/"laser.mp3"

        self.impact=Path.cwd()/"Assets"/"sound"/"impactSound.mp3"

        self.alien_file=Path.cwd()/"Assets"/"images"/"enemy_4.png"
        
        self.alien_w=40
        self.alien_h=40
        self.fleet_direction=1

        self.button_w=200
        self.button_h=50
        self.button_color=(0,135,50)

        self.text_color=(255,255,255)
        self.button_font_size=48
        self.HUD_font_size=20
        self.font_file=Path.cwd()/"Assets"/"Fonts"/"Silkscreen"/"Silkscreen-Bold.ttf"

    def initialize_dynamic_settings(self):
        """Settings that can be changed during in-game progression
        """
        self.ship_speed=5
        self.starting_ship_count=3
        self.bullet_speed=7
        self.bullet_amount=5
        self.bullet_w=25
        self.bullet_h=80
        self.fleet_speed=2
        self.fleet_drop_speed=40
        self.alien_points=50
    
    def increase_difficulty(self):
        """Increases the speed of ship, bullets and aliens every new level
        """
        self.ship_speed*=self.difficulty_scale
        self.bullet_speed*=self.difficulty_scale
        self.fleet_speed*=self.difficulty_scale




