import sys
import pygame
from pygame.sprite import Group

from pigboy import Pigboy
from game_platform import Platform
from settings import Settings
import game_functions as gf

def run_game():
    """Main function to run game"""
    pygame.init()
    g_sets = Settings()
    screen = pygame.display.set_mode(
        (g_sets.screen_width, g_sets.screen_height))
    pygame.display.set_caption("PB")

    level_limit = -1500
    screen_shift = 0

    #platform = Platform(screen, 300, 500, 150, 50)
    platforms = Group()

    plat_dim_list = g_sets.platform_list
    # Create 3 platforms (will move this to game functions)
    for dim in plat_dim_list:
        platform = Platform(screen, dim[0], dim[1], dim[2], dim[3])
        platforms.add(platform)


    pigboy = Pigboy(screen, g_sets, platforms)

    # Set Clock
    clock = pygame.time.Clock()
    # Start the main loop for the game.
    while True:
        # Watch for keyboard and mouse events.
        gf.check_events(g_sets, pigboy)
        gf.update_screen(g_sets, screen, pigboy, platforms)
        # gf.screen_respond(screen_shift, platforms, pigboy, g_sets)
        clock.tick(g_sets.fps)
run_game()
