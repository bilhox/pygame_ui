import pygame

class Input():

    def __init__(self):

        self.rect = pygame.Rect(0,0,0,0)
        self.state = "INACTIVE"

        self.font = pygame.Font(None, 20)
        self.text = ""
        self.visible_text = ""

        self.__generate_text_surface()

        self.surfaces : dict[str, pygame.Surface] = {}
        self.set_colors({
            "INACTIVE":[200,200,200],
            "HOVER":[190,190,190],
            "ACTIVE":[170,170,170]})

        self.typing = False
        self.cursor = [0, True]

        self.key_repeating_waiting_time = 1
        self.key_repeating_frequency = 0.05
        self._key_pressed = None
    
    def __generate_text_surface(self):
        
        self.text_surf = self.font.render(self.text, True, [40,40,40])

    def set_position(self, position : tuple[float, float]):
        self.rect.topleft = position
    
    def set_size(self, size : tuple[int, int]):
        self.rect.size = size
        self.set_colors(self.colors)
    
    def set_text(self, text : str):
        self.text = text
        self.__generate_text_surface()
    
    def set_font(self, font : pygame.Font):

        self.font = font
        self.__generate_text_surface()
    
    def set_colors(self, color_dict : dict[str, list[int, int, int]]):

        self.colors = color_dict
        self.__update_surfaces()

    def update(self, dt):
        if not self.typing or self._key_pressed == None:
            return
        
        if self._key_pressed[2] <= 0:
            if self._key_pressed[3] <= 0:
                self.__handle_input(*self._key_pressed[0:2])
                self._key_pressed[3] = self.key_repeating_frequency
            else:
                self._key_pressed[3] -= dt
        else:
            self._key_pressed[2] -= dt
                
        
    
    def events(self, event : pygame.Event):

        if event.type == pygame.MOUSEMOTION:
            if not self.state == "ACTIVE":
                if self.rect.collidepoint(event.pos):
                    self.state = "HOVER"
                else:
                    self.state = "INACTIVE"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not self.typing:
                if self.state == "HOVER":
                    self.state = "ACTIVE"
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                if self.state == "ACTIVE":
                    self.typing = True
            else:
                self.typing = False
                self.state = "INACTIVE"
        
        elif event.type == pygame.KEYDOWN:
            self.__handle_input(event.key, event.unicode)
        elif event.type == pygame.KEYUP:
            self._key_pressed = None
    
    def __handle_input(self, key, unicode_value):
        if not self.typing:
            return
        
        if self._key_pressed == None:
            self._key_pressed = [key, unicode_value, self.key_repeating_waiting_time, 0]

        if key == pygame.K_BACKSPACE:
            if len(self.text) != 0 and self.cursor[0] > 0:
                self.set_text(self.text[:self.cursor[0]-1] + self.text[self.cursor[0]:])
                self.cursor[0] = max(self.cursor[0]-1, 0)
        elif key == pygame.K_LEFT:
            self.cursor[0] = max(self.cursor[0]-1, 0)
        elif key == pygame.K_RIGHT:
            self.cursor[0] = min(self.cursor[0]+1, len(self.text))
        else:
            self.set_text(self.text[:self.cursor[0]] + unicode_value + self.text[self.cursor[0]:])
            self.cursor[0] += 1

        self.__generate_text_surface()
        
    def __update_surfaces(self):

        self.surfaces = {}

        for state, color in self.colors.items():
            surf = pygame.Surface(self.rect.size).convert()
            surf.fill(color)

            self.surfaces[state] = surf

    def display(self, dest : pygame.Surface):

        final_surf = self.surfaces[self.state].copy()
        final_surf.blit(self.text_surf, [
                3,
                self.rect.h / 2 - self.text_surf.get_height() / 2
            ])
        if self.typing:
            pygame.draw.line(final_surf, [0,0,0], [
                self.font.size(self.text[0:self.cursor[0]])[0] + 3,
                self.rect.h / 2 - self.text_surf.get_height() / 2,
            ],[
                self.font.size(self.text[0:self.cursor[0]])[0] + 3,
                self.rect.h / 2 + self.text_surf.get_height() / 2
            ])
        dest.blit(final_surf, self.rect.topleft)