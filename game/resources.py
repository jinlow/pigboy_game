"""Contains game resouces used throughout, such as images."""
import pyglet
import glob
from pyglet.image import Animation


pyglet.resource.path = ['resources']
pyglet.resource.reindex()

### Pigboy Resources ###

# Get images
pigboy_img = pyglet.resource.image('pg_moving0R.png')

image_paths = glob.glob(pathname="resources/*R.png")
image_paths.sort()
# Create pigboy animation
pigboy_imgs = []
for path in image_paths:
    path = path.split("/")[1]
    img = pyglet.resource.image(path)
    img.anchor_x = img.width // 2
    pigboy_imgs.append(pyglet.resource.image(path))

pigboy_imgsL = []
for img in pigboy_imgs:
    pigboy_imgsL.append(img.get_transform(flip_x=True))



pigboy_animationR = Animation.from_image_sequence(pigboy_imgs, 1/20.0)
pigboy_animationL = Animation.from_image_sequence(pigboy_imgsL, 1/20.0)

### Platform Resources ###
pltfm_short_grass = pyglet.resource.image("platform_grass.png")
pltfm_short_grass.anchor_x = pltfm_short_grass.width // 2
pltfm_short_grass.anchor_y = pltfm_short_grass.height
