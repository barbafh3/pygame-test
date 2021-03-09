import pygame
from pygame.constants import BLEND_RGB_SUB


class DataPanel:
    def __init__(self, font):
        self.content_list = {}
        self.font = font
        self.panel_length = 330

    def add_content_to_list(self, args):
        for (key, value) in args:
            self.content_list[key] = value

    def draw_debug_panel(self, drawing_surf):
        new_surf = pygame.Surface((self.panel_length, (len(self.content_list) * 20) + 15))
        coords = pygame.Vector2(20, 20)
        pygame.draw.rect(new_surf, (50, 50, 50, 128), (0, 0, self.panel_length, 135))
        drawing_surf.blit(new_surf, (10, 10), special_flags=BLEND_RGB_SUB)
        for key in self.content_list:
            self.font.render(drawing_surf, self.content_list[key], coords)
            coords.y += 20
