import pygame
import sys
from pygame.locals import *

# Pygame
WINDOW = (1200, 800)
DISPLAY = (600, 400)
FPS = 60

# Tilemap
TILE_SIZE = 16
MAP_WIDTH = 80
MAP_HEIGHT = 50
GRAVITY = 0.2

# Colors
GRASS_COLOR = (25, 175, 45)
DIRT_COLOR = (120, 70, 30)
PLAYER_COLOR = (255, 0, 0, 128)

JUMP_SPEED = 20
BASE_JUMP_COUNT = 1


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Collision:
    def __init__(self, left, right, top, bottom):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right


class Direction:
    def __init__(self, left, right, up, down):
        self.left = left
        self.right = right
        self.up = up
        self.down = down


def clip(surf, x, y, x_size, y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()


class Font():
    def __init__(self, path):
        self.spacing = 1
        self.character_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                                'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                                'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-',
                                ',', ':', '+', '\'', '!', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')',
                                '/', '_', '=', '\\', '[', ']', '*', '"', '<', '>', ';']
        font_img = pygame.image.load(path).convert()
        surf = pygame.Surface(font_img.get_size())
        surf.fill((255, 255, 255))
        font_img.set_colorkey((255, 0, 0))
        surf.blit(font_img, (0, 0))
        font_img = surf
        font_img.set_colorkey((0, 0, 0))
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['A'].get_width()

    def render(self, surf, text, loc):
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing


def load_tilemap(path):
    m = []
    map_file = open(path, "r")
    map_lines = map_file.read().splitlines()
    for line in map_lines:
        m.append(list(line))
    return m


clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Tilemap test")
screen = pygame.display.set_mode(WINDOW, 0, 32)
display = pygame.Surface(WINDOW)
drawing_surf = pygame.Surface(WINDOW)
my_font = Font('small_font.png')
my_big_font = Font('large_font.png')

player = pygame.Rect(30, 30, 20, 40)
direction = Direction(False, False, False, False)
player_collision = Collision(False, False, False, False)
jump_count = BASE_JUMP_COUNT
vertical_speed = 0

tilemap = load_tilemap("map.txt")
tile_list = []


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


def draw_tilemap(surface):
    global tilemap
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if tilemap[y][x] == "1":
                pygame.draw.rect(surface, DIRT_COLOR, (TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE))
            if tilemap[y][x] == "2":
                pygame.draw.rect(surface, GRASS_COLOR, (TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE))


def handle_events():
    global direction
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_UP or event.key == K_w:
                direction.up = True
            if event.key == K_DOWN or event.key == K_s:
                direction.down = True
            if event.key == K_LEFT or event.key == K_a:
                direction.left = True
            if event.key == K_RIGHT or event.key == K_d:
                direction.right = True
        if event.type == KEYUP:
            if event.key == K_UP or event.key == K_w:
                direction.up = False
            if event.key == K_DOWN or event.key == K_s:
                direction.down = False
            if event.key == K_LEFT or event.key == K_a:
                direction.left = False
            if event.key == K_RIGHT or event.key == K_d:
                direction.right = False


for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        if tilemap[y][x] == "1" or tilemap[y][x] == "2":
            tile = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            tile_list.append(tile)


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

    handle_events()

    move_time = function_time(lambda: move(player, movement, tile_list, player_collision))
    tilemap_time = function_time(lambda: draw_tilemap(drawing_surf))

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

    pygame.draw.rect(drawing_surf, PLAYER_COLOR, player)

    new_surf = pygame.Surface((300, 135))
    pygame.draw.rect(new_surf, (50, 50, 50, 128), (0, 0, 300, 135))
    drawing_surf.blit(new_surf, (10, 10), special_flags=BLEND_RGBA_SUB)

    my_big_font.render(drawing_surf, "FPS: " + str(int(clock.get_fps())), (20, 20))
    my_big_font.render(drawing_surf, "Drawing time for 'move()': " + move_time + "ms", (20, 40))
    my_big_font.render(drawing_surf, "Drawing time for 'draw_tilemap()': " + tilemap_time + "ms", (20, 60))
    collision_str = "Collisions: Top = " + str(player_collision.top) + " - Bottom = " + str(player_collision.bottom)
    my_big_font.render(drawing_surf, collision_str, (20, 80))
    my_big_font.render(drawing_surf, "Current velocity: x = " + str(movement.x) + " - y = " + format(movement.y, '.2f'), (20, 100))
    my_big_font.render(drawing_surf, "Current position: x = " + str(player.x) + " - y = " + format(player.y, '.2f'), (20, 120))

    display.blit(drawing_surf, (0, 0))
    # screen.blit(pygame.transform.scale(display, WINDOW), (0, 0))
    screen.blit(display, (0, 0))
    pygame.display.update()
    clock.tick(60)
