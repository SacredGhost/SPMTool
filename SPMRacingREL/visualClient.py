import pygame
import sys
import os
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_root, '..'))
from watches import *

# Global variables
FPS = 60

background = pygame.image.load(f"SPMRacingREL\graphics\placeholder.png")
SCREEN_WIDTH = background.get_width()
SCREEN_HEIGHT = background.get_height()
SCREEN_TITLE = "SPMRaceMod"
RADIUS = 5

mario_x = get_watch("Mario_X")
mario_y = get_watch("Mario_Y")
mario_z = get_watch("Mario_Z")
map = get_watch("CurrentMap")

current_map = ""

def get_currentstagemap():
    global current_map
    global stage_background
    new_map = map.read()

    if new_map != current_map:
        current_map = new_map
        stage_background = current_map

    return stage_background

stage_background = "placeholder"
current_background = "placeholder"

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    try:    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        stage_background = get_currentstagemap()

        if current_background != stage_background:
            try:
                background = pygame.image.load(f"SPMRacingREL\graphics\{stage_background}.png")
                current_background = stage_background
            except FileNotFoundError:
                stage_background = "placeholder"
                background = pygame.image.load(f"SPMRacingREL\graphics\{stage_background}.png")
                current_background = stage_background

        # Clear the screen
        screen.fill((0, 0, 0))

        # Update game logic here
        # Assuming you have correctly implemented the watches

        # Draw game elements here
        current_mario_x = int(mario_x.read())
        current_mario_y = int(mario_y.read())
        current_mario_z = int(mario_z.read())

        print(current_mario_x, current_mario_y, current_mario_z)

        screen.blit(background, (0, 0))  # Display the background image
        current_x = current_mario_x
        current_y = current_mario_y
        
        # Find the ratio of the image to position
        width_ratio = SCREEN_WIDTH / 4000
        height_ratio = SCREEN_HEIGHT / 2455

        current_x = current_x * width_ratio 
        current_y = current_y * height_ratio 

        # Reposition the graphic to the center of the screen
        current_x = SCREEN_WIDTH // 2 + current_x
        current_y = SCREEN_HEIGHT // 2 - current_y
        current_y += current_mario_z // 50

        pygame.draw.circle(screen, (255, 0, 0), (int(current_x), int(current_y) - RADIUS), RADIUS)

        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)
    except RuntimeError as e:
        print(e)
        while not dme.is_hooked():
            time.sleep(3)
            dme.hook()

# Quit Pygame
pygame.quit()
sys.exit()
