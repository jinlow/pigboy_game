import pyglet

class GameObject(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwards)

    self.velocity_x, self.velocity_y = 0.0, 0.0
    self.dead = False

    
