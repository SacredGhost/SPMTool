import pygame
import sys
from watches import *

# Global variables
FPS = 60

# Load the image
background = pygame.image.load("SPMRacingREL\graphics\R8PE01_2023-11-08_19-14-54.png")
SCREEN_WIDTH = background.get_width()
SCREEN_HEIGHT = background.get_height()
SCREEN_TITLE = "SPMRaceMod"
RADIUS = 5

mario_x = get_watch("Mario_X")
mario_y = get_watch("Mario_Y")
mario_z = get_watch("Mario_Z")

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

# Quit Pygame
pygame.quit()
sys.exit()
