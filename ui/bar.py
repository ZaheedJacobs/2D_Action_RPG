import pygame
from settings import *

class Bar:
    def __init__(self, pos_x, pos_y, amount, max, transition, change_speed, back_color, front_color, width = 300, height = 20):
        self.amount = amount
        self.max = max
        self.transition = transition
        self.back_color = back_color
        self.front_color = front_color
        self.width = width
        self.height = height
        self.ratio = self.max / self.width
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.change_speed = change_speed

    def draw(self, screen):
        # Figure out the amount to draw
        transition_width = 0
        transition_color = self.front_color
        
        if self.amount < self.transition:
            self.amount += self.change_speed
            transition_width = int((self.transition - self.amount)/self.ratio)
            transition_color = COLOURS["green"]
        
        if self.amount > self.transition:
            self.amount -= self.change_speed
            transition_width = int((self.transition - self.amount)/self.ratio)
            transition_color = COLOURS["yellow"]
        # filled = self.amount / self.ratio
        if (self.transition/self.ratio) + transition_width >= self.width:
            transition_width = self.width - (self.transition/self.ratio)
        normal_bar_rect = pygame.Rect(self.pos_x, self.pos_y, self.transition/self.ratio, self.height)
        transition_bar_rect = pygame.Rect(normal_bar_rect.right, self.pos_y, transition_width, self.height)
        
        # Draw background first
        pygame.draw.rect(screen,
                        self.back_color,
                        pygame.Rect(self.pos_x,
                                    self.pos_y,
                                    self.width,
                                    self.height))
        
        
        # Then the foreground
        pygame.draw.rect(screen,
                        self.front_color,
                        normal_bar_rect)
        
        pygame.draw.rect(screen,
                         transition_color,
                         transition_bar_rect)
        
        # Create a white border around the bar
        pygame.draw.rect(screen, 
                         (255, 255, 255), 
                         pygame.Rect(self.pos_x, 
                                     self.pos_y, 
                                     self.width, 
                                     self.height),
                                     1)
        
        
        
    def update(self):
        pass