import pyglet
from game import pigboy, platform, util, constants, enemy

game_window = pyglet.window.Window(constants.W_WIDTH, constants.W_HEIGHT)
pyglet.gl.glClearColor(0.3,0.4,0.6,0)

main_batch = pyglet.graphics.Batch()

# Characters
pigboy_sprite = pigboy.Pigboy(x=300, y=300, batch=main_batch)

crd_list = [(870, 180), (300, -15), (600, 180), (10, 280), (1300, 300)]

platform_list = []
for crd in crd_list:
    platform_list.append(platform.Platform(x=crd[0], y=crd[1], batch=main_batch))

# Enemy
ghost_enemy = enemy.Enemy(x=301, y=301, platform=platform_list[0], batch=main_batch)

game_list = platform_list + [ghost_enemy]

game_window.push_handlers(pigboy_sprite)
game_window.push_handlers(pigboy_sprite.key_handler)

@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()

def update(dt):
    pigboy_sprite.update(dt, platform_list, game_list)
    ghost_enemy.update(dt)

if __name__ == '__main__': 
    pyglet.clock.schedule_interval(update, 1/240.0)
    pyglet.app.run()
