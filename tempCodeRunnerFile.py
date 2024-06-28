import pygame, sys, random
import os
from os.path import join

pygame.mixer.pre_init(frequency = 44100, size = - 16, channels = 2, buffer = 512)
pygame.init()
pygame.display.set_caption("Flappy Bird")
icon = pygame.image.load("FileGame/assets/icon.png")
pygame.display.set_icon(icon)

def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos))
    top_pipe_height = random.randint(700, 750)
    top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos - top_pipe_height))
    return bottom_pipe, top_pipe    

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            die_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        hit_sound.play()
        die_sound.play()
        return False
    return True

def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 2, 1)
    return new_bird

def bird_animation():
    if bird_color == "yellow":
        bird_list = yellow_bird_list
    else:
        bird_list = blue_bird_list
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect 

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)
    
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {str(int(score))}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)
        
        high_score_surface = game_font.render(f'High Score: {str(int(high_score))}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (216, 630))
        screen.blit(high_score_surface, high_score_rect)
        
flap_sound = pygame.mixer.Sound(join("FileGame", "sound", "sfx_wing.wav"))
hit_sound = pygame.mixer.Sound(join("FileGame", "sound", "sfx_hit.wav"))
point_sound = pygame.mixer.Sound(join("FileGame", "sound", "sfx_point.wav"))
die_sound = pygame.mixer.Sound(join("FileGame", "sound", "sfx_die.wav"))
score_sound_countdown = 100

def update_high_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def update_score(pipes, bird_rect):
    global score
    for pipe in pipes:
        if bird_rect.centerx > pipe.centerx and bird_rect.centerx <= pipe.centerx + 3:
            point_sound.play()
            score += 1/2

game_font = pygame.font.Font('FileGame/04B_19.TTF', 40)
high_score = 0
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
score = 0 
gravity = 0.25
bird_movement = 0
game_active = False
menu_state = True

# Tạo các hình ảnh cho con chim xanh
blue_bird_up = pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "bluebird-upflap.png")).convert_alpha())
blue_bird_mid = pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "bluebird-midflap.png")).convert_alpha())
blue_bird_down = pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "bluebird-downflap.png")).convert_alpha())
blue_bird_list = [blue_bird_down, blue_bird_mid, blue_bird_up]

# Tạo các hình ảnh cho con chim vàng
yellow_bird_up = pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "yellowbird-upflap.png")).convert_alpha())
yellow_bird_mid = pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "yellowbird-midflap.png")).convert_alpha())
yellow_bird_down = pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "yellowbird-downflap.png")).convert_alpha())
yellow_bird_list = [yellow_bird_down, yellow_bird_mid, yellow_bird_up]

# Biến để lưu trạng thái của con chim
bird_color = "yellow"
bird_index = 0
if bird_color == "yellow":
    bird = yellow_bird_list[bird_index]
else:
    bird = blue_bird_list[bird_index]
bird_rect = bird.get_rect(center = (100, 384))

# Các hình ảnh khác
background = pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "background-night.png")).convert())
floor = pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "floor.png")).convert())
floor_x_pos = 0
game_over_surface = pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "gameover.png")).convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216, 384))
pipe_surface = pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "pipe-green.png")).convert())
pipe_list = []
pipe_height = [200, 300, 400]
menu_surface = pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "message.png")).convert_alpha())
menu_rect = menu_surface.get_rect(center=(216, 384))
character_button1 = pygame.transform.scale(pygame.image.load(join("FileGame", "assets", "bluebird-midflap.png")).convert_alpha(), (64, 64))
character_button1_rect = character_button1.get_rect(center = (144, 488))

spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, 1200)

bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)

while True:
    for event in pygame.event.get():
            
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = - 8
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                menu_state = False
                game_active = True
                pipe_list.clear()
                if bird_color == "yellow":
                    bird = yellow_bird_list[bird_index]
                    bird_rect = bird.get_rect(center = (100, 384))
                else:
                    bird = blue_bird_list[bird_index]
                    bird_rect = bird.get_rect(center = (100, 384))
                bird_movement = 0 
                score = 0
        if event.type == spawn_pipe:
            pipe_list.extend(create_pipe())
        if event.type == bird_flap:
            if bird_color == "yellow":
                if bird_index <  2:
                    bird_index += 1
                else:
                    bird_index = 0
            else:
                if bird_index <  2:
                    bird_index += 1
                else:
                    bird_index = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if character_button1_rect.collidepoint(event.pos):
                bird_color = "blue"
                bird = blue_bird_list[bird_index]
                bird_rect = bird.get_rect(center = (100, 384))

    screen.blit(background, (0, 0))
    
    if menu_state:
        screen.blit(character_button1, character_button1_rect)
        draw_floor()
        if floor_x_pos <= -432:
            floor_x_pos = 0
        floor_x_pos -= 1
    elif game_active:
        if bird_color == "yellow":
            rotated_bird = rotate_bird(bird)
            bird, bird_rect = bird_animation()
        else:
            rotated_bird = rotate_bird(bird)
            bird, bird_rect = bird_animation()
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        update_score(pipe_list, bird_rect)
        score_display('main_game')
        
        draw_floor()
        if floor_x_pos <= -432:
            floor_x_pos = 0
        floor_x_pos -= 1
    else:
        
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_high_score(score, high_score)
        score_display('game_over')
    
    
    pygame.display.update()
    clock.tick(120)