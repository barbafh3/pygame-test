import pygame
import sys
import random
from pygame.locals import *
import colors


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class CircleParticle:
    def __init__(self, position, velocity, timer, color):
        self.position = position
        self.velocity = velocity
        self.timer = timer
        self.color = color


class Direction:
    def __init__(self, left, right, up, down):
        self.left = left
        self.right = right
        self.up = up
        self.down = down


direction = Direction(False, False, False, False)
clicked = False

mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Example")

WINDOW = (500, 500)

screen = pygame.display.set_mode(WINDOW, 0, 32)

# [loc, velocity, timer, type]
particles = []

water_colors = [
    # (245, 255, 255),
    # pygame.Color(200, 255, 255, 128),
    pygame.Color(135, 255, 255, 200),
    pygame.Color(0, 210, 255, 255),
    pygame.Color(0, 125, 168, 255)
]

smoke_colors = [
    # (140, 140, 140),
    pygame.Color(180, 180, 180, 255),
    pygame.Color(240, 240, 240, 128),
]


def circle_surf(radius, color):
    surface = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surface, color, (radius, radius), radius)
    surface.set_colorkey((0, 0, 0))
    return surface


def draw_water_particles(surface, mx, my):
    global particles

    for particle in particles:
        particle.position.x += particle.velocity.x
        particle.position.y += particle.velocity.y
        particle.velocity.y += random.randint(0, 2) / 10
        pygame.draw.circle(screen, particle.color, [int(
            particle.position.x), int(particle.position.y)], int(particle.timer))

        # radius = particle.timer * 2
        # surface = circle_surf(radius, (60, 60, 60))
        # screen.blit(surface, (int(particle.position.x - radius), int(particle.position.y - radius)), special_flags=BLEND_RGB_ADD)

        if particle.timer <= 0:
            particles.remove(particles[0])


def draw_smoke(mx, my):
    random_color = random.randint(0, 1)
    particle = CircleParticle(Vector2(mx, my), Vector2(
        random.uniform(-1, 1), random.uniform(0, -1)), random.uniform(4, 6), smoke_colors[random_color])
    particles.append(particle)

    for particle in particles:
        particle.position.x += particle.velocity.x
        particle.position.y += particle.velocity.y
        particle.timer -= 0.1
        if particle.timer == 0:
            particle.timer = -1
        particle.radius += 0.1
        if particle.color.a - 60 <= 0:
            particle.color.a = 0
        else:
            particle.color.a -= 1

        pygame.draw.circle(screen, particle.color, [int(particle.position.x), int(
            particle.position.y)], int(particle.radius), int(particle.timer))

        if particle.timer <= 0:
            particles.remove(particle)


player = pygame.Rect(100, 100, 50, 80)
tiles = [(pygame.Rect(200, 350, 50, 50), (0, 255, 0)),
         (pygame.Rect(260, 320, 50, 50), (255, 0, 0))]


def collision_test(rect, tiles):
    collisions = []
    for tile, color in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions


def move(rect, movement, tiles):  # movement = [5,2]
    rect.x += movement.x
    collisions = collision_test(rect, tiles)
    for tile in collisions:
        if movement.x > 0:
            rect.right = tile.left
        if movement.x < 0:
            rect.left = tile.right
    rect.y += movement.y
    collisions = collision_test(rect, tiles)
    for tile in collisions:
        if movement.y > 0:
            rect.bottom = tile.top
        if movement.y < 0:
            rect.top = tile.bottom
    return rect


def event_handler():
    global direction
    global screen
    global particles
    global water_colors
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mx, my = pygame.mouse.get_pos()
            for i in range(15):
                particles.append(CircleParticle(Vector2(mx, my), Vector2(random.randint(
                    0, 20) / 10 - 1, -2), random.uniform(4, 6), water_colors[random.randint(0, 2)]))
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


while True:
    screen.fill((0, 0, 0))
    mx, my = pygame.mouse.get_pos()

    movement = Vector2(0, 0)

    if direction.right == True:
        movement.x += 5
    if direction.left == True:
        movement.x -= 5
    if direction.up == True:
        movement.y -= 5
    if direction.down == True:
        movement.y += 5

    player = move(player, movement, tiles)

    pygame.draw.rect(screen, colors.white, player)

    for tile, color in tiles:
        pygame.draw.rect(screen, color, tile)

    draw_water_particles(screen, mx, my)

    event_handler()

    pygame.display.update()
    mainClock.tick(60)
