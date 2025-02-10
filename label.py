import pygame

fonts = {}

anti_alias = True
# font_folder_path = "assets/fonts"

class Label:
    def __init__(self, x, y, font, text, size = 32, color = (255,255,255)):
        self.color = color
        self.x = x
        self.y = y
        if font in fonts:
            self.font = fonts[font]
        else:
            self.font = pygame.font.Font(font, size)
        
        self.set_text(text)

    def get_bounds(self):
        return pygame.Rect(0, 0, self.surface.get_width(), self.surface.get_height())

    def set_text(self, text):
        self.text = text
        self.surface = self.font.render(self.text, anti_alias, self.color)
        self.shadow_surface = self.font.render(self.text, anti_alias, (0, 0, 0))

    def draw(self, screen):
        screen.blit(self.shadow_surface, (self.x + 1, self.y + 1))
        screen.blit(self.surface, (self.x, self.y))