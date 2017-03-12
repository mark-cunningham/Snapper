# Snapper

import pygame, sys
from pygame.locals import *
import random

# Define the colours
DARKGREEN = (0, 98, 7)
YELLOW = (252, 225, 120)

# Define constants
SCREENWIDTH = 640
SCREENHEIGHT = 480

SCOREBOARDHEIGHT = 24
SCOREBOARDMARGIN = 4

# Camera viewer borders - these need to change if the graphic is changed
CAMLEFTBORDER = 7
VIEWFINDERWIDTH = 47
CAMTOPBORDER = 34
VIEWFINDERHEIGHT = 33

GAMELIVES = 3


# Setup
pygame.init()
game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Snapper")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Helvetica", 16)

def main():
    # Load images
    background_image = pygame.image.load("background.png").convert()
    foreground_image = pygame.image.load("foreground.png").convert()
    camera_image = pygame.image.load("camera.png").convert()
    lives_image = pygame.image.load("camera_lives.png").convert()
    snap_image = pygame.image.load("snap.png").convert()
    miss_image = pygame.image.load("miss.png").convert()
    rabbit_image = pygame.image.load("rabbit.png").convert()
    owl_image = pygame.image.load("owl.png").convert()
    moose_image = pygame.image.load("moose.png").convert()
    squirrel_image = pygame.image.load("squirrel.png").convert()


    # Initialise variables

    mouse_button_pressed = False

    rabbit_width = rabbit_image.get_width()
    rabbit_height = rabbit_image.get_height()
    owl_width = owl_image.get_width()
    owl_height = owl_image.get_height()
    moose_width = moose_image.get_width()
    moose_height = moose_image.get_height()
    squirrel_width = squirrel_image.get_width()
    squirrel_height = squirrel_image.get_height()

    snap_miss_width = snap_image.get_width()
    snap_miss_height = snap_image.get_height()
    snap_miss_border = (VIEWFINDERWIDTH - snap_miss_width) / 2

    lives_width = lives_image.get_width()

    camera_width = camera_image.get_width()
    camera_height = camera_image.get_height()

    animal_rect = pygame.Rect(0, 0, 0, 0)

    snap_visible = False
    miss_visible = False


    pygame.mouse.set_visible(False)

    animals = [['rabbit', [292, 197]],
               ['rabbit', [106, 189]],
               ['rabbit', [30, 198]],
               ['rabbit', [23, 155]],
               ['rabbit', [169, 218]],
               ['rabbit', [122, 264]],
               ['rabbit', [376, 196]],
               ['rabbit', [544, 186]],
               ['rabbit', [535, 250]],
               ['rabbit', [287, 293]],
               ['rabbit', [378, 297]],
               ['rabbit', [615, 238]],
               ['rabbit', [591, 150]],
               ['owl', [207, 99]],
               ['owl', [544, 113]],
               ['owl', [223, 45]],
               ['owl', [530, 49]],
               ['owl', [585, 31]],
               ['owl', [296, 35]],
               ['moose', [148, 136]],
               ['moose', [508, 122]],
               ['squirrel', [181, 330]],
               ['squirrel', [321, 322]],
               ['squirrel', [392, 288]],
               ['squirrel', [41, 284]],
               ['squirrel', [239, 344]]]

    random_animal = random.choice(animals)
    animal_type = random_animal[0]
    animal_location = random_animal[1]
    animal_x = animal_location[0]
    animal_y = animal_location[1]


    no_animal_timer = 0

    times_dict = {'rabbit': 60, 'owl': 70, 'moose': 90, 'squirrel': 40}
    score_boost_dict = {'rabbit': 10, 'owl': 5, 'moose': 1, 'squirrel': 25}
    animal_timer = times_dict[animal_type]


    animal_visible = True

    score = 0
    lives = GAMELIVES
    hi_score = 0


    while True: # main game loop

        # Keypress events
        for event in pygame.event.get():


            mouse_button_pressed = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_button_pressed = True

            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_RETURN]:
                if score > hi_score:
                    hi_score = score

                lives = GAMELIVES
                score = 0

                random_animal = random.choice(animals)
                animal_type = random_animal[0]
                animal_location = random_animal[1]
                animal_x = animal_location[0]
                animal_y = animal_location[1]

                animal_timer = times_dict[animal_type]





            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        mouse_pos = pygame.mouse.get_pos()
        camera_rect = camera_image.get_rect()

        camera_rect.centerx = mouse_pos[0]
        camera_rect.centery = mouse_pos[1]

        if camera_rect.centerx < camera_width / 2:
            camera_rect.centerx = camera_width / 2
        if camera_rect.centerx > SCREENWIDTH - camera_width / 2:
            camera_rect.centerx = SCREENWIDTH - camera_width / 2

        if camera_rect.centery < camera_height / 2 + SCOREBOARDHEIGHT:
            camera_rect.centery = camera_height / 2 + SCOREBOARDHEIGHT
        if camera_rect.centery > SCREENHEIGHT - camera_height / 2:
            camera_rect.centery = SCREENHEIGHT - camera_height / 2


        viewfinder_left = camera_rect.left + CAMLEFTBORDER
        viewfinder_top = camera_rect.top + CAMTOPBORDER

        viewfinder_rect = pygame.Rect(viewfinder_left, viewfinder_top, VIEWFINDERWIDTH, VIEWFINDERHEIGHT)
        snap_miss_rect = pygame.Rect(viewfinder_left + snap_miss_border, viewfinder_top, snap_miss_width, snap_miss_height)



        # Draw background
        scoreboard_rect = (0, 0, SCREENWIDTH, SCOREBOARDHEIGHT + 1)
        pygame.draw.rect(game_screen, DARKGREEN, scoreboard_rect)
        game_screen.blit(background_image, [0, SCOREBOARDHEIGHT])

        if animal_timer > 0:
            if animal_type == "rabbit":
                game_screen.blit(rabbit_image, animal_location)
                animal_rect = pygame.Rect(animal_x, animal_y, rabbit_width, rabbit_height)
            elif animal_type == "owl":
                game_screen.blit(owl_image, animal_location)
                animal_rect = pygame.Rect(animal_x, animal_y, owl_width, owl_height)
            elif animal_type == "moose":
                game_screen.blit(moose_image, animal_location)
                animal_rect = pygame.Rect(animal_x, animal_y, moose_width, moose_height)
            elif animal_type == "squirrel":
                game_screen.blit(squirrel_image, animal_location)
                animal_rect = pygame.Rect(animal_x, animal_y, squirrel_width, squirrel_height)

            animal_timer -= 1

            if animal_timer == 0:
                no_animal_timer = random.randint(20, 120)
                animal_visible = False


        if no_animal_timer > 0:
            no_animal_timer -= 1

            if no_animal_timer == 0:
                if lives > 0:
                    random_animal = random.choice(animals)
                    animal_type = random_animal[0]
                    animal_location = random_animal[1]
                    animal_x = animal_location[0]
                    animal_y = animal_location[1]

                    animal_timer = times_dict[animal_type]
                    animal_visible = True

                snap_visible = False
                miss_visible = False





        game_screen.blit(foreground_image, [0, SCOREBOARDHEIGHT + 1])

        if mouse_button_pressed is True and lives > 0:
            if snap_visible is False and miss_visible is False:
                if viewfinder_rect.colliderect(animal_rect):
                    if animal_visible is True:
                        snap_visible = True
                        score += animal_timer * score_boost_dict[animal_type]
                    else:
                        miss_visible = True
                        lives -= 1

                else:
                    miss_visible = True
                    lives -= 1

                animal_visible = False
                animal_timer = 0
                no_animal_timer = 120


        # Draw Camera
        game_screen.blit(camera_image, camera_rect)

        if snap_visible is True:
            game_screen.blit(snap_image, snap_miss_rect)
        elif miss_visible is True:
            game_screen.blit(miss_image, snap_miss_rect)

        # Display score board
        score_text = "Score: " + str(score)
        display_scoreboard_data(score_text, "Left")

        hi_score_text = "Hi: " + str(hi_score)
        display_scoreboard_data(hi_score_text, "Centre")

        for life in range(1, lives + 1):
            game_screen.blit(lives_image, [SCREENWIDTH - life * (lives_width + 2 * SCOREBOARDMARGIN),  SCOREBOARDMARGIN])

        if lives == 0:
            display_game_over()



        pygame.display.update()
        clock.tick(60)

