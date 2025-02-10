from pygame.math import Vector2 as vec

WIDTH, HEIGHT  = 400, 224
TILESIZE = 16
FONT = "assets/fonts/LexendExa-Regular.ttf"

INPUTS = {'escape': False, 
          'space': False, 
          'up': False, 
          'down': False, 
          'left': False, 
          'right': False, 
          'left_click': False, 
          'right_click': False,
          'scroll_up': False,
          'scroll_down': False,
          'q_press': False,
          'e_press': False,
          'r_press': False,
          'm_press': False
          }

COLOURS = {"black": (0, 0, 0), 
           "white":(255, 255, 255),
           "red": (255, 100, 100),
           "green": (0, 255, 0),
           "blue": (100, 100, 255),
           "orange": (230, 150, 0),
           "yellow": (255, 255, 0)}

LAYERS = ["background", 
          "objects",
          "blocks", 
          "characters", 
          "particles",
          "foreground"]

SCENE_DATA = {
                0:{1: 1, 3: 2},
                1:{1: 0, 2: 2},
                2:{2: 1, 3: 0}
            }

player_stats = {"Health": 0,
                "Stamina": 0,
                "Damage": 0,
                "Level": 1,
                "EXP": 0,
                "Strength": 0,
                "Dexterity": 0,
                "Agility": 0,
                "Intellect": 0,
                "Vitality": 0,
                "x-pos" : 0,
                "y-pos" : 0,
            }

map_data = {"player_direction": "right",
            "scene_num": 0,
            "entry_point_num": 0
            }

enemy_stats = {"Health": 0,
               "Damage": 0,
               "Level": 0,
               "Range": 0}

equipment = {"Headpiece": None,
             "Body": None,
             "Left hand": None,
             "Right hand": None,
             "Boots": None}

inventory = {0: [None, None, None, None, None, None],
             1: [None, None, None, None, None, None],
             2: [None, None, None, None, None, None],
             3: [None, None, None, None, None, None],
             4: [None, None, None, None, None, None],
             5: [None, None, None, None, None, None]}