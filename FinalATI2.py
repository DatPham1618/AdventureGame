# Import necessary libraries
import pygame, sys, random
import os
from os.path import join

# Initialize Pygame mixer and display
pygame.mixer.pre_init(frequency = 44100, size = - 16, channels = 2, buffer = 512)
pygame.init()
pygame.display.set_caption("Flappy Bird")
icon = pygame.image.load("FileGame/assets/icon.png")
pygame.display.set_icon(icon)


# Function to load high score from file
def load_high_score():  
    try:
        with open('high_score.txt', 'r') as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0

# Function to save high score to file  
def save_high_score(score):
    with open('high_score.txt', 'w') as file:
        file.write(str(int(score)))

# Function to draw the floor
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))

# Function to create pipes
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos))
    top_pipe_height = random.randint(700, 750)
    top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos - top_pipe_height))
    return bottom_pipe, top_pipe    

# Function to reset the game state
def reset_game():
    global bird_rect, bird_movement, score, pipe_list
    bird_rect = bird.get_rect(center = (100, 384))
    bird_movement = 0
    score = 0
    pipe_list.clear()
    return True

# Function to move pipes
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

# Function to draw pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

# Function to check collision between bird and pipes
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

# Function to rotate the bird sprite
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 2, 1)
    return new_bird

# Function to animate the bird
def bird_animation():
    new_bird = current_bird_color[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

# Function to display the score
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

# Load sound effects      
flap_sound = pygame.mixer.Sound(join("FileGame", "sound", "sfx_wing.wav"))
hit_sound = pygame.mixer.Sound(join("FileGame", "sound", "sfx_hit.wav"))
point_sound = pygame.mixer.Sound(join("FileGame", "sound", "sfx_point.wav"))
die_sound = pygame.mixer.Sound(join("FileGame", "sound", "sfx_die.wav"))
score_sound_countdown = 100

# Function to update high score
def update_high_score(score, high_score):
    score = int(score)
    if score > high_score:
        high_score = score
        save_high_score(high_score)
    return high_score

# Function to update score
def update_score(pipes, bird_rect):
    global score
    for pipe in pipes:
        if bird_rect.centerx > pipe.centerx and bird_rect.centerx <= pipe.centerx + 3:
            point_sound.play()
            score += 1/2

# Function to display high score menu
def display_high_score_menu():
    screen.blit(background, (0, 0))
    high_score_title = game_font.render("High Scores", True, (255, 255, 255))
    high_score_title_rect = high_score_title.get_rect(center=(216, 100))
    screen.blit(high_score_title, high_score_title_rect)
    
    top_1_font = game_font.render("Highest Score", True, (255, 255, 255))
    top_1_font_rect = top_1_font.get_rect(center = (216, 200))
    screen.blit(top_1_font, top_1_font_rect)

    high_score_value = game_font.render(str(high_score), True, (255, 255, 255))
    high_score_value_rect = high_score_value.get_rect(center=(216, 300))
    screen.blit(high_score_value, high_score_value_rect)

    back_button = game_font.render("Back", True, (255, 255, 255))
    back_button_rect = back_button.get_rect(center=(216, 500))
    screen.blit(back_button, back_button_rect)
    
    return back_button_rect

# Initialize game variables

high_score_menu = False
game_font = pygame.font.Font('FileGame/04B_19.TTF', 40)
high_score = 0
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
score = 0 
gravity = 0
bird_movement = 0
game_active = False
menu_state = True

#High score Menu
high_score_button = pygame.font.Font('FileGame/04B_19.TTF', 40).render("High Score", True, (255, 255, 255))
high_score_button_rect = high_score_button.get_rect(center=(216, 450))
high_score_button_frame = pygame.Rect(0, 0, high_score_button_rect.width + 20, high_score_button_rect.height + 10)
high_score_button_frame.center = high_score_button_rect.center

#Create Background
background = pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "background-night.png" )).convert())
#Create Floor
floor = pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "floor.png" )).convert())
floor_x_pos = 0

#Create Bird
blue_bird = [
    pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "bluebird-downflap.png")).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "bluebird-midflap.png")).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "bluebird-upflap.png")).convert_alpha())
]

yellow_bird = [
    pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "yellowbird-downflap.png")).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "yellowbird-midflap.png")).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "yellowbird-upflap.png")).convert_alpha())
]

red_bird = [
    pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "redbird-downflap.png")).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "redbird-midflap.png")).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "redbird-upflap.png")).convert_alpha())
]
current_bird_color = yellow_bird
bird_index = 0
bird = current_bird_color[0]
bird_rect = bird.get_rect(center = (100, 384))

bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)

#Game Over
game_over_surface = pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "gameover.png" )).convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216, 384))

#Create Pipe
pipe_surface = pygame.transform.scale2x(pygame.image.load(join("FileGame", "assets", "pipe-green.png" )).convert())
pipe_list = []
pipe_height = [200, 300, 400]


#Timer
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, 1200)

#Menu font
menu_surface = pygame.font.Font('FileGame/04B_19.TTF', 33).render("Please choose character", True, (255, 255, 255))
menu_rect = menu_surface.get_rect(center = (216, 250))

