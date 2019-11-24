import pyglet
import time
from pyglet.window import key
from pyglet import sprite
from . import resources
from . import util
from . import platform
from . import constants

class Pigboy(sprite.Sprite):
    """
    Base Pigboy Game Character Class:
        Class for main character Pigboy.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(img=resources.pigboy_img, *args, **kwargs)

        self.colR = False
        self.colL = False
        self.walk_speed = 4.5
        self.run_speed = 2
        self.key_handler = key.KeyStateHandler()
        self.facing_right = True
        self.scale = 0.74
        self.jumping = False
        self.y_force = 0
        self.y_speed = 8
        self.gforce = 0.5
        self.jump_force = 15
        self.walk_delta = 0
        self.lives = 3
        self.enemy_collide = False
        self.block_time = 0.0

    def update(self, dt: int, platform_list: list, enemy_list: list, lives_list: list) -> None:
        """
        Update Pigboy:
            Process and handle collisions walking and 
            interaction with other sprites.

            Notes: This may need to be reworked in the future to
            make it cleaner, but for now this works as I want it 
            to, and for this many platforms it is sufficiently 
            fast.
        """
        # Handle Horizontal collision
        self.walking_or_run(dt)
        self.x += self.walk_delta
        self.handle_x_collision(platform_list)

        # Handle Vertical Collision
        self.jump(dt)
        self.y -= self.y_force
        self.gravity(dt)
        self.handle_y_collision(platform_list)

        # Handle Enemy Collisions
        self.handle_enemy_collision(enemy_list, lives_list)
        
        # Handle Camera
        self.handle_camera((platform_list + enemy_list))

    def handle_camera(self, platform_list: list) -> None:
        """
        Handle Camera Movement:
            If the character gets to close to the edge of the game 
            window, stop its movements, and shift all of the 
            game platforms.
        """
        r_side = self.x + (self.width / 2)
        l_side = self.x - (self.width / 2)
        t_side = self.y + (self.height / 2)
        b_side = self.y - (self.height / 2)
        r_wind = (constants.W_WIDTH - 200)
        l_wind = 0 + 200
        t_wind = (constants.W_HEIGHT - 15)
        b_wind = 0 + 30
        if (r_side > r_wind) & self.facing_right:
            self.x = r_wind - (self.width / 2)
            for plat in platform_list:
                plat.x -= self.walk_delta
        elif (l_side < l_wind) and not self.facing_right:
            self.x = l_wind + (self.width / 2)
            for plat in platform_list:
                plat.x -= self.walk_delta
        if (t_side > t_wind) and (self.y_force != 0):
            self.y = t_wind - (self.height / 2)
            for plat in platform_list:
                plat.y += self.y_force
        elif (b_side < b_wind) and (self.y_force != 0):
            self.y = b_wind + (self.height / 2)
            for plat in platform_list:
                plat.y += self.y_force

    def walking_or_run(self, dt: int) -> None:
        """
        Run or Walk:
            Control if the pig is walking or running.
        """
        if self.key_handler[key.LSHIFT]:
            self._walking(dt)
            self.walk_delta = self.walk_delta*self.run_speed
        else:
            self._walking(dt)

    def _walking(self, dt: int) -> None:
        """
        Walk that Pig:
            Allow pig to walk, and control animation
        """
        self.walk_delta = 0
        if self.key_handler[key.RIGHT]:
            self.walk_delta = self.walk_speed
            if self.image != resources.pigboy_animationR:
                self.image = resources.pigboy_animationR
            self.facing_right = True

        if self.key_handler[key.LEFT]:
            self.walk_delta = -1*self.walk_speed
            if self.image != resources.pigboy_animationL:
                self.image = resources.pigboy_animationL
            self.facing_right = False

        if not self.key_handler[key.RIGHT] | self.key_handler[key.LEFT]:
            if self.facing_right:
                self.image = resources.pigboy_img
            else:
                self.image = resources.pigboy_img.get_transform(flip_x=True)

    def _fly(self, dt: int, y_speed: int) -> None:
        """
        Allow Pigboy to fly:
            This is a debugging function to help test collision
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

    def handle_x_collision(self, platform_list: list) -> None:
        """
        Handle X Collision:
            Deal with a collision with the side of a platform.
        """
        for plat in self.plat_collide_list(platform_list, -0.5):
            x_adjust = (plat.width / 2) + (self.width / 2)
            if self.walk_delta > 0:
                self.x = plat.x - x_adjust - 1
            if self.walk_delta < 0:
                self.x = plat.x + x_adjust + 1

    def handle_y_collision(self, platform_list: list) -> None:
        """
        Handle Y Collision:
            Deal with collisions where pigboy lands on a 
            platform, or jumps up into one.
        """
        for plat in self.plat_collide_list(platform_list):
            y_adjust = (plat.height / 2) + (self.height / 2)
            if self.y_force < 0:
                self.y = plat.y - y_adjust - 3
                self.y_force = 0
            if self.y_force > 0:
                self.y = plat.y + y_adjust
                self.y_force = 0
                self.jumping = False

    def handle_enemy_collision(self, enemy_list: list, lives_list: list):
        """
        Handle Enemy Collision
            Deal with Pigboys collision with an enemy.
        """
        enemy_collide = self.plat_collide_list(enemy_list)
        if ((len(enemy_collide) > 0) and
              (len(lives_list) > 0) and 
              (self.block_time < time.time())):
            lives_list[0].delete()
            lives_list.pop(0)
            self.block_time = (time.time() + 1)
        elif len(enemy_collide) == 0:
            self.block_time = 0
