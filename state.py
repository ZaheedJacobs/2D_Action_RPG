import pygame
from settings import *
from characters import NPC
from player import Player
from camera import Camera
from enemy import Enemy
from tile import Tile
from transition import Transition, MenuTransition
from pytmx.util_pygame import load_pygame
from objects import Wall, Collider
from ui.button import Button

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
    def __init__(self, game, current_scene = "0", entry_point = "0"):
        super().__init__(game)
        self.current_scene = current_scene
        self.entry_point = entry_point
        self.transition = MenuTransition(self)
    
    def update(self, dt):
        if INPUTS["space"]:
            Scene(self.game, self.current_scene, self.entry_point).enter_state()
            self.game.reset_inputs()

    def draw(self, screen):
        screen.fill(COLOURS["blue"])
        self.game.render_text("Splash Screen, press space", COLOURS["white"], self.game.font, (WIDTH/2, HEIGHT/2))

class MainMenu(SplashScreen):
    def __init__(self, game, current_scene = "0", entry_point = "0", scene = None):
        super().__init__(game, current_scene, entry_point)
        self.scene = scene
        self.new_game_button = Button(160, 80, COLOURS["white"], COLOURS["black"], "New Game", BUTTON_FONT, BUTTON_SIZE)
        self.continue_button = Button(160, 100, COLOURS["white"], COLOURS["black"], "Continue", BUTTON_FONT, BUTTON_SIZE)
        self.help_button = Button(160, 120, COLOURS["white"], COLOURS["black"], "Help", BUTTON_FONT, BUTTON_SIZE)
        self.quit_game_button = Button(160, 140, COLOURS["white"], COLOURS["black"], "Quit Game", BUTTON_FONT, BUTTON_SIZE)

    def reset_player_stats(self):
        global player_stats
        # new_stats = {}
        for stat, num in player_stats.items():
            if stat != "Level":
                player_stats[stat] = 0
        
        for pos, num in player_coordinates.items():
            player_coordinates[pos] = 0            

        player_stats["Level"] = 1

    def start_new_game(self):
        self.current_scene = "0"
        self.entry_point = "0"
        self.reset_player_stats()
        Scene(self.game, self.current_scene, self.entry_point).enter_state()
        self.game.reset_inputs()

    def load_current_game(self):
        if (player_coordinates["x-pos"] == 0 and player_coordinates["y-pos"] == 0):
            self.start_new_game()
        else:
            Scene(self.game, self.current_scene, self.entry_point).enter_state()
            self.game.reset_inputs()
    
    def check_button_press(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        if self.new_game_button.is_pressed(mouse_pos, mouse_pressed):
            self.start_new_game()
        
        elif self.continue_button.is_pressed(mouse_pos, mouse_pressed) or INPUTS["escape"]:
            self.load_current_game()

        elif self.help_button.is_pressed(mouse_pos, mouse_pressed):
            self.transition.exiting = True
            HelpScreen(self.game, self.current_scene, self.entry_point, self.scene).enter_state()
            self.game.reset_inputs()

        elif self.quit_game_button.is_pressed(mouse_pos, mouse_pressed):
            self.game.running = False

    def update(self, dt):
        self.check_button_press()
        self.transition.update(dt)

    def draw(self, screen):
        screen.fill(COLOURS["blue"])
        self.game.render_text("Menu Screen", COLOURS["white"], self.game.font, (WIDTH/2, HEIGHT/4))
        self.new_game_button.draw(screen)
        self.continue_button.draw(screen)
        self.help_button.draw(screen)
        self.quit_game_button.draw(screen)
        self.transition.draw(screen)
        
class HelpScreen(SplashScreen):
    def __init__(self, game, current_scene = "0", entry_point = "0", scene = None):
        super().__init__(game, current_scene, entry_point)
        self.scene = scene
        self.back_button = Button(20, 200, COLOURS["white"], COLOURS["black"], "Back to Main Menu", BUTTON_FONT, BUTTON_SIZE)

    def display_help_text(self, help_list):
        for index, control in enumerate(help_list):
            self.game.render_text(control, COLOURS["white"], self.game.font, (20, 20 * index), False)

    def draw(self, screen):
        screen.fill(COLOURS["blue"])
        # self.game.render_text("Help Screen", COLOURS["white"], self.game.font, (WIDTH/2, HEIGHT/4))
        self.display_help_text([
                                "Up-arrow/W -> Move up",
                                "Down-arrow/S -> Move down",
                                "Left-arrow/A -> Move Left",
                                "Right-Arrow/D -> Move Right",
                                "Left-click -> Attack",
                                "Right-click -> Dash",
                                "Escape key -> Open Main menu/Exit menu",
                                "C -> Open Character Stats Screen",
                                "I -> Open Inventory Screen"
                            ])
        self.back_button.draw(screen)
        self.transition.draw(screen)

    def check_button_press(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if self.back_button.is_pressed(mouse_pos, mouse_pressed) or INPUTS["escape"]:
            self.transition.exiting = True
            MainMenu(self.game, self.current_scene, self.entry_point, self.scene).enter_state()
            self.game.reset_inputs()

    def update(self, dt):
        self.check_button_press()
        self.transition.update(dt)

class StatScreen(SplashScreen):
    def __init__(self, game, current_scene="0", entry_point="0", scene = None):
        super().__init__(game, current_scene, entry_point)
        self.inventory_button = Button(170, 200, COLOURS["white"], COLOURS["black"], "Inventory", BUTTON_FONT, BUTTON_SIZE)
        self.scene = scene
    
    def check_button_press(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if INPUTS["escape"]:
            self.transition.exiting = True
            Scene(self.game, self.current_scene, self.entry_point).enter_state()
            self.game.reset_inputs()
        
        if INPUTS["i_press"] or self.inventory_button.is_pressed(mouse_pos, mouse_pressed):
            InventoryScreen(self.game, self.current_scene, self.entry_point, self.scene).enter_state()
            self.game.reset_inputs()

    def show_stats(self):
        index = 0
        for stat, num in self.scene.player.stats.items():
            self.game.render_text(f"{stat}: {num}", COLOURS["white"], self.game.font, (15, 15 +(15 * index)), False)
            index += 1

    def draw(self, screen):
        screen.fill(COLOURS["blue"])
        self.game.render_text("Stats", COLOURS["white"], self.game.font, (200, 5))
        self.transition.draw(screen)
        if not self.transition.exiting:
            self.show_stats()
        self.inventory_button.draw(screen)
        
    def update(self, dt):
        self.check_button_press()
        self.transition.update(dt)

class InventoryScreen(SplashScreen):
    def __init__(self, game, current_scene="0", entry_point="0", scene = None):
        super().__init__(game, current_scene, entry_point)
        self.scene = scene
        self.stats_button = Button(15, 200, COLOURS["white"], COLOURS["black"], "Stats", BUTTON_FONT, BUTTON_SIZE)

    def check_button_press(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if INPUTS["escape"]:
            Scene(self.game, self.current_scene, self.entry_point).enter_state()
            self.game.reset_inputs()
        
        if self.stats_button.is_pressed(mouse_pos, mouse_pressed) or INPUTS["c_press"]:
            StatScreen(self.game, self.current_scene, self.entry_point, self.scene).enter_state()
            self.game.reset_inputs()

    def draw(self, screen):
        screen.fill(COLOURS["blue"])
        self.transition.draw(screen)
        self.game.render_text("Inventory", COLOURS["white"], self.game.font, (200, 5))
        self.stats_button.draw(screen)
        
    def update(self, dt):
        self.check_button_press()
        self.transition.update(dt)

class Scene(State):
    def __init__(self, game, current_scene, entry_point):
        super().__init__(game)

        self.current_scene = current_scene
        self.entry_point = entry_point

        map_data["scene_num"] = self.current_scene
        map_data["entry_point_num"] = self.entry_point

        self.camera = Camera(self)
        
        self.update_sprites = pygame.sprite.Group()
        self.drawn_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.tile_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()
        self.exit_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()

        self.tmx_data = load_pygame(f"scenes/{self.current_scene}/{self.current_scene}.tmx")

        self.create_scene()

        self.transition = Transition(self)

    def go_to_scene(self):
        player_coordinates["x-pos"] = 0
        player_coordinates["y-pos"] = 0
        Scene(self.game, self.new_scene, self.entry_point).enter_state()
    
    def stop_player(self):
        self.player.vel.x = 0
        self.player.vel.y = 0

        self.player.acc.x = self.player.vel.x
        self.player.acc.y = self.player.vel.y

    def go_to_menu_screen(self):
        if INPUTS["escape"]:
            self.stop_player()
            MainMenu(self.game, map_data["scene_num"], map_data["entry_point_num"], self).enter_state()
            self.game.reset_inputs()

    def go_to_stats_screen(self):
        if INPUTS["c_press"]:
            self.stop_player()
            StatScreen(self.game, self.current_scene, self.entry_point, self).enter_state()
            self.game.reset_inputs()

    def go_to_inventory_screen(self):
        if INPUTS["i_press"]:
            self.stop_player()
            InventoryScreen(self.game, self.current_scene, self.entry_point, self).enter_state()
            self.game.reset_inputs()

    def draw_health_text(self, x = 30, y = 0):
        self.font = pygame.font.Font("assets/fonts/LexendExa-Regular.ttf", 10)
        self.game.render_text("Health:", COLOURS["white"], self.font, (30, y-4))

    def draw_stamina_text(self, x = 30, y = 0):
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
                    if player_coordinates["x-pos"] != 0 or player_coordinates["y-pos"] != 0:
                        self.pos = (player_coordinates["x-pos"], player_coordinates["y-pos"])
                    else:
                        self.pos = (obj.x, obj.y)
                    # self.player_direction = player_stats["direction"]
                    self.player = Player(self.game, 
                                        self, 
                                        [self.update_sprites, 
                                        self.drawn_sprites,
                                        self.player_sprites], 
                                        self.pos, 
                                        "blocks" ,
                                        "player", 
                                        map_data["player_direction"])
                    self.target = self.player
                    
                    self.camera.offset = vec(self.player.rect.centerx - WIDTH/2, self.player.rect.centery - HEIGHT/2)
        
        if "exits" in layers:
            for obj in self.tmx_data.get_layer_by_name("exits"):
                Collider([self.exit_sprites], (obj.x, obj.y), (obj.width, obj.height), obj.name)

        if "entities" in layers:
            for obj in self.tmx_data.get_layer_by_name("entities"):
                if "npc" in obj.name:
                    self.npc = NPC(self.game, self, 
                                   [self.update_sprites, self.drawn_sprites, self.npc_sprites], 
                                   (obj.x, obj.y), "blocks" , obj.name, "right")
                if "enemy" in obj.name:
                    self.npc = Enemy(self.game, self, 
                                    [self.update_sprites, self.drawn_sprites, self.enemy_sprites], 
                                    (obj.x, obj.y), "blocks" , obj.name, "right")

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

        self.player.update_health()
        self.player.draw_bar(10, 200, self.player.health, self.player.max_health, COLOURS["black"], COLOURS["red"])
        self.draw_health_text(30, 200)
        
        self.player.update_stamina()
        self.player.draw_bar(10, 215, self.player.stamina, self.player.max_stamina, COLOURS["black"], COLOURS["orange"])
        self.draw_stamina_text(30, 215)
        
        self.go_to_menu_screen()
        self.go_to_stats_screen()
        self.go_to_inventory_screen()

        self.debugger([
                        str("FPS: " + str(round(self.game.clock.get_fps(), 2))),
                        str("Velocity: " + str(round(self.player.vel, 2))),
                        "Vulnerable: " + str(self.player.vulnerable)
        ])