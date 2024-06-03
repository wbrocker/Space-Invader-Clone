import pygame
import sys
import random

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
YELLOW = (255, 255, 0)
ENEMY_COLOR = (255, 165, 0) # Orange

# SpaceShip Settings
spaceship_width = 60
spaceship_height = 40
spaceship_x = width // 2 - spaceship_width // 2
spaceship_y = height - spaceship_height - 10
spaceship_speed = 5

# Bullet Settings
bullet_width = 3
bullet_height = 7
bullet_speed = 7
bullet_cooldown = 200  # Milliseconds
last_shot_time = 0

# Enemy Settings
enemy_width = 50
enemy_height = 30
enemy_speed = 2
enemy_bomb_cooldown = 1000 # Milliseconds.


# Game Settings
lives = 3
score = 0

# Font Settings
font = pygame.font.Font(None, 36)


# Bullet Class
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.y -= bullet_speed

    def draw(self, surface):
        pygame.draw.ellipse(surface, YELLOW, (self.x, self.y, bullet_width, bullet_height))
        # pygame.draw.rect(surface, WHITE, (self.x, self.y, bullet_width, bullet_height))


# Bomb Class
class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.y -= bullet_speed

    def draw(self, surface):
        pygame.draw.ellipse(surface, RED, (self.x, self.y, bullet_width, bullet_height))


# Enemy Class
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 1      # 1: Right, -1: Left
        self.last_bomb_time = pygame.time.get_ticks()

    def move(self):
        self.x += enemy_speed * self.direction
        if self.x < 0 or self.x >= width - enemy_width:
            self.direction *= -1
            self.y += enemy_height

    def draw(self, surface):
        pygame.draw.rect(surface, ENEMY_COLOR, (self.x, self.y, bullet_width, bullet_height))

    def drop_bomb(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bomb_time > enemy_bomb_cooldown:
            self.last_bomb_time = current_time
            return Bomb(self.x + enemy_width //2, self.y + enemy_height)
        return None

# List to store bullets
bullets = []
bombs = []

# List to store enemies
enemies = []

# Function to create enemies
def create_enemies(rows, cols):
    for row in range(rows):
        for col in range(cols):
            enemy_x = col * (enemy_width + 10) + 50
            enemy_y = row * (enemy_height + 10) + 50
            enemies.append(Enemy(enemy_x, enemy_y))


# Create a grid of enemies
create_enemies(3, 10)


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


def draw_text(surface, text, font, x, y):
    text_obj = font.render(text, True, WHITE)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


# Main game loop
running = True

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key press handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spaceship_x - spaceship_speed > 0:
        spaceship_x -= spaceship_speed
    if keys[pygame.K_RIGHT] and spaceship_x + spaceship_speed < width - spaceship_width:
        spaceship_x += spaceship_speed
    if keys[pygame.K_SPACE] and current_time - last_shot_time > bullet_cooldown:
        bullet_x = spaceship_x + spaceship_width // 2 - bullet_width // 2
        bullet_y = spaceship_y
        bullets.append(Bullet(bullet_x, bullet_y))
        last_shot_time = current_time

    if keys[pygame.K_q]:  # Quit the game.
        running = False

    # Move Bullets
    for bullet in bullets:
        bullet.move()

    # Remove bullets that have moved off the screen
    bullets = [bullet for bullet in bullets if bullet.y > 0]

    # Move Enemies
    for enemy in enemies:
        enemy.move()
        bomb = enemy.drop_bomb()
        if bomb:
            bombs.append(bomb)

    # Move Bombs
    for bomb in bombs:
        bomb.move()

    # Remove bomb if it goes off screen
    bombs = [bomb for bomb in bombs if bomb.y < height]

    # Fill in the background
    window.fill(BLACK)

    # Draw the Spaceship
    draw_spaceship(window, spaceship_x, spaceship_y)
    # pygame.draw.rect(window, GREEN, (spaceship_x, spaceship_y, spaceship_width, spaceship_height))

    # Draw bullets
    for bullet in bullets:
        bullet.draw(window)

    # Draw bombs
    for bomb in bombs:
        bomb.draw(window)

    # Draw Enemies
    for enemy in enemies:
        enemy.draw(window)

    # Draw lives and score
    draw_text(window, f'Lives: {lives}', font, 10, 10)
    draw_text(window, f'Score: {score}', font, width - 120, 10)

    # Draw horizontal line below the text
    pygame.draw.line(window, WHITE, (0, 50), (width, 50), 2)

    # Update the Display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit pygame
pygame.quit()
sys.exit()
