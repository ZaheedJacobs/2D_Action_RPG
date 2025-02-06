import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, pos, layer = "background", surf = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self._layer = layer