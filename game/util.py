import math
import operator as op

def distance(point_1=(0, 0), point_2=(0, 0)):
    """Return the distance between two points"""
    euc_dist = (math.sqrt((point_1[0] - point_2[0]) ** 2 +
                (point_1[1] - point_2[1]) ** 2))
    return euc_dist

def collide_one_to_one(game_char, platform):
    """
    Check for collision of one object and list of objects.
        Returns:
        0 : side collision
        1 : top collision
    """
    side_distance = game_char.width // 2 + platform.width // 2
    game_char_top = game_char.position[1] + (game_char.height)
    game_char_bot = game_char.position[1]
    platform_top = platform.position[1]
    platform_bot = platform.position[1] - platform.height
    obj_diff = game_char.position[0] - platform.position[0]
    if (abs(obj_diff) <= side_distance and
    (game_char_top > platform_bot and game_char_bot < platform_top)):
        # print("side col")
        return 0
    elif (abs(obj_diff) <= side_distance and
        (game_char_top == platform_bot or game_char_bot ==  platform_top)):
        # print("top col")
        return 1
    else:
        # print("\n")
        return -1
