import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 300
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 60

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Runner Game")

# Player properties
player_x, player_y = 50, HEIGHT // 2
player_speed = 5
player_width, player_height = 30, 30

# Game variables
score = 0
game_over = False
level = None
input_mode = None  # Mouse or Keyboard

# Fonts
font = pygame.font.Font(None, 36)

# Function to spawn obstacles
def spawn_obstacle(level):
    obstacle_width = 20
    obstacle_x = WIDTH
    obstacle_speed = 5 if level == "medium" else 8

    if level == "medium":
        obstacle_height = random.randint(20, 80)
        obstacle_top = random.randint(0, HEIGHT - obstacle_height)
    elif level == "difficult":
        obstacle_height = random.randint(10, 30)
        obstacle_top = random.randint(0, HEIGHT - obstacle_height)

    return obstacle_x, obstacle_top, obstacle_width, obstacle_height, obstacle_speed

# Function to display level selection screen
def choose_level():
    screen.fill(WHITE)
    medium_text = font.render("Medium (Press 'M')", True, BLUE)  # Blue color
    difficult_text = font.render("Difficult (Press 'D')", True, BLUE)  # Blue color
    screen.blit(medium_text, (100, 100))
    screen.blit(difficult_text, (100, 150))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return "medium"
                elif event.key == pygame.K_d:
                    return "difficult"
                elif event.key == pygame.K_q:
                    pygame.quit()

# Function to display input mode selection screen
def choose_input_mode():
    screen.fill(WHITE)
    mouse_text = font.render("Mouse (Press 'M')", True, BLUE)  # Blue color
    keyboard_text = font.render("Keyboard (Press 'K')", True, BLUE)  # Blue color

    # Adjust the positioning of the text
    mouse_text_rect = mouse_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 25))
    keyboard_text_rect = keyboard_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 25))

    screen.blit(mouse_text, mouse_text_rect)
    screen.blit(keyboard_text, keyboard_text_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return "mouse"
                elif event.key == pygame.K_k:
                    return "keyboard"
                elif event.key == pygame.K_q:
                    pygame.quit()

# Function to save the player's score
def save_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

# Function to load the high score
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            high_score = int(file.read())
            return high_score
    except FileNotFoundError:
        return 0

# Initial level selection
level = choose_level()
input_mode = choose_input_mode()

# Load the high score
high_score = load_high_score()

while True:
    # Initialize obstacle variables
    obstacle_x, obstacle_top, obstacle_width, obstacle_height, obstacle_speed = spawn_obstacle(level)

    # Main game loop
    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        if input_mode == "keyboard":
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP] and player_y > 0:
                player_y -= player_speed
            if keys[pygame.K_DOWN] and player_y < HEIGHT - player_height:
                player_y += player_speed
        elif input_mode == "mouse":
            mouse_y = pygame.mouse.get_pos()[1]
            if 0 <= mouse_y <= HEIGHT - player_height:
                player_y = mouse_y

        # Move the obstacle
        obstacle_x -= obstacle_speed

        # Check for collision with the obstacle
        if (
            obstacle_x < player_x + player_width
            and obstacle_x + obstacle_width > player_x
            and player_y < obstacle_top + obstacle_height
            and player_y + player_height > obstacle_top
        ):
            game_over = True

        # Spawn a new obstacle when the current one goes off-screen
        if obstacle_x < 0:
            obstacle_x, obstacle_top, obstacle_width, obstacle_height, obstacle_speed = spawn_obstacle(level)
            score += 1

        # Draw everything
        screen.fill(WHITE)
        pygame.draw.rect(screen, RED, (obstacle_x, obstacle_top, obstacle_width, obstacle_height))
        pygame.draw.rect(screen, RED, (player_x, player_y, player_width, player_height))

        # Display score
        score_text = font.render(f"Score: {score}", True, RED)
        screen.blit(score_text, (10, 10))

        # Display high score
        high_score_text = font.render(f"High Score: {high_score}", True, RED)
        screen.blit(high_score_text, (10, 50))

        pygame.display.flip()
        clock.tick(FPS)

    # Update high score if necessary
    if score > high_score:
        high_score = score
        save_score(high_score)

    # Display game over screen and handle play again or exit
    choose_level_text = font.render("Choose Level (Press 'L')", True, BLUE)  # Blue color
    choose_input_mode_text = font.render("Choose Input Mode (Press 'I')", True, BLUE)  # Blue color
    play_again_text = font.render("Play Again (Press 'P')", True, BLUE)  # Blue color
    exit_text = font.render("Exit (Press 'Q')", True, BLUE)  # Blue color

    # Adjust the positioning of the text
    choose_level_text_rect = choose_level_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    choose_input_mode_text_rect = choose_input_mode_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    play_again_text_rect = play_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    exit_text_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))  # Increased space

    screen.blit(choose_level_text, choose_level_text_rect)
    screen.blit(choose_input_mode_text, choose_input_mode_text_rect)
    screen.blit(play_again_text, play_again_text_rect)
    screen.blit(exit_text, exit_text_rect)

    pygame.display.flip()

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_over = False
                    score = 0
                elif event.key == pygame.K_q:
                    pygame.quit()
                elif event.key == pygame.K_l:
                    level = choose_level()
                    game_over = False
                    score = 0
                elif event.key == pygame.K_i:
                    input_mode = choose_input_mode()
                    game_over = False
                    score = 0
