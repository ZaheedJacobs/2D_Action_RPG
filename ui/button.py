import pygame
from settings import *

# font_folder_path = "assets/fonts"

class Button:
    def __init__(self, x, y, fg, bg, content, font, fontsize):
        self.font = pygame.font.Font(font, fontsize)
        self.content = content
        
        self.x = x
        self.y = y
        
        self.fg = fg
        self.bg = bg

        self.text = self.font.render(self.content, True, self.fg)
        
        self.width = self.get_bounds().width
        self.height = self.get_bounds().height

        self.text_rect = self.text.get_rect(center = (self.width/2, self.height/2))

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

    def get_bounds(self):
        return pygame.Rect(0, 0, self.text.get_width(), self.text.get_height())

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
    
    def draw(self, screen):
        screen.blit(self.text, self.rect)