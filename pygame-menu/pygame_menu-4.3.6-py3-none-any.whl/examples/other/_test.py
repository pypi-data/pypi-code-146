import sys
import pygame
import pygame_menu

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
menus = pygame_menu.Menu('', 1920, 1080, False)

age = menus.add.text_input(
    'Character age:',
)

name = menus.add.text_input(
    'Character name:'
)

menus.render()
menus._widget_selected_update = False

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255, 0, 0))
    menus.update(events)
    age.draw(screen)
    if age.is_selected():
        age.update(events)
    age.set_position(500, 500)

    name.draw(screen)
    if name.is_selected():
        name.update(events)
    name.set_position(500, 800)

    pygame.display.update()
    clock.tick(60)
