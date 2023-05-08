import pygame
import sys

import button
import entry


screen = pygame.display.set_mode([800,600])

pygame.font.init()

button_font = pygame.Font(None, 30)

but = button.Button()
but.set_position([100,100])
but.set_size([300,175])
but.event = lambda : print("yes")

but.set_text("> Clé\"k ichi <")
but.set_font(button_font)

foo = entry.Input()
foo.set_position([100, 300])
foo.set_size([200, 60])
foo.set_font(button_font)

clock = pygame.Clock()

while True:

    screen.fill([0,0,0])
    dt = clock.tick(120) / 1000

    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        but.events(event)
        foo.events(event)
    
    foo.update(dt)
    
    but.display(screen)
    foo.display(screen)
    
    pygame.display.flip()