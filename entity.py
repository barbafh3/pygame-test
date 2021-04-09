import pygame
from engine.constants import TILE_SIZE


class Entity:
    def __init__(self, name, starting_position, rect):
        self.name = name
        self.sprite_rect = rect
        self.position = starting_position
        self.collision = pygame.Rect(self.position.x, self.position.y, TILE_SIZE, TILE_SIZE)
        self.collision_radius = TILE_SIZE * 2
        self.collisions = []

    def draw(self, surface, tileset):
        rect = pygame.Rect(self.sprite_rect)
        sprite = pygame.Surface(rect.size).convert_alpha()
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(tileset, (0, 0), rect)
        surface.blit(sprite, self.position)

    def update(self, delta):
        pass

    def collision_check(self, entity_list, delta):
        self.collisions = []
        for entity in entity_list:
            if self.position.distance_to(entity.position) <= self.collision_radius:
                if self.collision.colliderect(entity.collision):
                    self.collisions.append(entity)
