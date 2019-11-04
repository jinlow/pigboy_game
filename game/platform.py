import pyglet
from . import resources

class Platform(pyglet.sprite.Sprite):
    """Generic game platform class"""
    def __init__(self, *args, **kwargs):
        super().__init__(img = resources.pltfm_short_grass, *args, **kwargs)

        self.ytop = self.y + (self.height // 2)
