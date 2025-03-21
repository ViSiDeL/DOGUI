# Assisted by watsonx Code Assistant 
# The generated code is similar to code found in file https://github.com/Den1k22/python-lessons/blob/main/Code/pyGame/walking_sprite.py licensed under mit
import pygame
import sys

pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_SIZE = 20

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create the ball
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the state of the arrow keys
    keys = pygame.key.get_pressed()

    # Move the ball based on the arrow keys
    if keys[pygame.K_UP]:
        ball.move_ip(0, -1)
    if keys[pygame.K_DOWN]:
        ball.move_ip(0, 1)
    if keys[pygame.K_LEFT]:
        ball.move_ip(-1, 0)
    if keys[pygame.K_RIGHT]:
        ball.move_ip(1, 0)

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the ball
    pygame.draw.rect(screen, BLACK, ball)

    # Update the display
    pygame.display.flip()
