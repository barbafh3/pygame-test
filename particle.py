import pygame
import random
import engine.math
from pygame.locals import *


class CircleParticle:
    def __init__(self, position, velocity, timer, color):
        self.position = position
        self.velocity = velocity
        self.timer = timer
        self.color = color


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


def draw_water_particles(screen, surface, mx, my):
    global particles

    for particle in particles:
        particle.position.x += particle.velocity.x
        particle.position.y += particle.velocity.y
        particle.velocity.y += random.randint(0, 2) / 10
        pygame.draw.circle(screen, particle.color, [int(
            particle.position.x), int(particle.position.y)], int(particle.timer))

        particle.timer -= 0.1

        radius = particle.timer * 2
        surface = circle_surf(radius, (60, 60, 60))
        screen.blit(surface, (int(particle.position.x - radius),
                              int(particle.position.y - radius)), special_flags=BLEND_RGB_ADD)

        if particle.timer <= 0:
            particles.remove(particles[0])


def draw_smoke(screen, mx, my):
    random_color = random.randint(0, 1)
    particle = CircleParticle(engine.math.Vector2(mx, my), engine.math.Vector2(
        random.uniform(-1, 1), random.uniform(0, -1)), random.uniform(2, 4), smoke_colors[random_color])
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