def display_scoreboard_data(scoreboard_text, alignment):
    display_text = font.render(scoreboard_text, True, YELLOW)
    text_rect = display_text.get_rect()

    text_loc = [0, 0]

    if alignment == "Left":
        text_loc = [SCOREBOARDMARGIN, SCOREBOARDMARGIN]

    elif alignment == "Centre":
        text_loc = [(SCREENWIDTH - text_rect.width) / 2, SCOREBOARDMARGIN]

    game_screen.blit(display_text, text_loc)

def display_game_over():
    game_over_rect  = (3 * SCOREBOARDHEIGHT, 8 * SCOREBOARDHEIGHT, SCREENWIDTH - SCOREBOARDHEIGHT * 6, SCOREBOARDHEIGHT * 5)
    pygame.draw.rect(game_screen, DARKGREEN, game_over_rect)

    text_line_1 = font.render("GAME OVER", True, YELLOW)
    text_rect_1 = text_line_1.get_rect()
    text_line_1_loc = [(SCREENWIDTH - text_rect_1.width) / 2, (SCREENHEIGHT / 2) - 16]

    text_line_2 = font.render("Hit RETURN for new game", True, YELLOW)
    text_rect_2 = text_line_2.get_rect()
    text_line_2_loc = [(SCREENWIDTH - text_rect_2.width) / 2, (SCREENHEIGHT / 2) + 16]

    game_screen.blit(text_line_1, text_line_1_loc)
    game_screen.blit(text_line_2, text_line_2_loc)




if __name__ == "__main__":
    main()




