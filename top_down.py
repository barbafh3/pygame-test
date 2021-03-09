
from villagers import Builder, Hauler, VillagerManager
from pygame import Vector2
from engine.tilemap import SpriteTilemap
from engine.events import handle_events
from engine.constants import ASSETS_FOLDER, TILE_SIZE, WINDOW
import pygame
import engine.text
import engine.debug


clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Tilemap test")
screen = pygame.display.set_mode(WINDOW, 0, 32)
display = pygame.Surface(WINDOW)
drawing_surf = pygame.Surface(WINDOW)
my_font = engine.text.Font(ASSETS_FOLDER + 'small_font.png')
my_big_font = engine.text.Font(ASSETS_FOLDER + 'large_font.png')
tileset = pygame.image.load(ASSETS_FOLDER + "tileset.png").convert_alpha()
villager_manager = VillagerManager(drawing_surf, tileset)

villager_manager.villager_list.append(Hauler(Vector2(50, 50), 1))
villager_manager.villager_list.append(Builder(Vector2(100, 100), 1))

tile_types = {"0": (0, 0, TILE_SIZE, TILE_SIZE), "1": (16, 0, TILE_SIZE, TILE_SIZE), "2": (32, 0, TILE_SIZE, TILE_SIZE)}
tilemap = SpriteTilemap(ASSETS_FOLDER + "top_down_map.txt", tileset, tile_types)

debugger = engine.debug.DataPanel(my_big_font)
debug_panel_enabled = False

last_time = pygame.time.get_ticks()

while True:
    drawing_surf.fill((25, 175, 200))

    delta = (pygame.time.get_ticks() - last_time) * 60 / 1000
    last_time = pygame.time.get_ticks()

    handle_events()

    tilemap.draw_tilemap(drawing_surf)
    villager_manager.draw_villagers()
    villager_manager.update_villagers(delta)

    display.blit(drawing_surf, (0, 0))
    screen.blit(display, (0, 0))
    pygame.display.update()
    clock.tick(60)
