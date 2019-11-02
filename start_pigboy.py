import pyglet
from game import pigboy, platform, util

game_window = pyglet.window.Window(800, 600)
pyglet.gl.glClearColor(0.3,0.4,0.6,0)

main_batch = pyglet.graphics.Batch()

# Characters
pigboy_sprite = pigboy.Pigboy(x=300, y=300, batch=main_batch)

crd_list = [(300, 60), (600, 200), (10, 300)]

platform_list = []
for crd in crd_list:
    platform_list.append(platform.Platform(x=crd[0], y=crd[1], batch=main_batch))
game_objects = [pigboy_sprite]

game_window.push_handlers(pigboy_sprite)
game_window.push_handlers(pigboy_sprite.key_handler)

@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()

def update(dt):
    pigboy_sprite.update(dt, platform_list)

if __name__ == '__main__': 
    pyglet.clock.schedule_interval(update, 1/240.0)
    pyglet.app.run()
