import pygame
import component

class Section(component.Component):

    def __init__(self):
        
        self.components : dict[str, component.Component] = {}

    def update(self, dt):
        
        for component in self.components.values():
            component.update(dt)

    def events(self, event : pygame.Event):
        for component in self.components.values():
            component.events(event)

    def display(self, dest : pygame.Surface):
        for component in self.components.values():
            component.display(dest)