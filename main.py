from engine.math import Collision, Direction, Vector2
from engine.constants import BASE_JUMP_COUNT, DIRT_COLOR, GRASS_COLOR, PLAYER_COLOR, WINDOW, ASSETS_FOLDER
import pygame
import engine.text
import engine.events
import engine.tilemap
import engine.debug
from pygame.locals import *

# --- DISCLAIMERS ---
#
# -> Fonts used were made by the youtuber DaFluffyPotato, i just added missing character on the big font
#    such as (, ), / and \.

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Tilemap test")
screen = pygame.display.set_mode(WINDOW, 0, 32)
display = pygame.Surface(WINDOW)
drawing_surf = pygame.Surface(WINDOW)
my_font = engine.text.Font(ASSETS_FOLDER + 'small_font.png')
my_big_font = engine.text.Font(ASSETS_FOLDER + 'large_font.png')

debugger = engine.debug.DataPanel(my_big_font)
debug_panel_enabled = False

player = pygame.Rect(30, 30, 20, 40)
direction = Direction(False, False, False, False)
player_collision = Collision(False, False, False, False)
jump_count = BASE_JUMP_COUNT
vertical_speed = 0

tile_types = {'1': DIRT_COLOR, '2': GRASS_COLOR}

tilemap = engine.tilemap.ShapeTilemap(ASSETS_FOLDER + "map.txt", tile_types)


def collision_test(rect, tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions


def move(rect, movement, tiles, collisions):
    rect.x += movement.x
    collision = collision_test(rect, tiles)
    for tile in collision:
        if movement.x > 0:
            rect.right = tile.left
            collisions.right = True
        if movement.x < 0:
            rect.left = tile.right
            collisions.left = True
    rect.y += movement.y
    collision = collision_test(rect, tiles)
    for tile in collision:
        if movement.y > 0:
            rect.bottom = tile.top
            movement.y = 0
            collisions.bottom = True
        if movement.y < 0:
            rect.top = tile.bottom
            collisions.top = True
        # return rect


def function_time(func) -> str:
    before = pygame.time.get_ticks()
    func()
    after = pygame.time.get_ticks()
    elapsed = after - before
    return str(elapsed)


vertical = 0
air = 0

last_time = pygame.time.get_ticks()

while True:
    drawing_surf.fill((25, 175, 200))

    delta = (pygame.time.get_ticks() - last_time) * 60 / 1000
    last_time = pygame.time.get_ticks()

    player_collision = Collision(False, False, False, False)
    movement = Vector2(0, 0)
    grounded = ""

    if direction.right is True:
        movement.x += 3 * delta
    if direction.left is True:
        movement.x -= 3 * delta
    if direction.up is True and jump_count > 0:
        if air < 6:
            vertical = -9
            jump_count -= 1

    movement.y += vertical
    if movement.y < -3:
        vertical += 0.4 * delta
    if movement.y > -3 and movement.y <= 2:
        vertical += 0.3 * delta
    if movement.y > 2:
        vertical += 0.8 * delta
    if vertical > 8:
        vertical = 8

    debug_panel_enabled = engine.events.handle_events(
        direction, debug_panel_enabled)

    move_time = function_time(lambda: move(
        player, movement, tilemap.tile_list, player_collision))

    if player_collision.bottom is True:
        jump_count = BASE_JUMP_COUNT
        vertical = 0
        air = 0
        grounded = "Grounded"
    else:
        air += 1
        grounded = "Not grounded"
    if player_collision.top is True:
        vertical = 0

    tilemap_time = function_time(
        lambda: tilemap.draw_tilemap(drawing_surf))
    pygame.draw.rect(drawing_surf, PLAYER_COLOR, player)

    if debug_panel_enabled is True:
        fps = ("fps", "FPS: " + str(int(clock.get_fps())))
        move_drawtime = (
            "move_drawtime", "Drawing time for 'move()': " + move_time + "ms")
        tilemap_drawtime = (
            "tilemap_drawimte", "Drawing time for 'draw_tilemap()': " + tilemap_time + "ms")
        current_position = ("player_position", "Current player position: x = " +
                            str(player.x) + " - y = " + format(player.y, '.2f'))
        current_velocity = ("player_velocity", "Current player velocity: x = " +
                            str(movement.x) + " - y = " + format(movement.y, '.2f'))
        debugger.add_content_to_list([fps, move_drawtime,
                                      tilemap_drawtime, current_position, current_velocity])
        debugger.draw_debug_panel(drawing_surf)

    display.blit(drawing_surf, (0, 0))
    screen.blit(display, (0, 0))
    pygame.display.update()
    clock.tick(60)
