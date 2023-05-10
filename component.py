import pygame


class Component:

    def __init__(self):
        self.rect = pygame.Rect(0,0,0,0)

    def update(self, dt):
        pass

    def events(self, event : pygame.Event):
        pass

    def display(self, dest : pygame.Surface):
        pass