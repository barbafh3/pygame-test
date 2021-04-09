from engine.constants import WAREHOUSE_SPRITE, TILE_SIZE, BUILDING_SCALE_RATIO
from entity import Entity
import villagers
import pygame


class Building(Entity):
    def __init__(self, name, starting_position, rect):
        super().__init__(name, starting_position, rect)

    def draw(self, surface, tileset):
        rect = pygame.Rect(self.sprite_rect)
        sprite = pygame.Surface(rect.size).convert_alpha()
        sprite.blit(tileset, (0, 0), rect)
        scaled_surf = pygame.transform.scale(sprite, (int(TILE_SIZE * BUILDING_SCALE_RATIO), int(TILE_SIZE * BUILDING_SCALE_RATIO)))
        scaled_surf.set_colorkey((0, 0, 0))
        surface.blit(scaled_surf, self.position)


class Warehouse(Building):
    def __init__(self, name, starting_position):
        super().__init__(name, starting_position, WAREHOUSE_SPRITE)
        self.storage = {}

    def update(self, delta):
        for collider in self.collisions:
            if isinstance(collider, villagers.Hauler):
                print("Hauler collided")
            if isinstance(collider, villagers.Builder):
                print("Builder collided")


class BuildingManager:
    def __init__(self, tileset):
        self.building_list = []
        self.tileset = tileset

    def draw_buildings(self, surface):
        for building in self.building_list:
            building.draw(surface, self.tileset)

    def update_buildings(self, delta):
        for building in self.building_list:
            building.update(delta)

    def building_collision_checks(self, villager_list, delta):
        for building in self.building_list:
            building.collision_check(villager_list, delta)


class StorageManager:
    def __init__(self):
        self.global_storage = {}

    def get_total_global_usage(self) -> int:
        total = 0
        for resource in self.global_storage:
            total += self.global_storage[resource]
        return int(total)
