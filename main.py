import pygame
import sys

import button
import entry
import section


screen = pygame.display.set_mode([800,600])

pygame.font.init()

button_font = pygame.Font(None, 30)

but = button.Button()
but.event = lambda : print("yes")

but.set_text("> Clé\"k ichi <")
but.set_font(button_font)

foo = entry.Input()
foo.set_font(button_font)

sec = section.Section()
sec.set_size([400,400])
sec.set_position([100,100])
sec.add_component(but, 0.5)
sec.add_component(foo, 0.5)

clock = pygame.Clock()

while True:

    screen.fill([0,0,0])
    dt = clock.tick(120) / 1000

    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        sec.events(event)
    
    sec.update(dt)

    sec.display(screen)
    pygame.display.flip()