import pygame
import component

class Button(component.Component):

    def __init__(self):
        super().__init__()
        
        self.state = "NONE"
        self.event = lambda : None
        self.font = pygame.Font(None, 20)
        self.text = ""

        self.set_colors({
            "NONE":[200,200,200],
            "HOVER":[150,150,150],
            "CLICKED":[100,100,100]})
        
        
    def set_position(self, position : tuple[float, float]):
        self.rect.topleft = position
    
    def set_size(self, size : tuple[int, int]):
        self.rect.size = size
        self.set_colors(self.colors)

    def set_text(self, text : str):
        self.text = text
        self.__update_surfaces()
    
    def set_font(self, font : pygame.Font):

        self.font = font
        self.__update_surfaces()

    def __update_surfaces(self):

        self.surfaces = {}

        for state, color in self.colors.items():
            surf = pygame.Surface(self.rect.size).convert()
            surf.fill(color)

            text_surf = self.font.render(self.text, True, [0,0,0])
            surf.blit(
                text_surf,
                [
                    self.rect.w / 2 - text_surf.get_width() / 2,
                    self.rect.h / 2 - text_surf.get_height() / 2
                ]
            )

            self.surfaces[state] = surf

    def set_colors(self, color_dict : dict[list[int, int, int]]):

        self.colors = color_dict
        self.__update_surfaces()

    def update(self, dt):
        pass

    def events(self, event : pygame.Event):

        if event.type == pygame.MOUSEMOTION:
            if not self.state == "CLICKED":
                if self.rect.collidepoint(event.pos):
                    self.state = "HOVER"
                else:
                    self.state = "NONE"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.state == "HOVER":
                self.state = "CLICKED"
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                if self.state == "CLICKED":
                    self.event()
                    self.state = "HOVER"
            else:
                self.state = "NONE"
            

    def display(self, dest : pygame.Surface):

        dest.blit(self.surfaces[self.state], [self.rect.x - self.parent.rect.x, self.rect.y - self.parent.rect.y])