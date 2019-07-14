import pyglet
import glob
from pyglet.image import Animation

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

# Get images
pigboy_img = pyglet.resource.image('pg_moving0R.png')

image_paths = glob.glob(pathname="resources/*.png")
image_paths.sort()
# Create pigboy animation
pigboy_imgs = []
for path in image_paths:
    path = path.split("/")[1]
    img = pyglet.resource.image(path)
    img.anchor_x = img.width // 2
    pigboy_imgs.append(pyglet.resource.image(path))

pigboy_animation = Animation.from_image_sequence(pigboy_imgs, 1/20.0)
