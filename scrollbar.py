import pygame
import component

"""
Does nothing for now, it's just the structure
"""

class Scrollbar(component.Component):

    def __init__(self):
        super().__init__()
        self.bar_texture = pygame.Surface(self.rect.size)
        self.texture = pygame.Surface(self.rect.size)

        self.colors["bar"] = [100, 100, 100]
        self.colors["background"] = [230, 230, 230]

        self.__update_colors()
    
    def __update_colors(self):

        self.texture.fill(self.colors["background"])
        self.bar_texture.fill(self.colors["bar"])

    def display(self, dest):

        dest.blit(self.texture, [self.rect.x - self.parent.rect.x, self.rect.y - self.parent.rect.y])
        dest.blit(self.bar_texture, [self.rect.x - self.parent.rect.x, self.rect.y - self.parent.rect.y])
