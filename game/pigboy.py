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
        self.colR = False
        self.colL = False
        self.walk_speed = 2
        self.run_speed = 2
        self.key_handler = key.KeyStateHandler()
        self.facing_right = True
        self.scale = 0.75
        self.fall_init = 0
        self.jumping = False
        self.jump_force = 0

    def update(self, dt, plat):
        plat_collision = self.collide(plat)
        self.jump(dt)
        self.gravity(dt, plat_collision, plat)
        # self.fly(dt)
        if self.key_handler[key.LSHIFT]:
            self.walking(dt, walk_speed=self.walk_speed*self.run_speed)
        else:
            self.walking(dt, walk_speed=self.walk_speed)

    def walking(self, dt, walk_speed):
        """Allow pig to walk, and control animation"""
        if self.key_handler[key.RIGHT]: # and cold_type != 0:
            # if 0 in plat_collide_list and self.facing_right:
            #     walk_speed = 0
            self.x += walk_speed
            if self.image != resources.pigboy_animationR:
                self.image = resources.pigboy_animationR
            self.facing_right = True

        if self.key_handler[key.LEFT]:
            # if 0 in plat_collide_list and not self.facing_right:
            #     walk_speed = 0
            self.x -= walk_speed
            if self.image != resources.pigboy_animationL:
                self.image = resources.pigboy_animationL
            self.facing_right = False

        if not self.key_handler[key.RIGHT] | self.key_handler[key.LEFT]:
            if self.facing_right:
                self.image = resources.pigboy_img
            else:
                self.image = resources.pigboy_img.get_transform(flip_x=True)

    def fly(self, dt):
        """Allow Pigboy to fly to test collision"""
        if self.key_handler[key.UP]:
            self.y += 3
        if self.key_handler[key.DOWN]:
            self.y -= 3

    def jump(self, dt):
        """Jump in the air"""
        if (self.key_handler[key.SPACE] and self.fall_init == 0
        and not self.jumping):
            self.jumping = True
            self.jump_force = 25

        if self.jump_force > 0:
            self.y += self.jump_force
            self.jump_force -= 0.5
            print("jumping")
        else:
            self.jumping = False
            self.jump_force = 0

    def gravity(self, dt, plat_collision, plat):
        """Enact gravity on the pig."""
        if plat_collision:
            self.fall_init = 0
            self.y = plat.y + (plat.height // 2) + (self.height // 2)
        else:
            self.y -= self.fall_init
            self.fall_init += 0.5

    def collide(self, plat):
        """Check for collision and handle"""
        return util.point_collide(self, plat)
