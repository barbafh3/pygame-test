from engine.constants import BUILDER_SPRITE, HAULER_SPRITE
from pygame import Vector2
import pygame


class Villager:
    def __init__(self, starting_position, speed, rect):
        self.sprite_rect = rect
        self.position = starting_position
        self.speed = speed
        self.target_position = Vector2(800, 534)

    def draw(self, surface, tileset):
        rect = pygame.Rect(self.sprite_rect)
        sprite = pygame.Surface(rect.size).convert_alpha()
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(tileset, (0, 0), rect)
        surface.blit(sprite, self.position)


class Hauler(Villager):
    def __init__(self, starting_position, speed):
        super().__init__(starting_position, speed, HAULER_SPRITE)
        self.capacity = 0

    def update(self, delta):
        if self.position.distance_to(self.target_position) > 1.0:
            direction = (self.target_position - self.position).normalize()
            self.position += direction * self.speed * delta


class Builder(Villager):
    def __init__(self, starting_position, speed):
        super().__init__(starting_position, speed, BUILDER_SPRITE)
        self.construction_tick = 1

    def update(self, delta):
        pass


class VillagerManager:
    def __init__(self, surface, tileset):
        self.villager_list = []
        self.surface = surface
        self.tileset = tileset

    def draw_villagers(self):
        for villager in self.villager_list:
            villager.draw(self.surface, self.tileset)

    def update_villagers(self, delta):
        for villager in self.villager_list:
            villager.update(delta)
