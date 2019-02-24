import pygame
from pygame.sprite import Sprite
import glob

class Pigboy(pygame.sprite.Sprite):
    """ Class to define the game character Pigboy."""

    def __init__(self, screen, g_sets, platforms):

        super().__init__()

        """Initialize Pigboy"""
        self.screen = screen
        self.g_sets = g_sets

        # Load all images for animation
        self.images = []
        self.upload_images()

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

        # Falling force
        self.moving_y = 0

        # Set plaforms
        self.platforms = platforms

    def upload_images(self):
        """ Append animation images. """
        img_pathnames = glob.glob("images/pg/moving_right/pg_moving*")
        img_pathnames.sort()

        for path in img_pathnames:
            self.images.append(pygame.image.load(path))

    def update(self):
        """Update pigboys position based on the movement flag."""

        # Animation
        self.animate()

        # Pigboy motion
        self.jump()
        self.gravity()
        self.walking()

        # Check for collisions
        obj_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for platform in obj_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.moving_y > 0:
                self.rect.bottom = platform.rect.top
#               self.moving_left = False
#               self.moving_right = False
            elif self.moving_y < 0:
                self.rect.top = platform.rect.bottom
#               self.moving_left = False
#               self.moving_right = False

            # Stop our vertical movement
            self.moving_y= 0

    def walking(self):
        """The action of moving Pigboy."""
        if self.running:
            run_factor = self.g_sets.pig_run_factor
        else:
            run_factor = 1

        # Now walk
        if self.moving_right and self.rect.right < self.screen_rect.right - 30:
            self.center += self.g_sets.pig_walk_velocity*run_factor
        if self.moving_left and self.rect.left > self.screen_rect.left + 30:
           self.center -= self.g_sets.pig_walk_velocity*run_factor

        self.rect.centerx = self.center

    def gravity(self):
        """ Enact gravity on the pig """
        if self.moving_y == 0:
             self.moving_y = 1
        else:

            self.moving_y += 4

        if self.rect.y >= (self.g_sets.screen_height - self.rect.height) and self.moving_y >= 0:
            self.rect.y = (self.g_sets.screen_height - self.rect.height)
            self.moving_y = 0

        # Enact gravity
        self.rect.y += self.moving_y

    def jump(self):
        """Make Pigboy jump when the space bar is pressed."""
        if self.jumping_up:
            self.moving_y = - self.g_sets.pig_jump_velocity
            self.jumping_up = False

    def animate(self):
        """Animate Pigboys walking/jumping"""
        if self.facing_right:
            if self.moving_right:
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]
            else:
                self.index = 0
                self.image = self.images[self.index]

        else:
            if self.moving_left:
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
