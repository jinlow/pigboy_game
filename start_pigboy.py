import pyglet
from game import pigboy, platform, util

game_window = pyglet.window.Window(800, 600)
pyglet.gl.glClearColor(0.3,0.4,0.6,0)

main_batch = pyglet.graphics.Batch()

# Characters
#pigboy_sprite = pigboy.Pigboy(x=300, y=100, batch=main_batch)
pigboy_sprite = pigboy.Pigboy(x=100, y=100, batch=main_batch)
# Create platforms
platform1 = platform.Platform(x=300, y=100, batch=main_batch)
platform2 = platform.Platform(x=600, y=300, batch=main_batch)

platform_list = [platform1, platform2]

game_objects = [pigboy_sprite]

game_window.push_handlers(pigboy_sprite)
game_window.push_handlers(pigboy_sprite.key_handler)

@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()

def update(dt):
    for obj in game_objects:
        obj.update(dt)
        #print(obj.position[1]+ (obj.height // 2))
        # print("obj")
        # print(obj.width // 2 + platform2.width // 2)
        # print(obj.position)
        # print(obj.position[1] + (obj.height // 2))
        # print(obj.position[1] - (obj.height // 2))
    for plat in platform_list:
        plat.update()
        util.collide_one_to_one(pigboy_sprite, plat)
        #print(plt.position[1] - plt.height)
        # print(plat.position)
        # print(plat.position[1])
        # print(plat.position[1] - plat.height)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/240.0)
    # print(platform1.height)
    # print(pigboy_sprite.width // 2 + platform1.width // 2)
    # print(pigboy_sprite.position[1] + (pigboy_sprite.height // 2))
    # print(pigboy_sprite.position[1] - (pigboy_sprite.height // 2))
    # print(platform1.position[1])
    # print(platform1.position[1] - platform1.height)
    pyglet.app.run()
