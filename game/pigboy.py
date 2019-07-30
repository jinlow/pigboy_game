import pyglet
from pyglet.window import key
from . import resources
from . import util
import math

class Pigboy(pyglet.sprite.Sprite):
    """Class for main character Pigboy."""
    def __init__(self, *args, **kwargs):
        super().__init__(img=resources.pigboy_img, *args, **kwargs)

        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.dead = False
        self.walk_speed = 2
        self.run_speed = 1.5
        self.key_handler = key.KeyStateHandler()
        self.index = 1
        self.facing_right = True
        self.scale = 0.75

    def update(self, dt, plat):
        if self.collide_one(plat) == 1:
            print("cool")
        if self.key_handler[key.LSHIFT]:
            self.walking(dt, walk_speed=self.walk_speed*self.run_speed)
        else:
            self.walking(dt, walk_speed=self.walk_speed)

    def walking(self, dt, walk_speed):
        """Allow pig to walk, and control animation"""
        if self.key_handler[key.RIGHT]:
            self.x += walk_speed
            if self.image != resources.pigboy_animationR:
                self.image = resources.pigboy_animationR
            self.facing_right = True
        if self.key_handler[key.LEFT]:
            self.x -= walk_speed
            if self.image != resources.pigboy_animationL:
                self.image = resources.pigboy_animationL
            self.facing_right = False
        if not self.key_handler[key.RIGHT] | self.key_handler[key.LEFT]:
            self.index = 1
            if self.facing_right:
                self.image = resources.pigboy_img
            else:
                self.image = resources.pigboy_img.get_transform(flip_x=True)

    def collide_one(self, platform):
        util.collide_one_to_one(self, platform)
