import sys, pygame

pygame.init()
draw = pygame.draw

size = [1024, 768]
speed = [1, 1]
black = 0, 0, 0
space_bar = pygame.K_SPACE
keys = {
    'space' :pygame.K_SPACE,
}
print('spacebar')
print(space_bar)
screen = pygame.display.set_mode(size)
# image_path = "D:\\proceduworld\\prettyrandomoceansgif.gif"
# pygame_image = pygame.image.load(image_path)
# image_rect = pygame_image.get_rect()

circle_color = pygame.color.Color('red')


has_focus = 0
last_pressed_keys = pygame.key.get_pressed()
while 1:
    screen.fill(black)
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
        if pressed_keys[space_bar]:
            print('spacetime')

    my_cool_new_circle = pygame.draw.circle(screen, circle_color, (100, 100), 100)
    # screen.blit(my_cool_new_circle)
    pygame.display.flip()
