import pygame

# effects = []

# hit_x_speed = 0
# hit_y_speed = -1
# hit_life = 60
# hit_size = 30
# hit_font = None
# hit_font_file = "content/fonts/Simonetta-Italic.ttf"

# def create_hit_text(x, y, text, color = (255, 0, 0)):
#     global hit_font
#     if hit_font is None:
#         hit_font = pygame.font.Font(hit_font_file, hit_size)
#     image = hit_font.render(text, True, color)
#     Effect(x, y, hit_x_speed, hit_y_speed, hit_life, image)

class Effect(pygame.sprite.Sprite):
    def __init__(self, game, x, y, groups, layer):
        super().__init__(groups)
        self.x = x
        self.y = y
        self.game = game
        self._layer = layer
        
        # global effects
        # effects.append(self)

    def import_images(self, path):
        self.animations = self.game.get_animations(path)

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = self.game.get_images(full_path)

    def animate(self, state, fps, loop = True):
        self.frame_index += fps

        if self.frame_index >= len(self.animations[state]) - 1:
            if loop:
                self.frame_index = 0
            else:
                self.kill()
                return
        
        self.image = self.animations[state][int(self.frame_index)]

    def draw(self, screen):
        self.life -= 1
        if self.life <= 0:
            # global effects
            # effects.remove(self)
            self.kill()
        screen.blit(self.image, (self.x, self.y))

class AttackEffect(Effect):
    def __init__(self, game, x, y, groups, character, layer):
        super().__init__(game, x, y, groups, layer)
        self.frame_index = 0
        self.character = character
        self.import_images(f"assets/effects/attack/")
        self.image = self.animations[f"attack_effect_{self.character.get_direction()}"][self.frame_index]
        self.rect = self.image.get_frect(topleft = (self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.timer = 0.5

    
    def get_collide_list(self, group):
        collidable_list = pygame.sprite.spritecollide(self, group, False)
        return collidable_list
    
    def collision(self, group):
        for sprite in self.get_collide_list(group):
            if self.rect.colliderect(sprite.rect):
                if self.mask.overlap_mask(sprite.mask, (sprite.pos[0] - self.x, sprite.pos[1] - self.y)):
                    sprite.health -= self.character.damage
        return

    def update(self, dt):
        if self.timer <= 0:
            self.kill()
            return
        self.timer -= dt
        self.animate(f"attack_effect_{self.character.get_direction()}", 15 * dt, False)