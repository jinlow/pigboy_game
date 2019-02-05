import sys

import pygame

def key_down(g_sets, pigboy, event):
    """Respond to keydown events."""
    if event.key == pygame.K_RIGHT:
        pigboy.moving_right = True
        pigboy.facing_right = True
    elif event.key == pygame.K_LEFT:
        pigboy.moving_left = True
        pigboy.facing_right = False
    elif (not(pigboy.jumping_up) and
    event.key == pygame.K_SPACE and pigboy.moving_y == 0):
        pigboy.jumping_up = True
    # Check for running
    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
        pigboy.running = True

def key_up(g_sets, pigboy, event):
    """Respond to keyup events"""
    if event.key == pygame.K_RIGHT:
        pigboy.moving_right = False
    if event.key == pygame.K_LEFT:
        pigboy.moving_left = False
    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
        pigboy.running = False

def check_events(g_sets, pigboy):
    """Respond to kepresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            key_down(g_sets, pigboy, event)

        elif event.type == pygame.KEYUP:
            key_up(g_sets, pigboy, event)

def update_screen(g_sets, screen, pigboy, platforms):
    """Update images on the screen and flip to the new screen."""

    # Update Pigboy
    pigboy.update()

    # Redraw the screen during each pass through the loop.
    screen.fill(g_sets.bg_color)
    pigboy.blitme()
    platforms.draw(screen)

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def update_collisions(pigboy, platform):
    """ Check for collisions, and reset Pigboy movement
        when something is hit. """
    collisions = pygame.sprite.groupcollide(pigboy, platform, True, True)

    if collisions:
        pigboy.moving_y = False

def shift_screen(screen_shift, diff, platforms):
    """ Shift the screen when the pig moves off screen. """

    screen_shift += diff

    for platform in platforms:
        platform.rect.x += diff

def screen_respond(screen_shift, platforms, pigboy, g_sets):
    """ Make screen respond to pigbpy. """

    right_cut = g_sets.screen_width - 60
    left_cut = 60

    # Getting close to right of screen
    if pigboy.rect.right >= right_cut:
        diff = pigboy.rect.right - right_cut
        pigboy.rect.right = right_cut
        shift_screen(screen_shift, -diff, platforms)

    # Getting close to left of screen
    if pigboy.rect.left <= left_cut:
        diff = left_cut - pigboy.rect.left
        pigboy.rect.left = left_cut
        shift_screen(screen_shift, diff, platforms)

    # current_position = pigboy.rect.x + world_shift
    # if pigboy.rect.right <= left_cut:
    #     diff = right_cut - pigboy.rect.right
    #     pigboy.rect.right = right_cut
    #     shift_screen(shift_x, platforms)
