import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the Display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Space Invaders')

# Define colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# SpaceShip Settings
spaceship_width = 60
spaceship_height = 40
spaceship_x = width // 2 - spaceship_width // 2
spaceship_y = height - spaceship_height - 10
spaceship_speed = 5

def draw_spaceship(surface, x, y):
    # Main body
    pygame.draw.polygon(surface, GREEN, [
        (x + spaceship_width // 2, y),
        (x + spaceship_width, y + spaceship_height),
        (x, y + spaceship_height)
    ])
    # Cockpit
    pygame.draw.polygon(surface, BLUE, [
        (x + spaceship_width // 2, y + 5),
        (x + spaceship_width // 2 + 10, y + spaceship_height - 10),
        (x + spaceship_width // 2 - 10, y + spaceship_height - 10)
    ])
    # Left wing
    pygame.draw.polygon(surface, RED, [
        (x, y + spaceship_height),
        (x - 10, y + spaceship_height + 10),
        (x + 10, y + spaceship_height)
    ])
    # Right wing
    pygame.draw.polygon(surface, RED, [
        (x + spaceship_width, y + spaceship_height),
        (x + spaceship_width - 10, y + spaceship_height + 10),
        (x + spaceship_width + 10, y + spaceship_height)
    ])

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key press handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and spaceship_x - spaceship_speed > 0:
            spaceship_x -= spaceship_speed
        if keys[pygame.K_RIGHT] and spaceship_x + spaceship_speed < width - spaceship_width:
            spaceship_x += spaceship_speed

        # Fill in the background
        window.fill(BLACK)

        # Draw the Spaceship
        draw_spaceship(window, spaceship_x, spaceship_y)
        # pygame.draw.rect(window, GREEN, (spaceship_x, spaceship_y, spaceship_width, spaceship_height))

        # Update the Display
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(60)

# Quit pygame
pygame.quit()
sys.exit()
