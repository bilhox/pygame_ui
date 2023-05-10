import pygame
import component

class Section(component.Component):

    def __init__(self):
        
        self.components : list[component.Component] = []
        self._weights : list[float] = []

    def update(self, dt):
        
        for component in self.components:
            component.update(dt)

    def events(self, event : pygame.Event):
        for component in self.components:
            component.events(event)

    def display(self, dest : pygame.Surface):
        for component in self.components:
            component.display(dest)