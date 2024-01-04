"""
bow physics:
https://arxiv.org/ftp/arxiv/papers/1511/1511.02250.pdf

3d physics engine https://pybullet.org/
"""

import random
import sys
import time
from typing import List

import pygame
from pygame import Surface

from classes.archer import MAX_BOW_STR
from classes.archer_population import ArcherPopulation
from classes.entity import Entity
from vector import Vector

pygame.init()
draw = pygame.draw

SCREEN_SIZE: List[int] = [1024, 768]
SPEED: List[int] = [1, 1]
BLACK_COLOR = 0, 0, 0

screen: Surface = pygame.display.set_mode(SCREEN_SIZE)

the_surface: Surface = pygame.display.get_surface()

BAD_GUY_COLOR = pygame.color.Color('red')
ARCHER_COLOR = pygame.color.Color('green')

has_focus: int = 0
last_pressed_keys = pygame.key.get_pressed()
screen.fill(BLACK_COLOR)
radius: int = 25
good_guy_pos: List[int] = [radius, SCREEN_SIZE[1] - radius]
bad_guy_pos: List[int] = [SCREEN_SIZE[0] - radius, SCREEN_SIZE[1] - radius]

my_bow: float = MAX_BOW_STR
do_it: bool = True
bad_guy: Entity = Entity(Vector(bad_guy_pos), screen)
archer_pos: Vector = Vector(good_guy_pos)
archer_population: ArcherPopulation = ArcherPopulation(screen, archer_pos, num_archers=25, target=bad_guy)

while do_it:
    screen.fill(BLACK_COLOR)
    bad_guy.position.x = random.randrange(int(screen.get_width() * .75), screen.get_width())

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    archer_circle = pygame.draw.circle(screen, ARCHER_COLOR, (archer_pos.x, archer_pos.y), radius)
    bad_guy_circle = pygame.draw.circle(screen, BAD_GUY_COLOR, bad_guy.position_tuple, radius)
    archer_population.volley()
    archer_population.breed_population()

    time.sleep(.25)
    pygame.display.flip()

pygame.quit()