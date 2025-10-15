import pygame
import random
import sys

pygame.init()

# --- Screen settings ---
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Formula Racing Game with Flowers")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)
GREEN = (34, 139, 34)
GRAY = (169, 169, 169)
PINK = (255, 105, 180)
PURPLE = (160, 32, 240)
ORANGE = (255, 140, 0)
COLORS = [RED, YELLOW, WHITE]

# --- Clock ---
clock = pygame.time.Clock()
FPS = 60

# --- Car settings ---
CAR_WIDTH = 40
CAR_HEIGHT = 80
player_x = 230
player_y = SCREEN_HEIGHT - CAR_HEIGHT - 20
car_speed = 5

# AI Cars
ai_cars = [
    {"color": RED, "x": 120, "y": -150},
    {"color": YELLOW, "x": 320, "y": -300}
]
ai_speed = 4

# Game variables
score = 0
game_over = False
player_color = BLUE

# Fonts
font = pygame.font.SysFont(None, 40)
countdown_font = pygame.font.SysFont(None, 100)

# --- Functions --- #
def quit_game():
    pygame.quit()
    sys.exit()

def draw_car(x, y, color):
    """Draw a stylish car without wheels, with glasses."""
    # Car body
    pygame.draw.rect(screen, color, (x, y, CAR_WIDTH, CAR_HEIGHT))
    # Car roof/polygon
    pygame.draw.polygon(screen, color, [
        (x + 5, y), (x + CAR_WIDTH - 5, y),
        (x + CAR_WIDTH - 15, y + 20), (x + 15, y + 20)
    ])
    # Windows
    pygame.draw.rect(screen, (135, 206, 235), (x + 10, y + 5, CAR_WIDTH - 20, 15))
    pygame.draw.rect(screen, (135, 206, 235), (x + 10, y + 25, CAR_WIDTH - 20, 20))
    # Glasses effect (shiny windshield)
    pygame.draw.rect(screen, WHITE, (x + 12, y + 8, CAR_WIDTH - 24, 10))
    # Mirrors
    pygame.draw.rect(screen, color, (x - 5, y + 20, 5, 10))
    pygame.draw.rect(screen, color, (x + CAR_WIDTH, y + 20, 5, 10))
    # Roof line
    pygame.draw.rect(screen, BLACK, (x + 10, y, CAR_WIDTH - 20, 5))

def draw_flower(x, y):
    """Draw a simple flower."""
    pygame.draw.circle(screen, PINK, (x, y), 5)
    pygame.draw.circle(screen, PURPLE, (x - 5, y), 3)
    pygame.draw.circle(screen, PURPLE, (x + 5, y), 3)
    pygame.draw.circle(screen, PURPLE, (x, y - 5), 3)
    pygame.draw.circle(screen, PURPLE, (x, y + 5), 3)

def draw_track():
    screen.fill(GREEN)
    # Road
    pygame.draw.rect(screen, GRAY, (100, 0, 300, SCREEN_HEIGHT))
    for i in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.line(screen, WHITE, (250, i), (250, i + 20), 5)
    # Flowers on left and right side
    for i in range(0, SCREEN_HEIGHT, 60):
        draw_flower(50, i + 30)
        draw_flower(450, i + 10)

def move_ai_cars():
    global score, game_over
    for car in ai_cars:
        car["y"] += ai_speed
        if car["y"] > SCREEN_HEIGHT:
            car["y"] = -random.randint(100, 300)
            car["x"] = random.choice([120, 230, 320])
            score += 1
        # Collision detection
        if (player_x < car["x"] + CAR_WIDTH and
            player_x + CAR_WIDTH > car["x"] and
            player_y < car["y"] + CAR_HEIGHT and
            player_y + CAR_HEIGHT > car["y"]):
            game_over = True

def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))
    msg = font.render(text, True, WHITE)
    screen.blit(msg, (x + (w - msg.get_width()) // 2, y + (h - msg.get_height()) // 2))

def move_left():
    global player_x
    if player_x > 110:
        player_x -= car_speed

def move_right():
    global player_x
    if player_x < 350:
        player_x += car_speed

def draw_buttons():
    draw_button("Left", 50, SCREEN_HEIGHT - 60, 80, 40, BLUE, (0, 255, 255), action=move_left)
    draw_button("Right", 370, SCREEN_HEIGHT - 60, 80, 40, BLUE, (0, 255, 255), action=move_right)
    draw_button("Quit", 200, SCREEN_HEIGHT - 60, 100, 40, RED, (255, 100, 100), action=quit_game)

def start_countdown():
    for i in range(3, 0, -1):
        screen.fill(GREEN)
        draw_track()
        color = random.choice(COLORS)
        countdown_text = countdown_font.render(str(i), True, color)
        screen.blit(countdown_text, (SCREEN_WIDTH // 2 - countdown_text.get_width() // 2,
                                     SCREEN_HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(800)
        screen.fill(GREEN)
        draw_track()
        pygame.display.update()
        pygame.time.delay(200)
    for _ in range(3):
        screen.fill(GREEN)
        draw_track()
        go_color = random.choice(COLORS)
        go_text = countdown_font.render("GO!", True, go_color)
        screen.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2,
                              SCREEN_HEIGHT // 2 - go_text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(300)
        screen.fill(GREEN)
        draw_track()
        pygame.display.update()
        pygame.time.delay(200)

def game_over_screen():
    global game_over, score
    while True:
        screen.fill(BLACK)
        over_text = font.render("Game Over!", True, RED)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, 200))
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 250))
        draw_button("Restart", 150, 350, 80, 40, GREEN, (0, 255, 0), action=restart_game)
        draw_button("Quit", 270, 350, 80, 40, RED, (255, 100, 100), action=quit_game)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

def restart_game():
    global player_x, player_y, ai_cars, score, game_over
    player_x = 230
    player_y = SCREEN_HEIGHT - CAR_HEIGHT - 20
    ai_cars = [
        {"color": RED, "x": 120, "y": -150},
        {"color": YELLOW, "x": 320, "y": -300}
    ]
    score = 0
    game_over = False
    game_loop()

def game_loop():
    global game_over
    start_countdown()
    while True:
        draw_track()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            move_left()
        if keys[pygame.K_RIGHT]:
            move_right()
        draw_car(player_x, player_y, player_color)
        for car in ai_cars:
            draw_car(car["x"], car["y"], car["color"])
        move_ai_cars()
        draw_buttons()
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        if game_over:
            game_over_screen()
        pygame.display.update()
        clock.tick(FPS)

# --- Start the game ---
game_loop()
