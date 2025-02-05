import pygame
from settings import *
from characters import NPC
from player import Player, Attack
from camera import Camera
from enemy import Enemy
from tile import Tile
from transition import Transition
from pytmx.util_pygame import load_pygame
from objects import Object, Wall, Collider
from ui.bar import Bar

class State:
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def enter_state(self):
        if len(self.game.states) > 1:
            self.prev_state = self.game.states[-1]
        self.game.states.append(self)

    def exit_state(self):
        self.game.states.pop()

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

class SplashScreen(State):
    def __init__(self, game):
        super().__init__(game)
        self.current_scene = "0"
        self.entry_point = "0"
    
    def update(self, dt):
        if INPUTS["space"]:
            Scene(self.game, "0", "0").enter_state()
            self.game.reset_inputs()

    def draw(self, screen):
        screen.fill(COLOURS["blue"])
        self.game.render_text("Splash Screen, press space", COLOURS["white"], self.game.font, (WIDTH/2, HEIGHT/2))


class Scene(State):
    def __init__(self, game, current_scene, entry_point):
        super().__init__(game)

        self.current_scene = current_scene
        self.entry_point = entry_point

        self.camera = Camera(self)
        
        self.update_sprites = pygame.sprite.Group()
        self.drawn_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.tile_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()
        self.exit_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()

        self.tmx_data = load_pygame(f"scenes/{self.current_scene}/{self.current_scene}.tmx")

        self.create_scene()

        self.transition = Transition(self)

    def go_to_scene(self):
        Scene(self.game, self.new_scene, self.entry_point).enter_state()

    def draw_health_bar(self, health, x, y, screen):
        # ratio = health / 100
        # health_bar = pygame.Rect(x, y, 100 * ratio, 5)
        # pygame.draw.rect(screen, COLOURS["black"], (x, y, 100, 5))
        # pygame.draw.rect(screen, COLOURS["red"], health_bar)
        
        self.font = pygame.font.Font("assets/fonts/LexendExa-Regular.ttf", 10)
        self.game.render_text("Health:", COLOURS["white"], self.font, (30, y-4))

    def draw_stamina_bar(self, stamina, x, y, screen):
        # ratio = stamina / 100
        # stamina_bar = pygame.Rect(x, y, 100 * ratio, 5)
        # pygame.draw.rect(screen, COLOURS["black"], (x, y, 100, 5))
        # pygame.draw.rect(screen, COLOURS["orange"], stamina_bar)
        # stamina_bar = Bar(x, y, stamina, COLOURS["black"], COLOURS["orange"], 100, 5)
        # stamina_bar.draw(screen)
        self.font = pygame.font.Font("assets/fonts/LexendExa-Regular.ttf", 10)
        self.game.render_text("Stamina:", COLOURS["white"], self.font, (30, y-4))

    

    def create_scene(self):
        layers = []

        for l in self.tmx_data.layers:
            layers.append(l.name)

        if "blocks" in layers:
            for x, y, surf in self.tmx_data.get_layer_by_name("blocks").tiles():
                Wall([self.block_sprites, self.drawn_sprites], (x * TILESIZE, y * TILESIZE), "blocks", surf)
        
        if "tiles" in layers:
            for x, y, surf in self.tmx_data.get_layer_by_name("tiles").tiles():
                Tile([self.tile_sprites, self.drawn_sprites], (x * TILESIZE, y * TILESIZE), "background", surf)

        if "entries" in layers:
            for obj in self.tmx_data.get_layer_by_name("entries"):
                if obj.name == self.entry_point:
                    self.player = Player(self.game, self, [self.update_sprites, self.drawn_sprites, self.player_sprites], (obj.x, obj.y), "blocks" ,"player")
                    self.target = self.player
                    
                    self.camera.offset = vec(self.player.rect.centerx - WIDTH/2, self.player.rect.centery - HEIGHT/2)
        
        if "exits" in layers:
            for obj in self.tmx_data.get_layer_by_name("exits"):
                Collider([self.exit_sprites], (obj.x, obj.y), (obj.width, obj.height), obj.name)

        if "entities" in layers:
            for obj in self.tmx_data.get_layer_by_name("entities"):
                if "npc" in obj.name:
                    self.npc = NPC(self.game, self, [self.update_sprites, self.drawn_sprites, self.npc_sprites], (obj.x, obj.y), "blocks" , obj.name)
                if "enemy" in obj.name:
                    self.npc = Enemy(self.game, self, [self.update_sprites, self.drawn_sprites, self.enemy_sprites], (obj.x, obj.y), "blocks" , obj.name)


    def debugger(self, debug_list):
        for index, name in enumerate(debug_list):
            self.game.render_text(name, COLOURS["white"], self.game.font, (10, 15 * index), False)
    
    def update(self, dt):
        self.update_sprites.update(dt)
        self.camera.update(dt, self.target)
        self.transition.update(dt)

    def draw(self, screen):
        self.camera.draw(screen, self.drawn_sprites)
        self.transition.draw(screen)
        # health_bar = Bar(10, 200, self.player.health, self.player.max_health, self.player.target_health, self.player.health_regen, COLOURS["black"], COLOURS["red"], 100, 5)
        # health_bar.draw(screen)
        # stamina_bar = Bar(10, 215, self.player.stamina, self.player.max_stamina, self.player.target_stamina, self.player.stamina_regen, COLOURS["black"], COLOURS["orange"], 100, 5)
        # stamina_bar.draw(screen)
        self.player.update_health()
        self.player.update_stamina()
        self.player.draw_bar(10, 200, self.player.health, self.player.max_health, COLOURS["black"], COLOURS["red"])
        self.player.draw_bar(10, 215, self.player.stamina, self.player.max_stamina, COLOURS["black"], COLOURS["orange"])
        self.draw_health_bar(self.player.health, 10, 200, screen)
        self.draw_stamina_bar(self.player.stamina, 10, 215, screen)

        # self.debugger([
        #                 str("FPS: " + str(round(self.game.clock.get_fps(), 2))),
        #                 str("Velocity: " + str(round(self.player.vel, 2))),
        #                 str("State: " + str(self.player.state)),
        #                 str("Target stamina: " + str(self.player.target_stamina))
        # ])