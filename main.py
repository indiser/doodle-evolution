import pygame
from config import HEIGHT, WIDTH
from assets import *
import random
from Doodle import Player
from Platform import Platform, ExplodingPlatform, MovingPlatform
from Feeder import Feeder
from Monster import Monster
from Trampoline import Trampoline
import json


def load_high_score():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as file:
                data = json.load(file)
                return data.get("high_score", 0)
        except Exception:
            return 0
    return 0

def save_high_score(new_high_score):
    with open(SAVE_FILE, "w") as file:
        json.dump({"high_score": new_high_score}, file)

pygame.init()
pygame.font.init()
pygame.mixer.init()

pygame.display.set_icon(app_icon)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font('Game_Assests/fonts/al-seana.ttf', 36)
font.set_bold(True)
top_score_bg = pygame.transform.scale(top_score, (TOP_SCORE_WIDTH, TOP_SCORE_HEIGHT))

pygame.display.set_caption("Doodle Jump")

is_paused = False
game_state = "MENU"
pause_rect = pause_button.get_rect(topright=(WIDTH - 10, 5))
screen_rect = screen.get_rect()
platform_rect = platform.get_rect()
running = True

platforms = []
active_feeders = []
score = 0
high_score = load_high_score()
player_name = "Doodler"

menu_doodle_x = 30
menu_doodle_y = 350
menu_doodle_velocity = 0
menu_jump_strength = -15
menu_platform_y = 380

play_rect = play.get_rect(topright=(WIDTH - 40, 120))
resume_rect = resume.get_rect(bottomright=(WIDTH - 30, HEIGHT - 50))
play_again_rect = play_again.get_rect(bottomright=(WIDTH - 50, HEIGHT - 200))
menu_button_rect = menu_button.get_rect(bottomright=(WIDTH - 30, HEIGHT - 120))

active_monsters = []
bat_frames = [bat1, bat2, bat3]

broken_frames = [broken_platform0, broken_platform1, broken_platform2, broken_platform3]

explosive_frames = [exploding_platform0, exploding_platform1, exploding_platform2]

def make_platform(x, y, current_score):
    roll = random.randint(1, 100)
    
    if roll <= 10:   # 10% Horizontal
        return MovingPlatform(x, y, horizental_platform, 'horizontal', current_score)
    elif roll <= 20: # 10% Vertical
        return MovingPlatform(x, y, vertical_platform, 'vertical', current_score)
    elif roll <= 35: # 15% Explosive
        return ExplodingPlatform(x, y, explosive_frames)
    elif roll <= 50: # 15% Broken
        return Platform(x, y, broken_platform0, breakable=True, broken_frames=broken_frames)
        
    return Platform(x, y, platform)

def spawn_entities(new_plat, current_score, active_feeders, active_monsters, bat_frames, active_trampolines):
    if type(new_plat) is Platform and not new_plat.breakable:
        entity_roll = random.randint(1, 100)
        
        # 1-5: Trampoline (5% chance, rarer than feeder)
        if entity_roll <= 5 and current_score > 1000:
            new_tramp = Trampoline(new_plat.rect.centerx + 15, new_plat.rect.top - 5, trampoline_down, trampoline_up)
            active_trampolines.append(new_tramp)
            
        # 6-15: Feeder (10% chance)
        elif entity_roll > 5 and entity_roll <= 15 and current_score > FEEDER_THRESHOLD:
            new_feeder = Feeder(new_plat.rect.centerx + 15, new_plat.rect.top - 5, feeder_down, feeder_up)
            active_feeders.append(new_feeder)
            
        # 16-25: Monster (10% chance)
        elif entity_roll > 15 and entity_roll <= 25 and current_score > 1:
            active_monsters.append(Monster(new_plat, 0, bat_frames))

active_trampolines = []

