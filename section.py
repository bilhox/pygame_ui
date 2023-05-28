import pygame
import component

class Section(component.Component):

    def __init__(self):
        super().__init__()
        self.components : list[component.Component] = []
        self.texture : pygame.Surface = pygame.Surface(self.rect.size)
        self._weights : list[float] = []

        self.colors["background"] = [50,50,50]
    
    def add_component(self, component : component.Component, weight : float = -1):

        component.parent = self
        self.components.append(component)
        if weight == -1:
            remaining = 1 - sum(self._weights)
            if(remaining <= 1):
                self._weights.append(remaining)
            else:
                self._weights.append(self._weights[-1])
        else:
            self._weights.append(weight)
        
        self.__update_weights()
    
    def set_size(self, size):
        
        self.rect.size = size
        self.texture = pygame.Surface(self.rect.size)

    def __update_weights(self):

        parent_position = self.get_parent_position()
        pos = list([self.rect.x + parent_position[0] , self.rect.y + parent_position[1]])
        i = 0
        for w in self._weights:
            self.components[i].set_position(pos.copy())
            self.components[i].set_size([self.rect.w, w*self.rect.h])
            i += 1
            pos[1] += w*self.rect.h


    def update(self, dt):
        
        for component in self.components:
            component.update(dt)

    def events(self, event : pygame.Event):
        for component in self.components:
            component.events(event)

    def display(self, dest : pygame.Surface):
        self.texture.fill(self.colors["background"])
        for component in self.components:
            component.display(self.texture)
        
        dest.blit(self.texture, self.rect.topleft)