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
    # obj_diff_y = game_char.position[1] - platform.position[1]
    print(str(abs(obj_diff)) + " " + str(side_distance))
    print(str(math.ceil(game_char_bot / 10)*10) + " " + str(platform_top))

    if (math.ceil(game_char_bot / 10)*10 == platform_top and
    abs(obj_diff) <= side_distance):
        return 1
    elif (abs(obj_diff) <= side_distance and
    (game_char_top > platform_bot and game_char_bot < platform_top)):
        return 0
    else:
        return -1

def point_collide(gamechr, plat):
    """Collision based on point system."""
    gpts = object_points(gamechr)
    ppts = object_points(plat)

    print(gpts, end="")
    print(" pig")
    print(ppts, end="")
    print(" plat")

    x_overlap = not (gpts[0][0] > ppts[1][0] or
                     gpts[1][0] < ppts[0][0])

    y_overlap = not (gpts[0][1] < ppts[1][1] or
                     gpts[1][1] > ppts[0][1])

    return x_overlap and y_overlap


def object_points(game_obj):
    """
    Get the points of a game objects position.
       Return a list of tuples where the following
       points are defined.
       point_list -> [(top_left), (bot_right)]
    """
    x, y = game_obj.position
    xrad = game_obj.width // 2
    yrad = game_obj.height // 2

    # Get points of rectangle
    # All points of a rectangle can be derived
    # from these two points
    top_left = (x - xrad), (y + yrad)
    bot_right = (x + xrad), (y - yrad)

    return [top_left, bot_right]
