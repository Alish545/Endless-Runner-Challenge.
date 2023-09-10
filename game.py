import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 300
WHITE = (255, 255, 255)
RED = (255, 0, 0)
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
    medium_text = font.render("Medium (Press 'M')", True, RED)
    difficult_text = font.render("Difficult (Press 'D')", True, RED)
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

# Initial level selection
level = choose_level()

while True:
    # Initialize obstacle variables
    obstacle_x, obstacle_top, obstacle_width, obstacle_height, obstacle_speed = spawn_obstacle(level)

    # Main game loop
    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < HEIGHT - player_height:
            player_y += player_speed

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

        pygame.display.flip()
        clock.tick(FPS)

    # Display game over screen and handle play again or exit
    choose_level_text = font.render("Choose Level (Press 'L')", True, RED)
    play_again_text = font.render("Play Again (Press 'P')", True, RED)
    exit_text = font.render("Exit (Press 'Q')", True, RED)
    screen.blit(choose_level_text, (100, 100))
    screen.blit(play_again_text, (100, 150))
    screen.blit(exit_text, (100, 200))
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
