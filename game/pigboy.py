import pyglet
from pyglet.window import key
from . import resources
import math

class Pigboy(pyglet.sprite.Sprite):
    """Class for main character Pigboy."""
    def __init__(self, *args, **kwargs):
        super().__init__(img=resources.pigboy_img, *args, **kwargs)

        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.dead = False
        self.walk_speed = 4
        self.run_speed = 7
        self.key_handler = key.KeyStateHandler()
        self.index = 1
        self.facing_right = True
        self.scale = 0.75

    def update(self, dt):
        if self.key_handler[key.LSHIFT]:
            self.walking(dt, walk_speed=self.run_speed)
        else:
            self.walking(dt, walk_speed=self.walk_speed)

    def walking(self, dt, walk_speed):
        """Allow pig to walk, and control animation"""
        if self.key_handler[key.RIGHT]:
            self.x += walk_speed
            self.animate_pig(dt)
            self.facing_right = True
        if self.key_handler[key.LEFT]:
            self.x -= walk_speed
            self.animate_pig(dt, False)
            self.facing_right = False
        if not self.key_handler[key.RIGHT] | self.key_handler[key.LEFT]:
            self.index = 1
            if self.facing_right:
                self.image = resources.pigboy_img
            else:
                self.image = resources.pigboy_img.get_transform(flip_x=True)

    def animate_pig(self, dt, right=True):
        """Animate the pigboy sprite."""
        # We don't want the animation loop to move as
        # fast as the scheduled interval, so we allow for each
        # image to remain on the screen longer by dividing it by
        # another fraction
        self.index += (dt // (1/59.5))
        self.index = int(self.index)
        if self.index >= len(resources.pigboy_imgs):
            self.index = 1
        if right:
            self.image = resources.pigboy_imgs[self.index]
        else:
            self.image = resources.pigboy_imgs[self.index].get_transform(flip_x=True)
