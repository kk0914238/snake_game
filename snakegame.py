import pygame
import random
import pygame.mixer
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up the game window
width, height = 375, 812  # iPhone 14 Pro dimensions
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Define colors
background_color = (129, 145, 54)
snake_color = (0, 255, 0)
food_color = (255, 0, 0)
text_color = (0, 0, 0)
dot_color = (255, 0, 0)

# Define the snake's starting position and size
snake_head = [width // 2, height // 2]
snake_body = [[snake_head[0] - 10, snake_head[1]],
              [snake_head[0] - 20, snake_head[1]]]
snake_size = 10

# Define the initial movement direction of the snake
direction = "RIGHT"

# Create the food at a random position
food_position = [random.randrange(1, width // 10) * 10,
                 random.randrange(1, height // 10) * 10]

# Set up the game clock
clock = pygame.time.Clock()

# Set up the font for displaying the score and high score
font = pygame.font.Font(None, 36)
title_font = pygame.font.SysFont("arialblack", 36, True)
start_font = pygame.font.SysFont("bahnschriftsemiboldcondensed", 36, True)

# Initialize the score and high score
score = 0
high_score = 0

# Function to display the snake
def draw_snake():
    for segment in snake_body:
        pygame.draw.rect(window, snake_color, (segment[0], segment[1], snake_size, snake_size))

# Function to display the score and high score
def display_scores():
    score_text = font.render(f"Score: {score}", True, text_color)
    high_score_text = font.render(f"High Score: {high_score}", True, text_color)
    score_rect = score_text.get_rect(center=(width // 2, 20))
    high_score_rect = high_score_text.get_rect(center=(width // 2, 60))
    window.blit(score_text, score_rect)
    window.blit(high_score_text, high_score_rect)

# Function to reset the game state
def reset_game():
    global snake_head, snake_body, direction, food_position, score, high_score
    if score > high_score:
        high_score = score
    snake_head = [width // 2, height // 2]
    snake_body = [[snake_head[0] - 10, snake_head[1]],
                  [snake_head[0] - 20, snake_head[1]]]
    direction = "RIGHT"
    score = 0
    food_position = [random.randrange(1, width // 10) * 10,
                     random.randrange(1, height // 10) * 10]
    pygame.mixer.music.play(-1) #play the song on repeat

def show_menu_screen():
    display_menu = True
    start_text_timer = pygame.time.get_ticks()
    show_start_text = True

    # Load the soundtrack
    pygame.mixer.music.load(os.path.join(os.getcwd(), r"C:\Users\Sushil\Downloads\snakesound_menu.wav"))
    pygame.mixer.music.set_volume(0.5) #set the volume
    pygame.mixer.music.play(-1)  # -1 indicates infinite loop

    while display_menu:
        window.fill(background_color)

        # Display red dots
        for _ in range(75):
            dot_position = [random.randrange(0, width), random.randrange(0, height)]
            pygame.draw.circle(window, dot_color, dot_position, 2)

        title_text = title_font.render("SNAKE GAME", True, text_color)
        title_rect = title_text.get_rect(center=(width // 2, height // 2 - 50))
        window.blit(title_text, title_rect)

        current_time = pygame.time.get_ticks()
        if current_time - start_text_timer >= 1000:
            show_start_text = not show_start_text
            start_text_timer = current_time

        if show_start_text:
            start_text = start_font.render("CLICK ANYWHERE TO START", True, text_color)
            start_rect = start_text.get_rect(center=(width // 2, height // 2 + 50))
            window.blit(start_text, start_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()  # Stop the soundtrack
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                display_menu = False


# Main game loop
running = True
swipe_threshold = 100

show_menu_screen()

# Load the sound for when the snake eats the food
snake_eat_sound = pygame.mixer.Sound(r"C:\Users\Sushil\Downloads\snake_eat_food.wav")

pygame.mixer.music.play(-1)

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Change the direction of the snake with arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

        # Change the direction of the snake with touch input
        if event.type == pygame.FINGERMOTION:
            touch_pos = event.x * width, event.y * height
            touch_vector = pygame.math.Vector2(touch_pos) - pygame.math.Vector2(snake_head)
            if touch_vector.length() < swipe_threshold:
                continue  # Ignore small swipes
            x, y = touch_vector.normalize()
            if abs(x) > abs(y):
                if x > 0 and direction != "LEFT":  # Right swipe
                    direction = "RIGHT"
                elif x < 0 and direction != "RIGHT":  # Left swipe
                    direction = "LEFT"
            else:
                if y > 0 and direction != "UP":  # Down swipe
                    direction = "DOWN"
                elif y < 0 and direction != "DOWN":  # Up swipe
                    direction = "UP"

    # Move the snake
    if direction == "UP":
        snake_head[1] -= snake_size
    elif direction == "DOWN":
        snake_head[1] += snake_size
    elif direction == "LEFT":
        snake_head[0] -= snake_size
    elif direction == "RIGHT":
        snake_head[0] += snake_size

    # Check if the snake has collided with the food
    snake_head_rect = pygame.Rect(snake_head[0], snake_head[1], snake_size, snake_size)
    food_rect = pygame.Rect(food_position[0], food_position[1], snake_size, snake_size)

    if snake_head_rect.colliderect(food_rect):
        # Increase the length of the snake
        snake_body.append([])
        # Create a new food position
        food_position = [random.randrange(1, width // 10) * 10,
                         random.randrange(1, height // 10) * 10]
        # Increase the score
        score += 1

        # Play the snake eat sound
        snake_eat_sound.play()

    # Check if the snake has collided with the boundaries of the window
    if snake_head[0] < 0 or snake_head[0] >= width or snake_head[1] < 0 or snake_head[1] >= height:
        pygame.mixer.music.stop()  # Stop the soundtrack
        reset_game()

    # Check if the snake has collided with its own body
    for segment in snake_body:
        if snake_head == segment:
            pygame.mixer.music.stop()  # Stop the soundtrack
            reset_game()

    # Move the snake's body
    snake_body.insert(0, list(snake_head))
    if len(snake_body) > score + 1:
        snake_body.pop()

    # Fill the window with the background color
    window.fill(background_color)

    # Draw the snake and food
    draw_snake()
    pygame.draw.rect(window, food_color, (food_position[0], food_position[1], snake_size, snake_size))

    # Display the score and high score
    display_scores()

    # Update the game display
    pygame.display.update()

    # Set the frame rate
    clock.tick(30)

# Quit the game
pygame.quit()
