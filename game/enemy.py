import pyglet
from . import resources
from . import platform
from . import util

class Enemy(pyglet.sprite.Sprite):
    """
    Base Enemy Class:
        Class for game enemies.
        A platform is provided on creation of an enemy class
        This is the platform the enemy is tethered too, and 
        uses for the walk space.
    """
    def __init__(self, platform: platform.Platform = None, *args, **kwargs):
        super().__init__(img=resources.enemy_ghostR, *args, **kwargs)
        self.scale = 0.15
        self.x_range = None
        self.direction = 1
        self.walk_speed = 2.5
        self.platform = platform
        self.tether_to_platform()

    def tether_to_platform(self):
        """
        Tether Enemy:
            Tether the enemy class to a specific platform.
        """
        if self.platform is not None:
            y_up = (self.platform.height // 2) + self.platform.y
            self.y = y_up + (self.height // 2)
            self.x = self.platform.x

    def update(self, dt):
        self.x += self.walk_speed*self.direction
        plat_edge_r = self.platform.x + (self.platform.width // 2)
        plat_edge_l = self.platform.x - (self.platform.width // 2)
        char_r = self.width // 2
        if (self.x - char_r) < plat_edge_l:
            self.direction = 1
            self.image = resources.enemy_ghostR
        if (self.x + char_r) > plat_edge_r:
            self.direction = -1
            self.image = resources.enemy_ghostL





