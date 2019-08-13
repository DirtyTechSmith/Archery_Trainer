import sys, pygame

pygame.init()
draw = pygame.draw

size = width, height = 1024, 768
speed = [1, 1]
black = 0, 0, 0
space_bar = pygame.K_SPACE
print('spacebar')
print(space_bar)
screen = pygame.display.set_mode(size)
# image_path = "D:\\proceduworld\\prettyrandomoceansgif.gif"
# pygame_image = pygame.image.load(image_path)
# image_rect = pygame_image.get_rect()

# my_cool_new_rect = pygame.
has_focus = 0
last_pressed_keys = pygame.key.get_pressed()
while 1:
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
            # speed[0] = -speed[0]

    # image_rect = image_rect.move(speed)
    # if image_rect.left < 0 or image_rect.right > width:
    #     speed[0] = -speed[0]
    # if image_rect.top < 0 or image_rect.bottom > height:
    #     speed[1] = -speed[1]
    screen.fill(black)
    # screen.blit(pygame_image, image_rect)
    pygame.display.flip()
