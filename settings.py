from pathlib import Path
class Settings:
    def __init__(self):
        self.name: str="Alien Invasion"
        self.screen_w:int=1200
        self.screen_h:int=800
        self.fps:int=60
        self.bg_file=Path.cwd()/"Assets"/"images"/"Starbasesnow.png"
