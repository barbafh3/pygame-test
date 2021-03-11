from pygame import Vector2
import pygame
from villagers import Builder, Hauler, VillagerManager
from buildings import Warehouse, BuildingManager
from engine.tilemap import SpriteTilemap
from engine.events import handle_events_
from engine.constants import ASSETS_FOLDER, TILE_SIZE, WINDOW, DISPLAY, IDLE_POINT_SPRITE
import entity
import engine.text
import engine.debug


clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Tilemap test")
screen = pygame.display.set_mode(WINDOW, 0, 32)
display = pygame.Surface(DISPLAY)
drawing_surf = pygame.Surface(DISPLAY)

my_font = engine.text.Font(ASSETS_FOLDER + 'small_font.png')
my_big_font = engine.text.Font(ASSETS_FOLDER + 'large_font.png')
tileset = pygame.image.load(ASSETS_FOLDER + "tileset.png").convert_alpha()

villager_manager = VillagerManager(tileset)
villager_manager.villager_list.append(Hauler("Hauler1", Vector2(50, 50), 1))
villager_manager.villager_list.append(Builder("Builder1", Vector2(100, 100), 1))

building_manager = BuildingManager(tileset)
building_manager.building_list.append(Warehouse("Warehouse1", Vector2(350, 250)))

idle_point = entity.Entity("IdlePoint", Vector2(300, 200), IDLE_POINT_SPRITE)

tile_types = {"0": (0, 0, TILE_SIZE, TILE_SIZE), "1": (16, 0, TILE_SIZE, TILE_SIZE), "2": (32, 0, TILE_SIZE, TILE_SIZE)}
tilemap = SpriteTilemap(ASSETS_FOLDER + "top_down_map.txt", tileset, tile_types)
map_surf = pygame.Surface(DISPLAY)
tilemap.draw_tilemap(map_surf)

debugger = engine.debug.DataPanel(my_big_font)
debug_panel_enabled = False

last_time = pygame.time.get_ticks()

while True:
    drawing_surf.fill((25, 175, 200))
    drawing_surf.blit(map_surf, (0, 0))

    delta = (pygame.time.get_ticks() - last_time) * 60 / 1000
    last_time = pygame.time.get_ticks()

    handle_events_()

    building_manager.building_collision_checks(villager_manager.villager_list, delta)

    villager_manager.update_villagers(delta)
    building_manager.update_buildings(delta)

    idle_point.draw(drawing_surf, tileset)
    building_manager.draw_buildings(drawing_surf)
    villager_manager.draw_villagers(drawing_surf)

    my_font.render(drawing_surf, "FPS: " + str(int(clock.get_fps())), (20, 20))

    display.blit(drawing_surf, (0, 0))
    screen.blit(pygame.transform.scale(display, WINDOW), (0, 0))
    pygame.display.update()
    clock.tick(60)
