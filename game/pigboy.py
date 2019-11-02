import pyglet
from pyglet.window import key
from . import resources
from . import util
import math
from . import platform

class Pigboy(pyglet.sprite.Sprite):
    """Class for main character Pigboy."""
    def __init__(self, *args, **kwargs):
        super().__init__(img=resources.pigboy_img, *args, **kwargs)

        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.colR = False
        self.colL = False
        self.walk_speed = 4
        self.run_speed = 2
        self.key_handler = key.KeyStateHandler()
        self.facing_right = True
        self.scale = 0.75
        self.fall_init = 0
        self.jumping = False
        self.jump_force = 0
        self.collision_id = None
        self.side_collision = False
        self.new_collision = False
        self.y_speed = 8

    def update(self, dt: int, platform_list: list) -> None:
        """Process and handle collisions"""
        y_speed = self.y_speed
        walk_speed = self.walk_speed
        for plat in platform_list:
            if self.collide(plat):
                print("We've been hit!!!")
                y_speed = 0
            else:
                print("All clear :)")
        self.walking_or_run(dt, walk_speed=walk_speed)
        self.fly(dt, y_speed=y_speed)


    def walking_or_run(self, dt: int, walk_speed: int) -> None:
        """Control if the pig is walking or running"""
        if self.key_handler[key.LSHIFT]:
            self._walking(dt, walk_speed=self.walk_speed*self.run_speed)
        else:
            self._walking(dt, walk_speed=self.walk_speed)

    def _walking(self, dt: int, walk_speed) -> None:
        """Allow pig to walk, and control animation"""
        if self.key_handler[key.RIGHT]:
            self.x += walk_speed
            if self.image != resources.pigboy_animationR:
                self.image = resources.pigboy_animationR
                self.side_collision = False
            self.facing_right = True

        if self.key_handler[key.LEFT]:
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

    def fly(self, dt: int, y_speed: int) -> None:
        """Allow Pigboy to fly to test collision"""
        if self.key_handler[key.UP]:
            self.y += y_speed
        if self.key_handler[key.DOWN]:
            self.y -= y_speed

    def jump(self, dt: int) -> None:
        """Jump in the air"""
        if (self.key_handler[key.SPACE] and self.fall_init == 0
        and not self.jumping):
            self.jumping = True
            self.jump_force = 10
            self.side_collision = False

        if self.jump_force > 0:
            self.y += self.jump_force
            self.jump_force -= 0.1
        else:
            self.jumping = False
            self.jump_force = 0

    def gravity(self, dt: int, plat_collision: list, plat) -> None:
        """Enact gravity on the pig."""
        if not self.side_collision:
            if plat_collision:
                self.fall_init = 0
                self.y = plat.ytop + (self.height // 2)
                self.falling = False
            else:
                self.y -= self.fall_init
                self.fall_init += 0.1

    def collide(self, plat: platform.Platform) -> bool:
        """Check for collision and handle"""
        return util.point_collide(self, plat)

