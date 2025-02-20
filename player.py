import pygame
from settings import *
from characters import Entity, Hit
from effect import AttackEffect

class Player(Entity):
    def __init__(self, game, scene, group, pos, layer, name, direction):
        super().__init__(game, scene, group, pos, layer, name, direction)

        self.state = Idle(self)
        # self.image = self.animations[f"idle_{map_data["player_direction"]}"][self.frame_index]
        self.bar_width = 100
        
        self.health_regen = 0.01
        self.stamina_regen = 0.05
        self.damage = 25
        # self.weapon_type = "single"
        self.is_alive = True
        self.change_speed = 10
        
        self.stats = {"Health": 100,
                "Stamina": 100,
                "Damage": 25,
                "Level": 1,
                "EXP": 0,
                "EXP for next lvl": 100,
                "Strength": 0,
                "Dexterity": 0,
                "Agility": 0,
                "Intellect": 0,
                "Vitality": 0
            }
        self.health = self.stats["Health"]
        self.max_health = self.stats["Health"]
        self.stamina = self.stats["Stamina"]
        self.max_stamina = self.stats["Stamina"]
        self.equipment = equipment
        self.inventory = inventory

        # self.setup_stats()

    def setup_stats(self):
        self.stats["Health"] = self.health
        self.stats["Stamina"] = self.stamina
        self.stats["Damage"] = self.damage

    def movement(self):
        if INPUTS["left"]: self.acc.x = -self.force
        elif INPUTS["right"]: self.acc.x = self.force
        else: self.acc.x = 0
        player_coordinates["x-pos"] = self.hitbox.centerx
        
        if INPUTS["up"]: self.acc.y = -self.force
        elif INPUTS["down"]: self.acc.y = self.force
        else: self.acc.y = 0
        player_coordinates["y-pos"] = self.hitbox.centery

    def vec_to_mouse(self, speed):
        direction = vec(pygame.mouse.get_pos()) - (vec(self.hitbox.center) - vec(self.scene.camera.offset))
        if direction.length() > 0: direction.normalize_ip()
        return direction * speed

    def draw_bar(self, x_coord, y_coord, current_resource, max_resource, color1, color2):
        # transition_width = 0
        # transition_color = color2
        bar_ratio = max_resource/self.bar_width
        
        # if current_resource < target_resource:
        #     current_resource += self.change_speed
            # transition_width = int((target_resource - current_resource)/bar_ratio)
            # transition_color = COLOURS["green"]
        
        # if current_resource > target_resource:
        #     current_resource -= self.change_speed
            # transition_width = int((target_resource - current_resource)/bar_ratio)
            # transition_color = COLOURS["yellow"]
        # filled = self.amount / self.ratio
        # if (target_resource/bar_ratio) + transition_width >= self.bar_width:
        #     transition_width = self.bar_width - (target_resource/bar_ratio)
        normal_bar_rect = pygame.Rect(x_coord, y_coord, current_resource *bar_ratio, 5)
        # transition_bar_rect = pygame.Rect(normal_bar_rect.right, y_coord, transition_width, 5)
        
        # Draw background first
        pygame.draw.rect(self.scene.game.screen,
                        color1,
                        pygame.Rect(x_coord,
                                    y_coord,
                                    self.bar_width,
                                    5))
        
        
        # Then the foreground
        pygame.draw.rect(self.scene.game.screen,
                        color2,
                        normal_bar_rect)
        
        # pygame.draw.rect(self.scene.game.screen,
        #                  transition_color,
        #                  transition_bar_rect)
        
        # Create a white border around the bar
        pygame.draw.rect(self.scene.game.screen, 
                         (255, 255, 255), 
                         pygame.Rect(x_coord, 
                                     y_coord, 
                                     self.bar_width, 
                                     5),
                                     1)

    def update_health(self):
        if self.health >= self.max_health:
            self.health = self.max_health
        else:
            self.health += self.health_regen

        self.stats["Health"] = self.health
    
    def update_stamina(self):
        if self.stamina >= self.max_stamina:
            self.stamina = self.max_stamina
        else:
            self.stamina += self.stamina_regen

        self.stats["Stamina"] = self.stamina

    def on_death(self):
        if self.health <= 0:
            self.is_alive = False
            # self.state = Death(self)

    # def change_weapon_type(self):
    #     if INPUTS["q_press"] or INPUTS["e_press"]:
    #         if self.weapon_type == "dual": 
    #             self.weapon_type = "single"
    #             return
    #         if self.weapon_type == "single": 
    #             self.weapon_type = "dual"
    #             return

    def get_direction(self):
        angle = self.vel.angle_to(vec(0, 1))
        angle = (angle + 360) % 360
        if 45 <= angle < 135: 
            map_data["player_direction"] = "right"
            return map_data["player_direction"]
            # return "right"
        elif 135 <= angle < 225: 
            map_data["player_direction"] = "up"
            return map_data["player_direction"]
            # return "up"
        elif 225 <= angle < 315: 
            map_data["player_direction"] = "left"
            return map_data["player_direction"]
            # return "left"
        else: 
            map_data["player_direction"] = "down"
            return map_data["player_direction"]
            # return "down"
        # return player_stats["direction"]

    def get_attack_collision(self):
        if self.state == Attack:
            collidable_enemies = self.get_collide_list(self.scene.enemy_sprites)
            if len(collidable_enemies) != 0:
                for sprite in collidable_enemies:
                    if self.scene.attack_sprites.rect.colliderect(sprite.rect):
                        if self.scene.attack_sprites.mask.overlap_mask(sprite.mask, (sprite.pos[0] - self.pos[0], sprite.pos[1] - self.pos[1])):
                            if sprite.vulnerable:
                                sprite.health -= self.damage
                                sprite.state = Hit()
        
    def exit_scene(self):
        for exit in self.scene.exit_sprites:
            if self.hitbox.colliderect(exit.rect):
                self.scene.new_scene = SCENE_DATA[int(self.scene.current_scene)][int(exit.number)]
                self.scene.entry_point = exit.number
                self.scene.transition.exiting = True

    def update(self, dt):
        # self.change_weapon_type()
        self.get_direction()
        self.exit_scene()
        self.change_state()
        self.state.update(self, dt)
        self.on_death()
        
