import pygame
import sys

# Global variables
FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "SPMRaceMod"

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

# Load the image
background = pygame.image.load('SPMRacingREL/graphics/4-1_Chapter_4.png')

# Get the image's rect (rectangle)
background_rect = background.get_rect()

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

    # Draw game elements here

    screen.blit(background, background_rect)

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
