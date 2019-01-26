import pygame
# import sys
import os
from pygame.sprite import Sprite

class Platform(Sprite):
    def __init__(self, screen, g_sets):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.g_sets = g_sets
        self.image = pygame.Surface((self.g_sets.p1_w, self.g_sets.p1_h))
        self.image.fill(self.g_sets.p1_color)
        self.rect = self.image.get_rect()
        self.rect.x = self.g_sets.p1_xloc
        self.rect.y = self.g_sets.p1_yloc

    def blitme(self):
        """Draw the platform at its current location."""
        self.screen.blit(self.image, self.rect)

# class Platform(Sprite):
#     """ x location, y location, img width, img height, img file."""
#     def __init__(self, screen, g_sets):
#         #pygame.sprite.Sprite.__init__(self)
#         super(Platform, self).__init__()
#         self.screen = screen
#         self.g_sets = g_sets
#
#         # Load images
#         self.image = pygame.image.load(os.path.join('images/platforms',
#                                         self.g_sets.p1_img_path)).convert()
#
#         #self.image = pygame.image.load('images/platforms/platform_test.bmp')
#         self.image.convert_alpha()
#
#         self.rect = self.image.get_rect()
#
#         self.rect.y = self.g_sets.p1_yloc
#         self.rect.x = self.g_sets.p1_xloc
#
#         self.x = float(self.rect.x)
#
#     def blitme(self):
#         """Draw the platform at its current location."""
#         self.screen.blit(self.image, self.rect)
