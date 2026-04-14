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

        self.ship_file=Path.cwd()/"Assets"/"images"/"ship2(no bg).png"
        self.ship_w=40
        self.ship_h=60
        self.ship_speed=5

        self.bullet_file=Path.cwd()/"Assets"/"images"/"laserBlast.png"
        self.laser_sound=Path.cwd()/"Assets"/"sound"/"laser.mp3"
        self.bullet_speed=7
        self.bullet_w=25
        self.bullet_h=80
        self.bullet_amount=5

        self.alien_file=Path.cwd()/"Assets"/"images"/"enemy_4.png"
        self.fleet_speed=5
        self.fleet_drop_speed=40
        self.alien_w=40
        self.alien_h=40
        self.fleet_direction=1


