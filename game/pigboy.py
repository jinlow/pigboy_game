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
        self.walk_speed = 4.5
        self.run_speed = 2
        self.key_handler = key.KeyStateHandler()
        self.facing_right = True
        self.scale = 0.75
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
        Update Pigboy
            Process and handle collisions walking and 
            interaction with other sprites.
        """
        # TODO: Some kind of locational collision restriction needs to be 
        #       added.
        y_speed = self.y_speed
        walk_speed = self.walk_speed
        for plat in platform_list:
            collision = self.collide(plat, epsilon=3)
            pig_bot = self.y - self.height / 2
            plt_top = plat.y + plat.height / 2
            if collision and self.y_force > 0:
                y_adjust = (plat.height // 2) + (self.height // 2)
                self.y_force = 0
                self.y = plat.y + y_adjust
                self.jumping = False
            if collision and self.y_force < 0:
                y_adjust = (plat.height // 2) + (self.height // 2)
                self.y_force = 0
                self.y = plat.y - y_adjust - 10
                self.jumping = False
            # Check for if standing collision
            if collision and (pig_bot < plt_top - 10) and self.y_force == 0:
                walk_speed = 0
                x_adjust = (plat.width // 2) + (self.width // 2)
                if self.facing_right:
                    self.x = plat.x - x_adjust
                else:
                    self.x = plat.x + x_adjust
            if collision and collision and (pig_bot < plt_top - 10) and self.jumping:
                walk_speed = 0
        self.walking_or_run(dt, walk_speed=walk_speed)
        self.fly(dt, y_speed=y_speed)
        self.jump(dt)
        self.gravity(dt)


    def walking_or_run(self, dt: int, walk_speed: int) -> None:
        """
        Run or Walk
            Control if the pig is walking or running
        """
        if self.key_handler[key.LSHIFT]:
            self._walking(dt, walk_speed=self.walk_speed*self.run_speed)
        else:
            self._walking(dt, walk_speed=self.walk_speed)

    def _walking(self, dt: int, walk_speed) -> None:
        """
        Walk that Pig
            Allow pig to walk, and control animation
        """
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
        """
        Allow Pigboy to fly to test collision
            - Debugging Function
        """
        if self.key_handler[key.UP]:
            self.y += y_speed
        if self.key_handler[key.DOWN]:
            self.y -= y_speed

    def _jump(self, dt: int):
        pass 

    def jump(self, dt: int) -> None:
        """
        Jump in the air
            This funtion just provides the upward momentum,
            the gravtiy() method brings the pig back down.
        """
        if (self.key_handler[key.SPACE] and self.y_force == 0 and not self.jumping):
            self.jumping = True
            self.y_force = -1*self.jump_force

    def gravity(self, dt: int) -> None:
        """Enact gravity on the pig."""
        self.y -= self.y_force
        self.y_force += self.gforce

    def collide(self, plat: platform.Platform, epsilon: int) -> bool:
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
