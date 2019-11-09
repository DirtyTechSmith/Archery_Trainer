"""
bow physics:
https://arxiv.org/ftp/arxiv/papers/1511/1511.02250.pdf

3d physics engine https://pybullet.org/
"""

import sys
import pygame
from pygame import Surface
from classes.archer import Archer, ArcherBrain, MAX_BOW_STR
from classes.archer_population import ArcherPopulation
from classes.entity import Entity
from vector import Vector
# import random
# import numpy
# from profile_utils import cprofileContext

pygame.init()
draw = pygame.draw

size = [1024, 768]
speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size)  # type: Surface

the_surface = pygame.display.get_surface()

bad_guy_color = pygame.color.Color('red')
archer_color = pygame.color.Color('green')

has_focus = 0
last_pressed_keys = pygame.key.get_pressed()
screen.fill(black)
radius = 25
good_guy_pos = [radius, size[1] - radius]
bad_guy_pos = [size[0] - radius, size[1] - radius]

my_bow = MAX_BOW_STR
do_it = True
bad_guy = Entity(Vector(bad_guy_pos), screen)
archer_pos = Vector(good_guy_pos)
archer_population = ArcherPopulation(screen, archer_pos, num_archers=5, target=bad_guy)

while do_it:
    # print(type(screen))
    # print(dir(screen))

    # my_bow = random.uniform(MAX_BOW_STR * .5, MAX_BOW_STR * 1.5)

    # new_archer = Archer(good_guy_pos, screen, size, bad_guy, bow_str=my_bow)

    focus = pygame.key.get_focused()
    if has_focus != focus:
        print(f'focused changed to: {focus}')
        has_focus = focus

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    archer_circle = pygame.draw.circle(screen, archer_color, good_guy_pos, radius)
    bad_guy_circle = pygame.draw.circle(screen, bad_guy_color, bad_guy.position_tuple, radius)
    archer_population.volley()
    archer_population.breedPopulation()
    # new_archer.shoot(bad_guy)
    # screen.blit(my_cool_new_circle)
    pygame.display.flip()

    # do_it = False

# pressed_keys = pygame.key.get_pressed()
#     if pressed_keys != last_pressed_keys:
#         # print('keys changed')
#         last_pressed_keys = pressed_keys
#         if pressed_keys[pygame.K_SPACE]:
#             new_archer.shoot(bad_guy)
#             print('spacetime')
