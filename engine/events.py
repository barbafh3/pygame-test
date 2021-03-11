import pygame
import sys

from pygame.constants import KEYDOWN, KEYUP, K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_TAB, K_UP, K_a, K_d, K_s, QUIT


def handle_events(direction, debug_panel_enabled):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_UP or event.key == K_SPACE:
                direction.up = True
            if event.key == K_DOWN or event.key == K_s:
                direction.down = True
            if event.key == K_LEFT or event.key == K_a:
                direction.left = True
            if event.key == K_RIGHT or event.key == K_d:
                direction.right = True
            if event.key == K_TAB:
                debug_panel_enabled = not debug_panel_enabled
        if event.type == KEYUP:
            if event.key == K_UP or event.key == K_SPACE:
                direction.up = False
            if event.key == K_DOWN or event.key == K_s:
                direction.down = False
            if event.key == K_LEFT or event.key == K_a:
                direction.left = False
            if event.key == K_RIGHT or event.key == K_d:
                direction.right = False
    return debug_panel_enabled


def handle_events_():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
