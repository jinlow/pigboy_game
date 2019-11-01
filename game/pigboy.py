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
        self.walk_speed = 4
        self.run_speed = 2
        self.key_handler = key.KeyStateHandler()
        self.facing_right = True
        self.scale = 0.75
        self.fall_init = 0
        self.jumping = False
        self.jump_force = 0
        self.change_x = 0
        self.change_y = 0
        self.collision_id = 0

    def update(self, dt, platform_list):
        if self.key_handler[key.LSHIFT]:
            self.walking(dt, walk_speed=self.walk_speed*self.run_speed)
        else:
            self.walking(dt, walk_speed=self.walk_speed)

        self.calc_grav()
        self.jump(dt)
        self.y += self.change_y

        self.x += self.change_x
        collision_list = self.collide_list(platform_list)
        for platform in collision_list:
            if ((self.y - (self.height // 2)) <
                 (platform.y - (platform.height // 2))):
                x_adjust = (platform.width // 2) + (self.width // 2)
                if self.change_x > 0:
                    self.x = platform.x - x_adjust - 2
                elif self.change_x < 0:
                    self.x = platform.x + x_adjust + 2


        for platform in collision_list:
            y_adjust = (platform.height // 2) + (self.height // 2)
            self.jumping = False
            if self.change_y > 0:
                self.y = platform.y - y_adjust
                self.change_y = 0
                self.jumping = False
            elif self.change_y < 0:
                self.y = platform.y + y_adjust
                self.change_y = 0
                self.jumping = False

        self.change_x = 0


    def walking(self, dt, walk_speed):
        """Allow pig to walk, and control animation"""
        # If a new collision happens, stop walking
        if self.key_handler[key.RIGHT]:
            self.change_x += walk_speed
            if self.image != resources.pigboy_animationR:
                self.image = resources.pigboy_animationR
                # self.side_collision = False
            self.facing_right = True

        if self.key_handler[key.LEFT]:
            self.change_x -= walk_speed
            if self.image != resources.pigboy_animationL:
                self.image = resources.pigboy_animationL
                # self.side_collision = False
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
        if self.key_handler[key.SPACE] and not self.jumping:
            self.jumping = True
            self.change_y = 15

    def calc_grav(self):
        """Calculate effect of gravity"""
        if self.change_y == 0:
            self.change_y = -1
        else:
            self.change_y -= 0.5

    def gravity(self, dt, collision_list):
        """Enact gravity on the pig."""
        self.y -= self.fall_init
        self.fall_init += 0.1

    def collide_list(self, platform_list):
        """Check for collision and handle"""
        return [platform for platform in platform_list
                if util.point_collide(self, platform)]

    def handle_collisions(self, collide_list):
        """Deal with platforms in collision list"""
        for object in collision_list:
            if self.change_x > 0:
                self.fall_init = 0
                self.y = plat.ytop + (self.height // 2)
                self.falling = False
