import pygame
from settings import *
from characters import Entity
from math_extras import distance

class Enemy(Entity):
    def __init__(self, game, scene, group, pos, layer, name, direction):
        super().__init__(game, scene, group, pos, layer, name, direction)

        self.state = Idle(self)
        # self.image = self.animations[f"idle_{self.direction}"][self.frame_index]
        self.health = 100
        self.max_health = self.health
        self.regen = 0.01
        self.damage = 25
        self.sight = 500
        self.attack_range = 100
        self.is_alive = True
        self.stats = enemy_stats.copy()
        self.other = self.scene.player_sprites
        self.setup_stats()

    def get_attack_collision(self):
        if self.state == Attack:
            collidable_enemies = self.get_collide_list(self.other)
            if len(collidable_enemies) != 0:
                for sprite in collidable_enemies:
                    if self.rect.colliderect(sprite.rect):
                        if self.mask.overlap_mask(sprite.mask, (sprite.pos[0] - self.pos[0], sprite.pos[1] - self.pos[1])):
                            sprite.target_health -= self.damage
                            sprite.state = Hit()

    def setup_stats(self):
        self.stats["Health"] = self.health
        self.stats["Damage"] = self.damage
        self.stats["Range"] = self.attack_range

    def update_health(self):
        if self.health >= self.max_health:
            self.health = self.max_health
        else:
            self.health += self.regen
        
        self.stats["Health"] = self.health

    def on_death(self):
        if self.health <= 0:
            self.is_alive = False

    def update(self, dt):
        self.update_health()
        self.on_death()
        self.state.update(self, dt)
class Idle:
    def __init__(self, character):
        character.frame_index = 0
    
    def enter_state(self, character):
        if character.vel.magnitude() > 1:
            return Run(character)

    def update(self, character, dt):
        character.animate("idle", 15 * dt)
        character.movement()
        character.physics(dt, character.frict)

class Run:
    def __init__(self, character):
        Idle.__init__(self, character)
    
    def enter_state(self, character):
        if character.vel.magnitude() < 1:
            return Idle(character)

    def update(self, character, dt):
        character.animate("run", 15 * dt)
        character.movement()
        character.physics(dt, character.frict)

class Attack:
    def __init__(self, character):
        Idle.__init__(self, character)
        self.timer = 0.5
        
    def enter_state(self, character):
        if self.timer <= 0:
            return Idle(character)

    def update(self, character, dt):
        self.timer -= dt
        character.animate(f"attack_{character.get_attack_direction()}", 15 * dt, False)

        character.physics(dt, character.frict)
        character.acc = vec()
        character.vel = self.vel

class Hit:
    def __init__(self, character):
        Idle.__init__(self, character)
        self.timer = 0.25

    def enter_state(self, character):
        if self.timer <= 0:
            return Idle(character)

    def update(self, character, dt):
        self.timer -= dt
        character.animate(f"hit_{character.get_direction()}", 15 * dt, False)