# Animation state classes
class Idle:
    def __init__(self, player):
        player.frame_index = 0
    
    def enter_state(self, player):
        # player.change_weapon_type()

        if player.vel.magnitude() > 1:
            return Run(player)
        
        if INPUTS["right_click"]:
            if player.stamina >= 10:
                return Dash(player)
        
        if INPUTS["left_click"]:
            return Attack(player, player.game.screen)      

    def update(self, player, dt):
        player.animate(f"idle_{player.get_direction()}", 15 * dt)
        player.movement()
        player.physics(dt, player.frict)

    def __str__(self):
        return "Idle"

class Run:
    def __init__(self, player):
        Idle.__init__(self, player)
    
    def enter_state(self, player):
        # player.change_weapon_type()

        if player.vel.magnitude() < 1:
            return Idle(player)
        
        if INPUTS["right_click"]:
            if player.stamina >= 10:
                return Dash(player)
        
        if INPUTS["left_click"]:
            return Attack(player, player.game.screen)

    def update(self, player, dt):
        player.animate(f"run_{player.get_direction()}", 15 * dt)
        player.movement()
        player.physics(dt, player.frict)
    
    def __str__(self):
        return "Run"

class Dash:
    def __init__(self, player):
        Idle.__init__(self, player)
        self.timer = 0.5
        INPUTS["right_click"] = False
        self.dash_pending = False
        self.vel = player.vec_to_mouse(200)
        player.stamina -= 10
        player.vulnerable = False

    def enter_state(self, player):
        if INPUTS["right_click"]:
            self.dash_pending = True
        if self.timer <= 0:
            if self.dash_pending and player.stamina >= 10:
                return Dash(player)
            player.vulnerable = True
            return Idle(player)

    def update(self, player, dt):
        self.timer -= dt
        player.animate(f"dashing_{player.get_direction()}", 15 * dt, False)

        player.physics(dt, -2)
        player.acc = vec()
        player.vel = self.vel

    def __str__(self):
        return "Dash"

class Attack:
    def __init__(self, player, surface):
        Idle.__init__(self, player)
        self.timer = 0.5
        INPUTS["left_click"] = False
        self.attack_pending = False
        self.vel = player.vec_to_mouse(10)
        self.surface = surface
        
        # self.attack_direction = player.get_direction()
        if map_data["player_direction"] == "left":
            x_pos = player.hitbox.centerx - (TILESIZE // 2)
            y_pos = player.hitbox.centery
        if map_data["player_direction"] == "right":
            x_pos = player.hitbox.centerx + (TILESIZE // 2)
            y_pos = player.hitbox.centery
        if map_data["player_direction"] == "up":
            x_pos = player.hitbox.centerx
            y_pos = player.hitbox.centery - (TILESIZE // 2)
        if map_data["player_direction"] == "down":
            x_pos = player.hitbox.centerx
            y_pos = player.hitbox.centery + (TILESIZE // 2)
        
        self.attack_effect = AttackEffect(player.game, x_pos, y_pos, 
                                          [player.scene.update_sprites, 
                                           player.scene.drawn_sprites, 
                                           player.scene.attack_sprites], 
                                          player, player.layer)

    def enter_state(self, player):
        if INPUTS["left_click"]:
            self.attack_pending = True
        if self.timer <= 0:
            if self.attack_pending:
                return Attack(player, player.game.screen)
            return Idle(player)

    def update(self, player, dt):
        self.timer -= dt
        player.animate(f"attack_{map_data["player_direction"]}", 15 * dt, False)
        self.attack_effect.collision(player.scene.enemy_sprites)
        # self.attack_effect.animate(f"attack_effect_{self.attack_direction}", 15 * dt, False)

        player.physics(dt, player.frict)
        player.acc = vec()
        player.vel = self.vel

    def __str__(self):
        return "Attack"

class Death:
    def __init__(self, player):
        Idle.__init__(self, player)
        self.timer = 0.25

    def enter_state(self, player):
        if self.timer <= 0:
            pass

    def update(self, player, dt):
        self.timer -= dt
        player.animate("death", 15 * dt, False)

    def __str__(self):
        return "Death"
        