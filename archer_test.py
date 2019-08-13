import sys
import pygame
from classes.archer import Archer, ArcherBrain

pygame.init()
draw = pygame.draw

size = [1024, 768]
speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size)
the_surface = pygame.display.get_surface()

bad_guy_color = pygame.color.Color('red')
archer_color = pygame.color.Color('green')

has_focus = 0
last_pressed_keys = pygame.key.get_pressed()
screen.fill(black)
radius = 50
good_guy_pos = [radius, size[1] - radius]
bad_guy_pos = [size[0] - radius, size[1] - radius]
while 1:
    new_archer = Archer(good_guy_pos, screen, size)
    focus = pygame.key.get_focused()
    if has_focus != focus:
        print(f'focused changed to: {focus}')
        has_focus = focus

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys != last_pressed_keys:
        # print('keys changed')
        last_pressed_keys = pressed_keys
        if pressed_keys[pygame.K_SPACE]:
            new_archer.shoot(bad_guy_pos)
            print('spacetime')

    archer_circle = pygame.draw.circle(screen, archer_color, good_guy_pos, radius)
    bad_guy_circle = pygame.draw.circle(screen, bad_guy_color, bad_guy_pos, radius)
    # screen.blit(my_cool_new_circle)
    pygame.display.flip()
