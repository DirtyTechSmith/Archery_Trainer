"""
bow physics:
https://arxiv.org/ftp/arxiv/papers/1511/1511.02250.pdf

3d physics engine https://pybullet.org/
"""

import random
import sys
import time

import pygame
from pygame import Surface

from classes.archer import MAX_BOW_STR
from classes.archer_population import ArcherPopulation
from classes.entity import Entity
from vector import Vector

pygame.init()
draw = pygame.draw

SCREEN_SIZE = [1024, 768]
SPEED = [1, 1]
BLACK_COLOR = 0, 0, 0

screen = pygame.display.set_mode(SCREEN_SIZE)  # type: Surface

the_surface = pygame.display.get_surface()

BAD_GUY_COLOR = pygame.color.Color('red')
ARCHER_COLOR = pygame.color.Color('green')

has_focus = 0
last_pressed_keys = pygame.key.get_pressed()
screen.fill(BLACK_COLOR)
radius = 25
good_guy_pos = [radius, SCREEN_SIZE[1] - radius]
bad_guy_pos = [SCREEN_SIZE[0] - radius, SCREEN_SIZE[1] - radius]

my_bow = MAX_BOW_STR
do_it = True
bad_guy = Entity(Vector(bad_guy_pos), screen)
archer_pos = Vector(good_guy_pos)
archer_population = ArcherPopulation(screen, archer_pos, num_archers=25, target=bad_guy)

while do_it:
    screen.fill(BLACK_COLOR)
    # print(type(screen))
    # print(dir(screen))
    bad_guy.position.x = random.randrange(int(screen.get_width() * .75), screen.get_width())
    # bad_guy.position.y = random.randrange(int(screen.get_height() * .75), screen.get_height())
    # archer_pos.x = random.randrange(0, int(screen.get_width() * .25))
    # archer_pos.y = random.randrange(int(screen.get_height() * .75), screen.get_height())
    # my_bow = random.uniform(MAX_BOW_STR * .5, MAX_BOW_STR * 1.5)

    # new_archer = Archer(good_guy_pos, screen, size, bad_guy, bow_str=my_bow)

    focus = pygame.key.get_focused()
    if has_focus != focus:
        print(f'focused changed to: {focus}')
        has_focus = focus

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    archer_circle = pygame.draw.circle(screen, ARCHER_COLOR, (archer_pos.x, archer_pos.y), radius)
    bad_guy_circle = pygame.draw.circle(screen, BAD_GUY_COLOR, bad_guy.position_tuple, radius)
    archer_population.volley()
    archer_population.breed_population()
    # new_archer.shoot(bad_guy)

    # screen.blit(my_cool_new_circle)
    time.sleep(.25)
    pygame.display.flip()

    # do_it = False

pygame.quit()
