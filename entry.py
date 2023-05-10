import pygame
import pyperclip
import utils
import component

class Input(component.Component):

    def __init__(self):
        super().__init__()

        self.state = "INACTIVE"

        self.font = pygame.Font(None, 20)
        self.text = ""
        self.visible_range = [0,0]

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

        self._offset_x = 0
    
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
                
                last_width = self.font.size(self.text[:max(0,self.visible_range[0]-1)])[0] + 3 - self._offset_x
                pos_found = False
                for i in range(self.visible_range[0],self.visible_range[1]+2):

                    l_pos = self.font.size(self.text[:i])[0] + 3 - self._offset_x
                    if self.rect.x + l_pos > event.pos[0]:
                        pos_found = True
                        if not last_width-l_pos:
                            self.cursor[0] = 0
                            break
                        nearest = utils.nearest(last_width, l_pos, event.pos[0]-self.rect.x)
                        if nearest < event.pos[0]-self.rect.x:
                            self.cursor[0] = max(i-1,0)
                        else:
                            self.cursor[0] = i
                        break
                    last_width = l_pos
                
                
                if not pos_found:
                    self.cursor[0] = self.visible_range[1]+1

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
        elif unicode_value.lower() in "abcdefghijklmnopqrstuvwxyz<>?./§,;:!^¨£$%ùµ*1234567890°+=)àç_è-('\"é&)~#{}[]|`\\@":
            self.set_text(self.text[:self.cursor[0]] + unicode_value + self.text[self.cursor[0]:])
            self.cursor[0] += 1
        
        text_width = self.font.size(self.text[:self.cursor[0]])[0]
        if text_width - self._offset_x + 3 > self.rect.width:
            self._offset_x = text_width + 3 - self.rect.w
        elif text_width - self._offset_x + 3 < 0:
            self._offset_x = max(self._offset_x - self.rect.w, 0)

        self.__generate_text_surface()
        self.__update_visibility_range()
    
    def __update_visibility_range(self):

        for i in range(len(self.text)-1,-1,-1):
            text_width = self.font.size(self.text[:i])[0]
            if(text_width + 3 - self._offset_x < self.rect.w):
                self.visible_range[1] = i
                break
        
        for i in range(0,len(self.text)):
            text_width = self.font.size(self.text[:i])[0]
            if(text_width + 3 - self._offset_x > 0):
                self.visible_range[0] = max(i-1,0)
                break
        
    def __update_surfaces(self):

        self.surfaces = {}

        for state, color in self.colors.items():
            surf = pygame.Surface(self.rect.size).convert()
            surf.fill(color)

            self.surfaces[state] = surf

    def display(self, dest : pygame.Surface):

        final_surf = self.surfaces[self.state].copy()
        final_surf.blit(self.text_surf, [
                3 - self._offset_x,
                self.rect.h / 2 - self.text_surf.get_height() / 2
            ])
        if self.typing:
            pygame.draw.line(final_surf, [0,0,0], [
                self.font.size(self.text[0:self.cursor[0]])[0] - self._offset_x + 3,
                self.rect.h / 2 - self.text_surf.get_height() / 2,
            ],[
                self.font.size(self.text[0:self.cursor[0]])[0] - self._offset_x + 3,
                self.rect.h / 2 + self.text_surf.get_height() / 2
            ])
        dest.blit(final_surf, self.rect.topleft)