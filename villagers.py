from engine.constants import BUILDER_SPRITE, HAULER_SPRITE, TILE_SIZE
from pygame import Vector2
from entity import Entity
import pygame


class VillagerManager:
    def __init__(self, tileset):
        self.villager_list = []
        self.tileset = tileset

    def draw_villagers(self, surface):
        for villager in self.villager_list:
            villager.draw(surface, self.tileset)

    def update_villagers(self, delta):
        for villager in self.villager_list:
            villager.update(delta)


class Villager(Entity):
    def __init__(self, name, starting_position, speed, rect):
        super().__init__(name, starting_position, rect)
        self.speed = speed
        self.target_position = Vector2(350, 250)


class Hauler(Villager):
    def __init__(self, name, starting_position, speed):
        super().__init__(name, starting_position, speed, HAULER_SPRITE)
        self.capacity = 0

    def update(self, delta):
        if self.position.distance_to(self.target_position) > 1.0:
            direction = (self.target_position - self.position).normalize()
            self.position += direction * self.speed * delta
            self.collision = pygame.Rect(self.position.x, self.position.y, TILE_SIZE, TILE_SIZE)


class Builder(Villager):
    def __init__(self, name, starting_position, speed):
        super().__init__(name, starting_position, speed, BUILDER_SPRITE)
        self.construction_tick = 1
