import pyglet
from pyglet.window import key
from . import resources
from . import util
import math
from . import platform

class Pigboy(pyglet.sprite.Sprite):
    """
    Base Pigboy Game Character Class:
        Class for main character Pigboy.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(img=resources.pigboy_img, *args, **kwargs)

        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.colR = False
        self.colL = False
        self.walk_speed = 4.5
        self.run_speed = 2
        self.key_handler = key.KeyStateHandler()
        self.facing_right = True
        self.scale = 0.74
        self.fall_init = 0
        self.jumping = False
        self.y_force = 0
        self.collision_id = None
        self.side_collision = False
        self.new_collision = False
        self.y_speed = 8
        self.gforce = 0.5
        self.jump_force = 15

    def update(self, dt: int, platform_list: list) -> None:
        """
        Update Pigboy:
            Process and handle collisions walking and 
            interaction with other sprites.

            Notes: This may need to be reworked in the future to
            make it cleaner, but for now this works as I want it 
            to, and for this many platforms it is sufficiently 
            fast.
        """
        # Report change in x
        # TODO: Make this directly handled by object attribute
        walk_delta = self.walking_or_run(dt)

        # Handle Horizontal collision
        self.x += walk_delta
        for plat in self.plat_collide_list(platform_list, -0.5):
            x_adjust = (plat.width / 2) + (self.width / 2)
            if walk_delta > 0:
                self.x = plat.x - x_adjust - 1
            if walk_delta < 0:
                self.x = plat.x + x_adjust + 1

        # Handle Vertical Collision
        self.jump(dt)
        self.y -= self.y_force
        self.gravity(dt)
        for plat in self.plat_collide_list(platform_list):
            y_adjust = (plat.height / 2) + (self.height / 2)
            if self.y_force < 0:
                self.y = plat.y - y_adjust - 3
                self.y_force = 0
            if self.y_force > 0:
                self.y = plat.y + y_adjust
                self.y_force = 0
                self.jumping = False

    def walking_or_run(self, dt: int) -> int:
        """
        Run or Walk:
            Control if the pig is walking or running.
        """
        if self.key_handler[key.LSHIFT]:
            return self._walking(dt)*self.run_speed
        else:
            return self._walking(dt)

    def _walking(self, dt: int) -> int:
        """
        Walk that Pig:
            Allow pig to walk, and control animation
        """
        walk_delta = 0
        if self.key_handler[key.RIGHT]:
            # self.x += walk_speed
            walk_delta = self.walk_speed
            if self.image != resources.pigboy_animationR:
                self.image = resources.pigboy_animationR
                self.side_collision = False
            self.facing_right = True

        if self.key_handler[key.LEFT]:
            # self.x -= walk_speed
            walk_delta = -1*self.walk_speed
            if self.image != resources.pigboy_animationL:
                self.image = resources.pigboy_animationL
                self.side_collision = False
            self.facing_right = False

        if not self.key_handler[key.RIGHT] | self.key_handler[key.LEFT]:
            if self.facing_right:
                self.image = resources.pigboy_img
            else:
                self.image = resources.pigboy_img.get_transform(flip_x=True)
        
        return walk_delta

    def fly(self, dt: int, y_speed: int) -> None:
        """
        Allow Pigboy to fly to test collision
            - Debugging Function
        """
        if self.key_handler[key.UP]:
            self.y += y_speed
        if self.key_handler[key.DOWN]:
            self.y -= y_speed

    def jump(self, dt: int) -> None:
        """
        Jump in the air
            This funtion just provides the upward momentum,
            the gravtiy() method brings the pig back down.
        """

        if (self.key_handler[key.SPACE] and self.y_force == 0 and not self.jumping):
            self.jumping = True
            self.y_force = -1*self.jump_force

    def gravity(self, dt: int, off: bool = False) -> None:
        """
        Gravity function
            Enact gravity on the pig.
        """
        if not off:
            self.y_force += self.gforce

    def collide(self, plat: platform.Platform, epsilon: float) -> bool:
        """
        Check for collision and return collision type
            plat: Platform to check for collision
            epsilon: Pixel distance to check.
        """
        gpts = util.object_points(self)
        ppts = util.object_points(plat)

        # Check upper left and lower right Pigboy by epsilon
        gpts_top = tuple([point + epsilon for point in gpts[0]])
        gpts_bot = tuple([point - epsilon for point in gpts[1]])

        collide = (util.point_collide(tuple([gpts_top, gpts_bot]), ppts))
        
        return collide

    def plat_collide_list(self, platform_list: list, epsilon: float = 0) -> list:
        """
        Collision List
            Loop through platforms and check if player
            and platform have collided.
        """
        collide_list = [plat for plat in platform_list if 
                        self.collide(plat, epsilon)]

        return collide_list
