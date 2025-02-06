import pygame
from settings import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, game, scene, group, pos, layer, name):
        super().__init__(group)

        self.game = game
        self.scene = scene
        self._layer = layer
        self.name = name
        self.import_images(f"assets/characters/{self.name}/")
        self.frame_index = 0
        self.image = self.animations["idle_right"][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.hitbox = self.rect.copy().inflate(-self.rect.width/2, -self.rect.height/2)
        self.speed = 60
        self.force = 2000
        self.acc = vec()
        self.vel = vec()
        self.frict = -15
        self.move = {"left": False, "right": False, "up": False, "down": False}
        self.state = Idle(self)
        
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
                self.frame_index = len(self.animations[state]) - 1
        
        self.image = self.animations[state][int(self.frame_index)]

    def get_direction(self):
        angle = self.vel.angle_to(vec(0, 1))
        angle = (angle + 360) % 360
        if 45 <= angle < 135: return "right"
        if 135 <= angle < 225: return "up"
        if 225 <= angle < 315: return "left"
        else: return "down"

    def movement(self):
        if self.move["left"]: self.acc.x = -self.force
        elif self.move["right"]: self.acc.x = self.force
        else: self.acc.x = 0
        
        if self.move["up"]: self.acc.y = -self.force
        elif self.move["down"]: self.acc.y = self.force
        else: self.acc.y = 0

    def get_collide_list(self, group):
        collidable_list = pygame.sprite.spritecollide(self, group, False)
        return collidable_list
    
    def collision(self, axis, group):
        for sprite in self.get_collide_list(group):
            if self.hitbox.colliderect(sprite.hitbox):
                if axis == "x":
                    if self.vel.x >= 0: self.hitbox.right = sprite.hitbox.left
                    if self.vel.x <= 0: self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx

                if axis == "y":
                    if self.vel.y >= 0: self.hitbox.bottom = sprite.hitbox.top
                    if self.vel.y <= 0: self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery

    def physics(self, dt, frict):
        # x-direction
        self.acc.x += self.vel.x * frict
        self.vel.x += self.acc.x * dt
        self.hitbox.centerx += self.vel.x * dt + (self.vel.x / 2)*dt
        self.rect.centerx = self.hitbox.centerx
        self.collision("x", self.scene.block_sprites)

        # y-direction
        self.acc.y += self.vel.y * frict
        self.vel.y += self.acc.y * dt
        self.hitbox.centery += self.vel.y * dt + (self.vel.y / 2)*dt
        self.rect.centery = self.hitbox.centery
        self.collision("y", self.scene.block_sprites)


        if self.vel.magnitude() >= self.speed:
            self.vel = self.vel.normalize() * self.speed

    def change_state(self):
        new_state = self.state.enter_state(self)
        if new_state: self.state = new_state
        else: self.state

    def update(self, dt):
        self.get_direction()
        self.change_state()
        self.state.update(self, dt)

class Idle:
    def __init__(self, character):
        character.frame_index = 0
    
    def enter_state(self, character):
        if character.vel.magnitude() > 1:
            return Run(character)

    def update(self, character, dt):
        character.animate(f"idle_{character.get_direction()}", 15 * dt)
        character.movement()
        character.physics(dt, character.frict)

class Run:
    def __init__(self, character):
        Idle.__init__(self, character)
    
    def enter_state(self, character):
        if character.vel.magnitude() < 1:
            return Idle(character)

    def update(self, character, dt):
        character.animate(f"run_{character.get_direction()}", 15 * dt)
        character.movement()
        character.physics(dt, character.frict)

    