import sys
import pygame
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

    pigboy = Pigboy(screen, g_sets)
    platform = Platform(screen, g_sets)
    # Set Clock
    clock = pygame.time.Clock()
    # Start the main loop for the game.
    while True:
        # Watch for keyboard and mouse events.
        gf.check_events(g_sets, pigboy)
        gf.update_screen(g_sets, screen, pigboy, platform)
        clock.tick(g_sets.fps)
run_game()
