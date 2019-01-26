import pygame
from pygame.sprite import Sprite
import glob

class Pigboy(pygame.sprite.Sprite):
    """ Class to define the game character Pigboy."""

    def __init__(self, screen, g_sets):
        pygame.sprite.Sprite.__init__(self)
        """Initialize Pigboy"""
        self.screen = screen
        self.g_sets = g_sets

        # # Load image and get rect
        # self.image = pygame.image.load("images/pg/pg_sketch_flat_small.bmp")

        # Load all images for animation
        self.images = []
        self.images.append(pygame.image.load("images/pg/moving_right/pg_moving0R.bmp"))
        self.images.append(pygame.image.load("images/pg/moving_right/pg_moving1R.bmp"))
        self.images.append(pygame.image.load("images/pg/moving_right/pg_moving2R.bmp"))
        self.images.append(pygame.image.load("images/pg/moving_right/pg_moving3R.bmp"))
        self.images.append(pygame.image.load("images/pg/moving_right/pg_moving4R.bmp"))
        self.images.append(pygame.image.load("images/pg/moving_right/pg_moving5R.bmp"))
        self.images.append(pygame.image.load("images/pg/moving_right/pg_moving6R.bmp"))
        self.images.append(pygame.image.load("images/pg/moving_right/pg_moving7R.bmp"))
        self.images.append(pygame.image.load("images/pg/moving_right/pg_moving8R.bmp"))
        self.images.append(pygame.image.load("images/pg/moving_right/pg_moving9R.bmp"))
        # self.pathnames = glob.glob("images/pg/moving_right/pg_moving*")
        # self.pathnames.sort()
        #
        # self.upload_images()
        # for path in self.pathnames:
        #     self.images.append(pygame.image.load(path)

        # Set the initial index for the image
        self.index = 0

        # Set starting image
        self.image = self.images[self.index]

        # Get rect from image
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start at bottom center of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.g_sets.pg_start_height

        # Store a decimal value for the characters center.
        self.center = float(self.rect.centerx)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.jumping_up = False

        # Facing flags
        self.facing_right = True

        self.running = False

        # Falling Flag
        self.falling = True

    def update(self):
        """Update pigboys position based on the movement flag."""
        # Run faster if SHIFT key is pressed...
        if self.running:
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.center += self.g_sets.pig_walk_velocity*self.g_sets.pig_run_factor
            if self.moving_left and self.rect.left > self.screen_rect.left:
                self.center -= self.g_sets.pig_walk_velocity*self.g_sets.pig_run_factor
        else:
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.center += self.g_sets.pig_walk_velocity
            if self.moving_left and self.rect.left > self.screen_rect.left:
                self.center -= self.g_sets.pig_walk_velocity
        self.rect.centerx = self.center

        # Collision with platforms (later enemies)

    def gravity(self, platform, g_sets):
        """ Check if player is falling """
        if self.falling:
            Frce = - ( 0.5 * self.g_sets.pig_mass *
                    (self.g_sets.pig_jump_velocity**2))

            self.rect.y -= Frce

        # if self.rect.y >= (self.g_sets.screen_height - self.rect.height):
        #    self.falling = False
        #if self.rect.colliderect(platform.rect):
            # self.falling = False
            # self.y = (platform.rect.y-g_sets.p1_h)
        if self.rect.y >= (self.g_sets.screen_height - self.rect.height):
            self.rect.y = (self.g_sets.screen_height - self.rect.height)
            self.falling = False
            self.g_sets.pig_jump_velocity = self.g_sets.pig_jump_cap

    def jump(self):
        """Make Pigboy jump when the space bar is pressed."""
        if self.jumping_up:
            if self.g_sets.pig_jump_velocity > 0:
                Frce = ( 0.5 * self.g_sets.pig_mass *
                        (self.g_sets.pig_jump_velocity**2))
            else:
                Frce = - ( 0.5 * self.g_sets.pig_mass *
                        (self.g_sets.pig_jump_velocity**2))

            # Change Position
            self.rect.y -= Frce

            # Change velocity
            self.g_sets.pig_jump_velocity = (self.g_sets.pig_jump_velocity -
                                             self.g_sets.pig_jump_decay)

            # If ground is reached reset variables.
            if self.rect.y >= (self.g_sets.screen_height - self.rect.height):
                self.rect.y = (self.g_sets.screen_height - self.rect.height)
                self.jumping_up = False
                self.g_sets.pig_jump_velocity = self.g_sets.pig_jump_cap

            # Collision
    # def hiting_things(self):
    #     """Check if we hit anything and adjust position accordingly."""
    #     block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
    #     for block in block_hit_list


    def animate(self):
        """Animate Pigboys walking/jumping"""
        if self.facing_right:
            if self.moving_right and not(self.jumping_up):
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]
            else:
                self.index = 0
                self.image = self.images[self.index]

        else:
            if self.moving_left and not(self.jumping_up):
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = pygame.transform.flip(self.images[self.index], True, False)
            else:
                self.index = 0
                self.image = pygame.transform.flip(self.images[self.index], True, False)



    def blitme(self):
        """Draw Pigboy at current location."""
        self.screen.blit(self.image, self.rect)