#Button to choose character
button_size = (80, 64)
character_button1 = pygame.transform.scale(pygame.image.load(join("FileGame", "assets", "bluebird-midflap.png")).convert_alpha(), button_size)
character_button1_rect = character_button1.get_rect(center = (100, 350))
character_button1_frame = pygame.Rect(0, 0, button_size[0] + 20, button_size[1] + 20)
character_button1_frame.center = character_button1_rect.center

character_button2 = pygame.transform.scale(pygame.image.load(join("FileGame", "assets", "yellowbird-midflap.png")).convert_alpha(), button_size)
character_button2_rect = character_button2.get_rect(center = (216, 350))
character_button2_frame = pygame.Rect(0, 0, button_size[0] + 20, button_size[1] + 20)
character_button2_frame.center = character_button2_rect.center

character_button3 = pygame.transform.scale(pygame.image.load(join("FileGame", "assets", "redbird-midflap.png")).convert_alpha(), button_size)
character_button3_rect = character_button3.get_rect(center = (332, 350))
character_button3_frame = pygame.Rect(0, 0, button_size[0] + 20, button_size[1] + 20)
character_button3_frame.center = character_button3_rect.center

#Back button from high score to menu
back_button = pygame.font.Font('FileGame/04B_19.TTF', 40).render("Back to Menu", True, (255, 255, 255))
back_button_rect = back_button.get_rect(center=(216, 500))
back_button_frame = pygame.Rect(0, 0, back_button_rect.width + 20, back_button_rect.height + 10)
back_button_frame.center = back_button_rect.center

#High score and play again inform
high_score = load_high_score()
play = pygame.font.Font('FileGame/04B_19.TTF', 40). render("Press Space to play", True, (255, 255, 255))
play_rect = play.get_rect(center = (216, 570))

# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        #Choose character
        if event.type == pygame.MOUSEBUTTONDOWN and menu_state:
            if character_button1_rect.collidepoint(event.pos):
                current_bird_color = blue_bird
                menu_state = False
                high_score_menu = False
                game_active = reset_game()
            elif character_button2_rect.collidepoint(event.pos):
                current_bird_color = yellow_bird
                menu_state = False
                high_score_menu = False
                game_active = reset_game()
            elif character_button3_rect.collidepoint(event.pos):
                current_bird_color = red_bird
                menu_state = False
                high_score_menu = False
                game_active = reset_game()
        #Quit Event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #Handle spacebar for flapping and restart game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and menu_state:
                current_bird_color = yellow_bird
                menu_state = False
                high_score_menu = False
                game_active = reset_game()
            if event.key == pygame.K_SPACE and game_active:
                gravity = 0.25
                bird_movement = 0
                bird_movement = - 8
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                gravity = 0
                menu_state = False
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0 
                score = 0
                bird_list = current_bird_color
        #Handle pipe spawn and bird animation
        if event.type == spawn_pipe and game_active:
            pipe_list.extend(create_pipe())
        if event.type == bird_flap:
            if bird_index <  2:
                bird_index += 1
            else:
                bird_index = 0
        bird, bird_rect = bird_animation() 
        #Back to menu from game over 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_active and back_button_rect.collidepoint(event.pos):
                gravity = 0
                menu_state = True
                game_active = False
                score = 0
                bird_rect.center = (100, 384)
                bird_movement = 0
                pipe_list.clear()
        #Update high score
        if event.type == pygame.MOUSEBUTTONDOWN and menu_state:
            if high_score_button_rect.collidepoint(event.pos):
                high_score_menu = True
                menu_state = False
    if not game_active:
        high_score = update_high_score(score, high_score)
    
    # Draw background
    screen.blit(background, (0, 0))
    
    # Draw menu items and handle character selection
    if menu_state:
        screen.blit(menu_surface, menu_rect)
        screen.blit(character_button1, character_button1_rect)
        screen.blit(character_button2, character_button2_rect)
        screen.blit(character_button3, character_button3_rect)
        
        pygame.draw.rect(screen, (255, 255, 255), character_button1_frame, 6)
        screen.blit(character_button1, character_button1_rect)
        
        pygame.draw.rect(screen, (255, 255, 255), character_button2_frame, 6)
        screen.blit(character_button2, character_button2_rect)
        
        pygame.draw.rect(screen, (255, 255, 255), character_button3_frame, 6)
        screen.blit(character_button3, character_button3_rect)
        
        screen.blit(high_score_button, high_score_button_rect)
        pygame.draw.rect(screen, (255, 255, 255), high_score_button_frame, 6)
        
        screen.blit(play, play_rect)
        
        draw_floor()
        if floor_x_pos <= -432:
            floor_x_pos = 0
        floor_x_pos -= 1
    
    # Display high score menu   
    elif high_score_menu:
        back_button_high_score_rect = display_high_score_menu()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button_high_score_rect.collidepoint(event.pos):
                high_score_menu = False
                menu_state = True
    
    # Update bird position, check collisions, move pipes, update score            
    elif game_active:        
        rotated_bird = rotate_bird(bird)
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
        
    # Display game over screen and options to restart or return to menu    
    else:
        pygame.draw.rect(screen, (255, 255, 255), back_button_frame, 2)
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_high_score(score, high_score)
        score_display('game_over')
        screen.blit(back_button, back_button_rect)
        screen.blit(play, play_rect)


    
    # Update display
    pygame.display.update()
    clock.tick(120)