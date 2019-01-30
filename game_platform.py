import pygame
# import sys
import os
from pygame.sprite import Sprite

class Platform(Sprite):
    def __init__(self, screen, xloc, yloc, w, h):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((w, h))
        self.image.fill((10, 100, 200))
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc
