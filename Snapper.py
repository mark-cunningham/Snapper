#!/usr/bin/python
# Snapper
# Code Angel

import sys
import os
import pygame
from pygame.locals import *
import random

# Define the colours
DARK_GREEN = (0, 98, 7)
DARK_GREY = (70, 70, 70)
WHITE = (255, 255, 255)

# Define constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCOREBOARD_HEIGHT = 24
SCOREBOARD_MARGIN = 4

# Camera viewfinder constants
CAM_LEFT_BORDER = 9
VIEWFINDER_WIDTH = 44
CAM_TOP_BORDER = 21
VIEWFINDER_HEIGHT = 30

GAME_LIVES = 3

# Setup
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snapper')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial Narrow Bold', 24)


# Load images
background_image = pygame.image.load('background.png').convert()
foreground_image = pygame.image.load('foreground.png').convert_alpha()
camera_image = pygame.image.load('camera.png').convert_alpha()
camera_flash_image = pygame.image.load('camera_flash.png').convert_alpha()
lives_image = pygame.image.load('camera_lives.png').convert_alpha()
snap_image = pygame.image.load('snap.png').convert_alpha()
miss_image = pygame.image.load('miss.png').convert_alpha()
rabbit_image = pygame.image.load('rabbit.png').convert_alpha()
owl_image = pygame.image.load('owl.png').convert_alpha()
deer_image = pygame.image.load('deer.png').convert_alpha()
squirrel_image = pygame.image.load('squirrel.png').convert_alpha()

# Load sounds
camera_sound = pygame.mixer.Sound('click.ogg')
miss_sound = pygame.mixer.Sound('miss.ogg')


def main():

    # Initialise variables
    mouse_button_pressed = False

    snap_visible = False
    miss_visible = False

    pygame.mouse.set_visible(False)

    animal_rect = pygame.Rect(0, 0, 0, 0)

    # Dictionary to store the animals
    animals = {
               'animal_1': {'type': 'rabbit', 'x_loc': 290, 'y_loc': 120, 'time': 60, 'points': 10},
               'animal_2': {'type': 'rabbit', 'x_loc': 382, 'y_loc': 318, 'time': 60, 'points': 10},
               'animal_3': {'type': 'rabbit', 'x_loc': 96, 'y_loc': 304, 'time': 60, 'points': 10},
               'animal_4': {'type': 'rabbit', 'x_loc': 358, 'y_loc': 159, 'time': 60, 'points': 10},
               'animal_5': {'type': 'rabbit', 'x_loc': 466, 'y_loc': 155, 'time': 60, 'points': 10},
               'animal_6': {'type': 'rabbit', 'x_loc': 202, 'y_loc': 297, 'time': 60, 'points': 10},
               'animal_7': {'type': 'rabbit', 'x_loc': 265, 'y_loc': 318, 'time': 60, 'points': 10},
               'animal_8': {'type': 'rabbit', 'x_loc': 367, 'y_loc': 344, 'time': 60, 'points': 10},
               'animal_9': {'type': 'owl', 'x_loc': 387, 'y_loc': 46, 'time': 75, 'points': 5},
               'animal_10': {'type': 'owl', 'x_loc': 295, 'y_loc': 47, 'time': 75, 'points': 5},
               'animal_11': {'type': 'owl', 'x_loc': 474, 'y_loc': 235, 'time': 75, 'points': 5},
               'animal_12': {'type': 'owl', 'x_loc': 574, 'y_loc': 132, 'time': 75, 'points': 5},
               'animal_13': {'type': 'owl', 'x_loc': 23, 'y_loc': 126, 'time': 75, 'points': 5},
               'animal_14': {'type': 'squirrel', 'x_loc': 17, 'y_loc': 113, 'time': 40, 'points': 20},
               'animal_15': {'type': 'squirrel', 'x_loc': 567, 'y_loc': 124, 'time': 40, 'points': 20},
               'animal_16': {'type': 'squirrel', 'x_loc': 448, 'y_loc': 278, 'time': 40, 'points': 20},
               'animal_17': {'type': 'squirrel', 'x_loc': 452, 'y_loc': 359, 'time': 40, 'points': 20},
               'animal_18': {'type': 'squirrel', 'x_loc': 304, 'y_loc': 301, 'time': 40, 'points': 20},
               'animal_19': {'type': 'squirrel', 'x_loc': 62, 'y_loc': 279, 'time': 40, 'points': 20},
               'animal_20': {'type': 'deer', 'x_loc': 106, 'y_loc': 87, 'time': 90, 'points': 1},
               'animal_21': {'type': 'deer', 'x_loc': 268, 'y_loc': 84, 'time': 90, 'points': 1},
               'animal_22': {'type': 'deer', 'x_loc': 302, 'y_loc': 90, 'time': 90, 'points': 1},
               'animal_23': {'type': 'deer', 'x_loc': 392, 'y_loc': 127, 'time': 90, 'points': 1}
    }

    animal = get_random_animal(animals)
    animal_timer = int(animal.get('time'))
    no_animal_timer = 0

    animal_visible = True

    score = 0
    lives = GAME_LIVES
    hi_score = 0

    # Main game loop
    while True:

        # Check for mouse and key presses
        for event in pygame.event.get():

            # Mouse button clicked
            mouse_button_pressed = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_button_pressed = True

            # Return key pressed when game over
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_RETURN] and lives == 0:
                if score > hi_score:
                    hi_score = score

                lives = GAME_LIVES
                score = 0

                animal = get_random_animal(animals)
                animal_timer = int(animal.get('time'))
                no_animal_timer = 0

                animal_visible = True

                snap_visible = False
                miss_visible = False

            # User quits
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Set the camera centre to the location of the mouse pointer
        mouse_pos = pygame.mouse.get_pos()

        camera_rect = camera_image.get_rect()
        camera_rect.centerx = mouse_pos[0]
        camera_rect.centery = mouse_pos[1]

        camera_width = camera_image.get_width()
        camera_height = camera_image.get_height()

        # Prevent the camera going off the screen
        if camera_rect.centerx < camera_width / 2:
            camera_rect.centerx = camera_width / 2
        if camera_rect.centerx > SCREEN_WIDTH - camera_width / 2:
            camera_rect.centerx = SCREEN_WIDTH - camera_width / 2

        if camera_rect.centery < camera_height / 2 + SCOREBOARD_HEIGHT:
            camera_rect.centery = camera_height / 2 + SCOREBOARD_HEIGHT
        if camera_rect.centery > SCREEN_HEIGHT - camera_height / 2:
            camera_rect.centery = SCREEN_HEIGHT - camera_height / 2

        # Calculate the camera's viewfinder rectangle
        viewfinder_left = camera_rect.left + CAM_LEFT_BORDER
        viewfinder_top = camera_rect.top + CAM_TOP_BORDER
        viewfinder_rect = pygame.Rect(viewfinder_left, viewfinder_top, VIEWFINDER_WIDTH, VIEWFINDER_HEIGHT)

        # If there is an animal visible, decrease the animal_timer and work out the animal rect
        if animal_visible is True:
            animal_timer -= 1

            # If the animal timer reaches zero, hide the animal and pause
            if animal_timer == 0:
                no_animal_timer = random.randint(30, 120)
                animal_visible = False

            animal_x = int(animal.get('x_loc'))
            animal_y = int(animal.get('y_loc'))

            if animal.get('type') == 'rabbit':
                animal_rect = pygame.Rect(animal_x, animal_y, rabbit_image.get_width(), rabbit_image.get_height())
            elif animal.get('type') == 'owl':
                animal_rect = pygame.Rect(animal_x, animal_y, owl_image.get_width(), owl_image.get_height())
            elif animal.get('type') == 'deer':
                animal_rect = pygame.Rect(animal_x, animal_y, deer_image.get_width(), deer_image.get_height())
            else:
                animal_rect = pygame.Rect(animal_x, animal_y, squirrel_image.get_width(), squirrel_image.get_height())

        # Countdown the no animal timer, and when it hits zero get a new animal
        if animal_visible is False:
            no_animal_timer -= 1

            if no_animal_timer == 0:
                if lives > 0:
                    animal = get_random_animal(animals)
                    animal_timer = int(animal.get('time'))
                    animal_visible = True

                snap_visible = False
                miss_visible = False

        # The player has clicked the mouse to take a photograph
        if mouse_button_pressed is True:
            if snap_visible is False and miss_visible is False and lives > 0:

                # Check to see whether they got the animal in the viewfinder, and that the animal is visible
                if viewfinder_rect.colliderect(animal_rect):
                    if animal_visible is True:
                        score += animal_timer * int(animal.get('points'))
                        snap_visible = True
                        camera_sound.play()

                    else:
                        miss_visible = True
                        lives -= 1
                        miss_sound.play()

                else:
                    miss_visible = True
                    lives -= 1
                    miss_sound.play()

                # Hide the animal and pause
                animal_visible = False
                animal_timer = 0
                no_animal_timer = 120

        # Draw background
        game_screen.blit(background_image, [0, 0])

        # If there is an animal visible, draw animal
        if animal_visible is True:
            animal_x = int(animal.get('x_loc'))
            animal_y = int(animal.get('y_loc'))

            # Blit the correct animal onto the screen on top of background but below foreground
            if animal.get('type') == 'rabbit':
                game_screen.blit(rabbit_image, [animal_x, animal_y])
            elif animal.get('type') == 'owl':
                game_screen.blit(owl_image, [animal_x, animal_y])
            elif animal.get('type') == 'deer':
                game_screen.blit(deer_image, [animal_x, animal_y])
            else:
                game_screen.blit(squirrel_image, [animal_x, animal_y])

        # Draw the foreground overlay image
        game_screen.blit(foreground_image, [0, 0])

        # Draw Camera
        if snap_visible is True or miss_visible is True:
            game_screen.blit(camera_flash_image, camera_rect)
        else:
            game_screen.blit(camera_image, camera_rect)

        # Draw the snap or miss image
        snap_or_miss_border = (VIEWFINDER_WIDTH - snap_image.get_width()) / 2
        snap_or_miss_rect = pygame.Rect(viewfinder_left + snap_or_miss_border, viewfinder_top,
                                        snap_image.get_width(), snap_image.get_height())

        if snap_visible is True:
            game_screen.blit(snap_image, snap_or_miss_rect)
        elif miss_visible is True:
            game_screen.blit(miss_image, snap_or_miss_rect)

        # Display score board
        score_text = 'Score: ' + str(score)
        display_scoreboard_data(score_text, 'Left')

        hi_score_text = 'Hi: ' + str(hi_score)
        display_scoreboard_data(hi_score_text, 'Centre')

        # Display the lives remeaining
        for life in range(1, lives + 1):
            life_xloc = SCREEN_WIDTH - life * (lives_image.get_width() + 2 * SCOREBOARD_MARGIN)
            life_y_loc = SCREEN_HEIGHT - SCOREBOARD_HEIGHT
            game_screen.blit(lives_image, [life_xloc, life_y_loc])

        if lives == 0:
            display_game_over()

        pygame.display.update()
        clock.tick(60)


# Get a random animal from the dictionary
def get_random_animal(animals):
    random_animal = random.choice(list(animals.keys()))
    return animals.get(random_animal)


# Handle the text display
def display_scoreboard_data(scoreboard_text, alignment):
    display_text = font.render(scoreboard_text, True, WHITE)
    text_rect = display_text.get_rect()

    text_loc = [0, 0]

    if alignment == 'Left':
        text_loc = [SCOREBOARD_MARGIN, SCREEN_HEIGHT - SCOREBOARD_HEIGHT]

    elif alignment == 'Centre':
        text_loc = [(SCREEN_WIDTH - text_rect.width) / 2, SCREEN_HEIGHT - SCOREBOARD_HEIGHT]

    game_screen.blit(display_text, text_loc)


# Display end of game message
def display_game_over():

    game_over_rect = (3 * SCOREBOARD_HEIGHT, 8 * SCOREBOARD_HEIGHT,
                      SCREEN_WIDTH - SCOREBOARD_HEIGHT * 6, SCOREBOARD_HEIGHT * 5)

    pygame.draw.rect(game_screen, DARK_GREEN, game_over_rect)

    text_line_1 = font.render('GAME OVER', True, WHITE)
    text_rect_1 = text_line_1.get_rect()
    text_line_1_loc = [(SCREEN_WIDTH - text_rect_1.width) / 2, (SCREEN_HEIGHT / 2) - 16]

    text_line_2 = font.render('Hit RETURN for a new game', True, WHITE)
    text_rect_2 = text_line_2.get_rect()
    text_line_2_loc = [(SCREEN_WIDTH - text_rect_2.width) / 2, (SCREEN_HEIGHT / 2) + 16]

    game_screen.blit(text_line_1, text_line_1_loc)
    game_screen.blit(text_line_2, text_line_2_loc)


if __name__ == '__main__':
    main()
