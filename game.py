import pygame, sys, os
from settings import *
from state import *

class Game:
    def __init__(self):
        
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN|pygame.SCALED)
        self.font = pygame.font.Font(FONT)
        self.running = True
        self.FPS = 60

        self.states = []
        self.menu_screen = MainMenu(self)
        self.states.append(self.menu_screen)
    
    def render_text(self, text, colour, font, pos, centralised = True):
        surf = font.render(str(text), False, colour)
        rect = surf.get_rect(center = pos) if centralised else surf.get_rect(topleft = pos)
        self.screen.blit(surf, rect)

    def custom_cursor(self, screen):
        pygame.mouse.set_visible(False)
        cursor_img = pygame.image.load("assets/cursor-pointer-30.cur").convert_alpha()
        cursor_rect = cursor_img.get_rect(center = pygame.mouse.get_pos())
        cursor_img.set_alpha(150)
        screen.blit(cursor_img, cursor_rect.center)

    def get_images(self, path):
        images = []
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            img = pygame.image.load(full_path).convert_alpha()
            images.append(img)
        return images

    def get_animations(self, path):
        animations = {}
        for file_name in os.listdir(path):
            animations.update({file_name:[]})
        return animations

    def get_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    INPUTS["escape"] = True
                    # self.running = False
                
                elif event.key == pygame.K_SPACE:
                    INPUTS["space"] = True

                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    INPUTS["left"] = True

                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    INPUTS["right"] = True

                elif event.key in (pygame.K_UP, pygame.K_w):
                    INPUTS["up"] = True

                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    INPUTS["down"] = True

                elif event.key == pygame.K_q:
                    INPUTS["q_press"] = True
                    # self.running = False

                elif event.key == pygame.K_e:
                    INPUTS["e_press"] = True

                elif event.key == pygame.K_r:
                    INPUTS["r_press"] = True
                
                elif event.key == pygame.K_m:
                    INPUTS["m_press"] = True

                elif event.key == pygame.K_i:
                    INPUTS["i_press"] = True

                elif event.key == pygame.K_c:
                    INPUTS["c_press"] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    INPUTS["space"] = False

                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    INPUTS["left"] = False

                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    INPUTS["right"] = False

                elif event.key in (pygame.K_UP, pygame.K_w):
                    INPUTS["up"] = False

                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    INPUTS["down"] = False
                
                elif event.key == pygame.K_q:
                    INPUTS["q_press"] = False
                
                elif event.key == pygame.K_e:
                    INPUTS["e_press"] = False

                elif event.key  == pygame.K_r:
                    INPUTS["r_press"] = False

                elif event.key == pygame.K_m:
                    INPUTS["m_press"] = False

                elif event.key == pygame.K_i:
                    INPUTS["i_press"] = False

                elif event.key == pygame.K_c:
                    INPUTS["c_press"] = False
            
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    INPUTS["scroll_up"] = True
                if event.y == -1:
                    INPUTS["scroll_down"] = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    INPUTS["left_click"] = True
                elif event.button == 3:
                    INPUTS["right_click"] = True
                elif event.button == 4:
                    INPUTS["scroll_down"] = True
                elif event.button == 2:
                    INPUTS["scroll_up"] = True
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    INPUTS["left_click"] = False
                elif event.button == 3:
                    INPUTS["right_click"] = False
                elif event.button == 4:
                    INPUTS["scroll_down"] = False
                elif event.button == 2:
                    INPUTS["scroll_up"] = False
    
    def reset_inputs(self):
        for key in INPUTS:
            INPUTS[key] = False

    def loop(self):
        while self.running:
            dt = self.clock.tick(self.FPS)/1000
            self.get_inputs()
            self.states[-1].update(dt)
            self.states[-1].draw(self.screen)
            self.custom_cursor(self.screen)
            pygame.display.update()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.loop()