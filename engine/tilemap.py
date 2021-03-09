from engine.constants import MAP_HEIGHT, MAP_WIDTH, TILE_SIZE
import pygame


class ShapeTilemap:
    def __init__(self, path, tile_types):
        self.tile_types = tile_types
        self.map = []
        self.tile_list = []
        map_file = open(path, "r")
        map_lines = map_file.read().splitlines()
        for line in map_lines:
            self.map.append(list(line))
        self.create_map_collisions()

    def draw_tilemap(self, surface):
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                for tile_type in self.tile_types:
                    if self.map[y][x] == tile_type:
                        rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(surface, self.tile_types[tile_type], rect)

    def create_map_collisions(self):
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if self.map[y][x] == "1" or self.map[y][x] == "2":
                    tile = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    self.tile_list.append(tile)


class SpriteTilemap:
    def __init__(self, map_path, tileset, tile_types):
        self.tile_types = tile_types
        self.map = []
        self.tileset = tileset
        map_file = open(map_path, "r")
        map_lines = map_file.read().splitlines()
        for line in map_lines:
            self.map.append(list(line))

    def get_sprite_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        sprite = pygame.Surface(rect.size).convert()
        sprite.blit(self.tileset, (0, 0), rect)
        return sprite

    def draw_tilemap(self, drawing_surf):
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                for tile_type in self.tile_types:
                    if self.map[y][x] == tile_type:
                        tile = self.get_sprite_at(pygame.Rect(self.tile_types[tile_type]))
                        drawing_surf.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))
