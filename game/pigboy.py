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
        self.collision_id = None
        self.side_collision = False

    def update(self, dt, plat):
        print(self.fall_init)
        plat_collision = self.collide(plat)
        # self.fly(dt)
        self.jump(dt)
        if self.key_handler[key.LSHIFT]:
            self.walking(dt, plat_collision, plat, walk_speed=self.walk_speed*self.run_speed)
        else:
            self.walking(dt, plat_collision, plat, walk_speed=self.walk_speed)
        if plat_collision:
            self.collision_id = plat.platform_id
        self.gravity(dt, plat_collision, plat)

    def walking(self, dt, plat_collision, plat, walk_speed):
        """Allow pig to walk, and control animation"""
        # If a new collision happens, stop walking
        if self.key_handler[key.RIGHT]:
            if (plat_collision and (self.collision_id != plat.platform_id)
            and (self.collision_id is not None)):
                self.x -= (walk_speed + 2)
                walk_speed = 0
                self.side_collision = True
            self.x += walk_speed
            if self.image != resources.pigboy_animationR:
                self.image = resources.pigboy_animationR
                self.side_collision = False
            self.facing_right = True

        if self.key_handler[key.LEFT]:
            if (plat_collision and (self.collision_id != plat.platform_id)
            and (self.collision_id is not None)):
                self.x += (walk_speed + 2)
                walk_speed = 0
                self.side_collision = True
            self.x -= walk_speed
            if self.image != resources.pigboy_animationL:
                self.image = resources.pigboy_animationL
                self.side_collision = False
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
            self.jump_force = 10
            self.side_collision = False

        if self.jump_force > 0:
            self.y += self.jump_force
            self.jump_force -= 0.1
            print("jumping")
        else:
            self.jumping = False
            self.jump_force = 0

    def gravity(self, dt, plat_collision, plat):
        """Enact gravity on the pig."""
        if not self.side_collision:
            if plat_collision:
                self.fall_init = 0
                self.y = plat.ytop + (self.height // 2)
                self.falling = False
            else:
                self.y -= self.fall_init
                self.fall_init += 0.1

    def collide(self, plat):
        """Check for collision and handle"""
        return util.point_collide(self, plat)
