import pygame

class Component:

    def __init__(self):
        self.parent : Component = None
        self.rect = pygame.Rect(0,0,0,0)
        self.colors : dict[str, list[int, int, int]] = {}
    
    def get_parent_position(self):
        
        if self.parent:
            return self.parent.rect.topleft
        else:
            return [0, 0]
    
    def set_position(self, position):
        self.rect.topleft = position
    
    def set_size(self, size):
        self.rect.size = size

    def update(self, dt):
        pass

    def events(self, event : pygame.Event):
        pass

    def display(self, dest : pygame.Surface):
        pass