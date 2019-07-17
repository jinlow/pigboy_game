import pyglet
from . import resources

class Platform(pyglet.sprite.Sprite):
    """Generic game platform class"""
    def __init__(self, *args, **kwargs):
        super().__init__(img = resources.pltfm_short_grass, *args, **kwargs)

        # Change image anchor to be the upper middle
        # self.image.anchor_x = self.image.width // 2
        # self.image.anchor_y = 0