def reset_game():
    global platforms, active_feeders, active_monsters, score, player
    # 1. Clear the board
    active_trampolines.clear()
    platforms.clear()
    active_feeders.clear()
    active_monsters.clear()
    score = 0
    
    # 2. Rebuild the starting platform
    start_x = screen_rect.centerx - (PLATFORM_WIDTH // 2)
    start_y = screen_rect.bottom - 20
    start_p = Platform(start_x, start_y, platform)
    platforms.append(start_p)
    
    # 3. Reset the player
    player = Player(screen_rect.centerx, start_p.rect.top, doodle_right, doodle_left)
    
    # 4. Generate the initial climb
    current_y = start_p.rect.top
    while current_y > 0:
        gap = random.randint(60, 120)
        current_y -= gap
        p_x = random.randint(0, WIDTH - PLATFORM_WIDTH)
        platforms.append(make_platform(p_x, current_y, score))

# Call it once so the game is ready when you open the window
reset_game()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == "MENU":
                    game_state = "PLAYING"
                elif game_state == "PLAYING":
                    game_state = "PAUSED"
                elif game_state == "PAUSED":
                    game_state = "PLAYING"
                elif game_state == "GAME_OVER":
                    reset_game()
                    game_state = "PLAYING"
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == "MENU" and play_rect.collidepoint(event.pos):
                game_state = "PLAYING"
            elif game_state == "PLAYING" and pause_rect.collidepoint(event.pos):
                game_state = "PAUSED"
            elif game_state == "PAUSED" and resume_rect.collidepoint(event.pos):
                game_state = "PLAYING"
            elif game_state == "GAME_OVER":
                if play_again_rect.collidepoint(event.pos):
                    reset_game()
                    game_state = "PLAYING"
                elif menu_button_rect.collidepoint(event.pos):
                    reset_game()
                    game_state = "MENU"

    # --- 1. INPUT & PHYSICS ---
    if game_state == "MENU":
        # Apply gravity to the menu doodle
        menu_doodle_velocity += GRAVITY
        menu_doodle_y += menu_doodle_velocity
        
        # Fake collision with the painted platform
        if menu_doodle_y >= menu_platform_y:
            menu_doodle_y = menu_platform_y
            menu_doodle_velocity = menu_jump_strength
            jump_sound.play()
            
    if game_state == "PLAYING":
        keys = pygame.key.get_pressed()
        player.move(keys, MOVE_SPEED, WIDTH)
        player.apply_gravity(GRAVITY)

        # --- 2. COLLISIONS ---
        if player.y_velocity > 0:
            hit_boost = False

            for t in active_trampolines:
                if player.rect.colliderect(t.rect):
                    player.rect.bottom = t.rect.top
                    player.jump(JUMP_STRENGTH, boost_multiplier=2.5, flip=True)
                    t.trigger()
                    score += 700
                    hit_boost = True
                    trampoline_sound.play()
                    break

            if not hit_boost:
                for f in active_feeders:
                    if player.rect.colliderect(f.rect):
                        player.rect.bottom = f.rect.top
                        player.jump(JUMP_STRENGTH, boost_multiplier=1.8)
                        f.trigger()
                        hit_boost = True
                        feder_sound.play()
                        break

            if not hit_boost:
                for p in platforms:
                    if not p.broken and player.rect.colliderect(p.rect):
                        player.rect.bottom = p.rect.top
                        player.jump(JUMP_STRENGTH)
                        if p.breakable:
                            p.break_platform()
                            platform_break_sound.play()
                        else:
                            jump_sound.play()
                        break


        if player.rect.top > HEIGHT:
            game_state = "DEATH_FALL"
            fall_sound.play()
            if score > high_score:
                high_score = score
                save_high_score(high_score)

        for m in active_monsters[:]:
            if player.rect.colliderect(m.rect):
                if player.y_velocity > 0 and player.rect.bottom < m.rect.centery + 10:
                    player.jump(JUMP_STRENGTH)
                    active_monsters.remove(m)
                    jump_on_monster_sound.play()
                else:
                    player.y_velocity = 0 # Kill momentum
                    game_state = "DEATH_FALL"
                    monster_crash_sound.play()
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)

        # --- 2.5 UPDATE/CLEANUP PLATFORMS (every frame) ---
        for p in platforms[:]:
            p.update()
            if p.finished or p.rect.top >= HEIGHT:
                platforms.remove(p)

                new_x = random.randint(0, WIDTH - PLATFORM_WIDTH)
                highest_y = min([plat.rect.y for plat in platforms])
                new_y = highest_y - random.randint(60, 120)
                new_plat = make_platform(new_x, new_y, score)
                platforms.append(new_plat)

                spawn_entities(new_plat, score, active_feeders, active_monsters, bat_frames, active_trampolines)

        for m in active_monsters[:]:
            m.update()
            # If the monster's parent platform was deleted, kill the monster
            if m.platform not in platforms:
                active_monsters.remove(m)


        # --- 3. CAMERA & WORLD SHIFT ---
        scroll_threshold = HEIGHT // 3
        if player.rect.top <= scroll_threshold:
            player.rect.top = scroll_threshold
            
            # Invert the negative upward velocity to create positive downward shift
            shift = player.y_velocity 
            score -= shift

            # Shift platforms and handle generation
            for p in platforms[:]:
                p.scroll(shift)
                if p.rect.top >= HEIGHT:
                    platforms.remove(p)
                    
                    new_x = random.randint(0, WIDTH - PLATFORM_WIDTH)
                    highest_y = min([plat.rect.y for plat in platforms]) 
                    new_y = highest_y - random.randint(60, 120)
                    new_plat = make_platform(new_x, new_y, score)
                    platforms.append(new_plat)

                    spawn_entities(new_plat, score, active_feeders, active_monsters, bat_frames, active_trampolines)

            for f in active_feeders[:]:
                f.scroll(shift)
                if f.rect.top >= HEIGHT:
                    active_feeders.remove(f)

            for t in active_trampolines[:]:
                t.scroll(shift)
                if t.rect.top >= HEIGHT:
                    active_trampolines.remove(t)
        

    # --- 4. RENDER ---
    if game_state == "MENU":
        screen.blit(menu_cover, (0, 0))
        screen.blit(doodle_right, (menu_doodle_x, menu_doodle_y))
        screen.blit(play, play_rect)

    elif game_state == "DEATH_FALL":
        player.apply_gravity(GRAVITY)
        
        shift = player.y_velocity
        
        for p in platforms[:]:
            p.rect.y -= shift
            if p.rect.bottom < 0: platforms.remove(p)
                
        for f in active_feeders[:]:
            f.rect.y -= shift
            if f.rect.bottom < 0: active_feeders.remove(f)
                
        for m in active_monsters[:]:
            m.rect.y -= shift
            if m.rect.bottom < 0: active_monsters.remove(m)

        for t in active_trampolines[:]:
            t.rect.y -= shift
            if t.rect.bottom < 0: active_trampolines.remove(t)
            
        if len(platforms) == 0:
            game_state = "GAME_OVER"
    else:

        screen.blit(background, (0, 0))

        for p in platforms:
            p.draw(screen)
        for f in active_feeders:
            f.draw(screen)
        for m in active_monsters:
            m.draw(screen)
        for t in active_trampolines:
            t.draw(screen)
            
        player.draw(screen)

        screen.blit(top_score_bg, (0, 0))
        score_surface = font.render(f"{int(score)}", True, (0, 0, 0))    
        screen.blit(score_surface, (10, 2))
        screen.blit(pause_button, pause_rect)

        if game_state == "PAUSED":
            screen.blit(pause_screen, (0, 0))
            screen.blit(resume, resume_rect)

        elif game_state == "GAME_OVER":
            # Draw the background cover
            screen.blit(game_over, (0, 0))
            
            name_text = font.render(f"{player_name}", True, (0, 0, 0))
            score_text = font.render(f"{int(score)}", True, (0, 0, 0))
            high_score_text = font.render(f"{int(high_score)}", True, (0, 0, 0))

            value_x = WIDTH // 2 + 60
            
            screen.blit(score_text, (value_x, 180))
            screen.blit(high_score_text, (value_x, 225))  
            screen.blit(name_text, (value_x - 40, 268))

            screen.blit(play_again, play_again_rect)
            screen.blit(menu_button, menu_button_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()