import pygame
import os
from config import *
import sys

pygame.mixer.init()

def get_path(filepath: str):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filepath)
    return os.path.join(os.path.dirname(__file__), filepath)


# app icon
app_icon = pygame.image.load(get_path('Game_Assests/icon.png'))

# background
background = pygame.image.load(get_path('Game_Assests/covers/background.png'))

# Menu Cover
menu_cover = pygame.image.load(get_path('Game_Assests/covers/menu-cover.png'))
menu_cover = pygame.transform.scale(menu_cover, (WIDTH, HEIGHT))

# Game Over Cover
game_over = pygame.image.load(get_path('Game_Assests/covers/gameover-cover.png'))
game_over = pygame.transform.scale(game_over, (WIDTH, HEIGHT))

# Doodle
doodle_right = pygame.image.load(get_path('Game_Assests/sprites/right.png'))
doodle_right = pygame.transform.scale(doodle_right, (DOODLE_WIDTH, DOODLE_HEIGHT))
doodle_left = pygame.image.load(get_path('Game_Assests/sprites/left.png'))
doodle_left = pygame.transform.scale(doodle_left, (DOODLE_WIDTH, DOODLE_HEIGHT))

# Platforms
platform = pygame.image.load(get_path('Game_Assests/sprites/platform.png'))
platform = pygame.transform.scale(platform, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

broken_platform0 = pygame.image.load(get_path('Game_Assests/sprites/broken_platform0.png'))
broken_platform0 = pygame.transform.scale(broken_platform0, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

broken_platform1 = pygame.image.load(get_path('Game_Assests/sprites/broken_platform1.png'))
broken_platform1 = pygame.transform.scale(broken_platform1, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

broken_platform2 = pygame.image.load(get_path('Game_Assests/sprites/broken_platform2.png'))
broken_platform2 = pygame.transform.scale(broken_platform2, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

broken_platform3 = pygame.image.load(get_path('Game_Assests/sprites/broken_platform3.png'))
broken_platform3 = pygame.transform.scale(broken_platform3, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

exploding_platform0 = pygame.image.load(get_path('Game_Assests/sprites/explosive_platform0.png'))
exploding_platform0 = pygame.transform.scale(exploding_platform0, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

exploding_platform1 = pygame.image.load(get_path('Game_Assests/sprites/explosive_platform1.png'))
exploding_platform1 = pygame.transform.scale(exploding_platform1, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

exploding_platform2 = pygame.image.load(get_path('Game_Assests/sprites/explosive_platform2.png'))
exploding_platform2 = pygame.transform.scale(exploding_platform2, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

horizental_platform = pygame.image.load(get_path('Game_Assests/sprites/horizontal_platform.png'))
horizental_platform = pygame.transform.scale(horizental_platform, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

vertical_platform = pygame.image.load(get_path('Game_Assests/sprites/vertical_platform.png'))
vertical_platform = pygame.transform.scale(vertical_platform, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

# Monsters
bat1 = pygame.image.load(get_path('Game_Assests/monsters/bat1.png'))
bat1 = pygame.transform.scale(bat1, (MONSTER_WIDTH, MONSTER_HEIGHT))

bat2 = pygame.image.load(get_path('Game_Assests/monsters/bat2.png'))
bat2 = pygame.transform.scale(bat2, (MONSTER_WIDTH, MONSTER_HEIGHT))

bat3 = pygame.image.load(get_path('Game_Assests/monsters/bat3.png'))
bat3 = pygame.transform.scale(bat3, (MONSTER_WIDTH, MONSTER_HEIGHT))

# Top Score
top_score = pygame.image.load(get_path('Game_Assests/covers/top-score.png'))

# Pause 
pause_button = pygame.image.load(get_path('Game_Assests/buttons/pause.png'))

pause_screen = pygame.image.load(get_path('Game_Assests/covers/pause-cover.png'))
pause_screen = pygame.transform.scale(pause_screen, (WIDTH, HEIGHT))

# Buttons
play = pygame.image.load(get_path('Game_Assests/buttons/play.png'))
resume = pygame.image.load(get_path('Game_Assests/buttons/resume.png'))
play_again = pygame.image.load(get_path('Game_Assests/buttons/play_again.png'))
play_again = pygame.transform.scale(play_again, (play.get_width(), play.get_height()))
menu_button = pygame.image.load(get_path('Game_Assests/buttons/menu.png'))

# Feeders
feeder_down = pygame.image.load(get_path('Game_Assests/sprites/feder.png'))
feeder_down = pygame.transform.scale(feeder_down, (FEEDER_WIDTH, FEEDER_HEIGHT))
feeder_up = pygame.image.load(get_path('Game_Assests/sprites/feder_up.png'))
feeder_up = pygame.transform.scale(feeder_up, (FEEDER_WIDTH, FEEDER_HEIGHT))

# Trampolines
trampoline_down = pygame.image.load(get_path('Game_Assests/sprites/trampoline.png'))
trampoline_down = pygame.transform.scale(trampoline_down, (TRAMPOLINE_WIDTH, TRAMPOLINE_HEIGHT))
trampoline_up = pygame.image.load(get_path('Game_Assests/sprites/trampoline_up.png'))
trampoline_up = pygame.transform.scale(trampoline_up, (TRAMPOLINE_WIDTH, TRAMPOLINE_HEIGHT))

# Sounds
exploding_platform_sound = pygame.mixer.Sound(get_path('Game_Assests/sounds/exploding_platform.wav'))
fall_sound = pygame.mixer.Sound(get_path('Game_Assests/sounds/exploding_platform.wav'))
feder_sound = pygame.mixer.Sound(get_path('Game_Assests/sounds/feder.mp3'))
jump_sound = pygame.mixer.Sound(get_path('Game_Assests/sounds/jump.wav'))
jump_on_monster_sound = pygame.mixer.Sound(get_path('Game_Assests/sounds/jumponmonster.mp3'))
monster_crash_sound = pygame.mixer.Sound(get_path('Game_Assests/sounds/monster-crash.mp3'))
platform_break_sound = pygame.mixer.Sound(get_path('Game_Assests/sounds/monster-crash.mp3'))
trampoline_sound = pygame.mixer.Sound(get_path('Game_Assests/sounds/trampoline.wav'))