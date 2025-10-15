import pygame
import random
import sys
import time

pygame.init()

# --- Screen settings ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Real Flight Shooting Game")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 60, 60)
GREEN = (0, 255, 120)
BLUE = (60, 160, 255)
YELLOW = (255, 230, 80)
ORANGE = (255, 150, 0)
PURPLE = (180, 80, 255)
GRAY = (20, 20, 30)

# --- Game clock ---
clock = pygame.time.Clock()
FPS = 60

# --- Star class for background ---
class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.randint(1, 4)

    def move(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.size)

# --- Flight class ---
class Flight:
    def __init__(self):
        self.image = pygame.Surface((80, 80), pygame.SRCALPHA)
        self.color = random.choice([BLUE, GREEN, YELLOW, ORANGE, PURPLE])
        self.draw_flight()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120))
        self.speed = 6
        self.bullets = []
        self.shoot_timer = 0  # auto-shoot timer
        self.powered_up = False
        self.power_timer = 0

    def draw_flight(self):
        pygame.draw.polygon(
            self.image, self.color,
            [(40, 0), (20, 25), (10, 70), (40, 50), (70, 70), (60, 25)]
        )
        pygame.draw.line(self.image, WHITE, (40, 0), (40, 80), 2)

    def move_left(self):
        if self.rect.left > 0:
            self.rect.x -= self.speed

    def move_right(self):
        if self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def auto_shoot(self):
        self.shoot_timer += 1
        interval = 8 if self.powered_up else 15  # faster shooting with power-up
        if self.shoot_timer >= interval:
            bullet = pygame.Rect(self.rect.centerx - 3, self.rect.top, 6, 15)
            self.bullets.append(bullet)
            self.shoot_timer = 0

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.y -= 10
            if bullet.y < 0:
                self.bullets.remove(bullet)

    def draw(self):
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            pygame.draw.rect(screen, YELLOW, bullet)

# --- Enemy class ---
class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - 40), -40, 40, 40)
        self.color = random.choice([RED, ORANGE, PURPLE])
        self.speed = random.randint(2, 5)

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# --- PowerUp class ---
class PowerUp:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(50, SCREEN_WIDTH - 50), -40, 30, 30)
        self.color = random.choice([GREEN, BLUE, ORANGE])
        self.speed = 3
        self.type = random.choice(['fast_shoot', 'extra_points'])

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 20)
        text = "F" if self.type == 'fast_shoot' else "+"
        screen.blit(font.render(text, True, WHITE), (self.rect.x+6, self.rect.y+4))

# --- Button class ---
class Button:
    def __init__(self, x, y, w, h, text, color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color

    def draw(self):
        mouse = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse) else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=12)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False

# --- Countdown ---
def countdown():
    font = pygame.font.Font(None, 100)
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        text = font.render(str(i), True, YELLOW)
        screen.blit(text, (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()
        time.sleep(1)

# --- Game Over screen ---
def game_over_screen(score):
    restart_button = Button(200, 400, 200, 60, "Restart", BLUE, GREEN)
    quit_button = Button(200, 500, 200, 60, "Quit", RED, ORANGE)
    font_title = pygame.font.Font(None, 60)
    font_score = pygame.font.Font(None, 40)
    running = True

    while running:
        screen.fill(BLACK)
        title_text = font_title.render("💥 GAME OVER 💥", True, RED)
        score_text = font_score.render(f"Your Score: {score}", True, WHITE)
        screen.blit(title_text, (120, 200))
        screen.blit(score_text, (200, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if restart_button.is_clicked(event):
                main_game()
                return
            if quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

        restart_button.draw()
        quit_button.draw()

        pygame.display.flip()
        clock.tick(60)

# --- Main Game ---
def main_game():
    flight = Flight()
    enemies = []
    stars = [Star() for _ in range(80)]
    powerups = []
    score = 0
    font = pygame.font.Font(None, 36)

    left_button = Button(60, 600, 100, 50, "◀ LEFT", BLUE, GREEN)
    right_button = Button(440, 600, 100, 50, "RIGHT ▶", BLUE, GREEN)

    countdown()
    running = True

    while running:
        screen.fill(GRAY)

        # Stars
        for star in stars:
            star.move()
            star.draw()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if left_button.is_clicked(event):
                flight.move_left()
            if right_button.is_clicked(event):
                flight.move_right()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            flight.move_left()
        if keys[pygame.K_RIGHT]:
            flight.move_right()

        # Automatic shooting
        flight.auto_shoot()
        flight.update_bullets()

        # Spawn enemies
        if random.randint(1, 30) == 1:
            enemies.append(Enemy())

        # Spawn power-ups occasionally
        if random.randint(1, 200) == 1:
            powerups.append(PowerUp())

        # Update enemies
        for enemy in enemies[:]:
            enemy.move()
            if enemy.rect.top > SCREEN_HEIGHT:
                enemies.remove(enemy)
            for bullet in flight.bullets[:]:
                if enemy.rect.colliderect(bullet):
                    enemies.remove(enemy)
                    flight.bullets.remove(bullet)
                    score += 1
                    break
            if enemy.rect.colliderect(flight.rect):
                game_over_screen(score)
                return
            enemy.draw()

        # Update power-ups
        for powerup in powerups[:]:
            powerup.move()
            if powerup.rect.top > SCREEN_HEIGHT:
                powerups.remove(powerup)
            elif powerup.rect.colliderect(flight.rect):
                if powerup.type == 'fast_shoot':
                    flight.powered_up = True
                    flight.power_timer = pygame.time.get_ticks()
                elif powerup.type == 'extra_points':
                    score += 5
                powerups.remove(powerup)
            powerup.draw()

        # Disable power-up after 5 seconds
        if flight.powered_up and pygame.time.get_ticks() - flight.power_timer > 5000:
            flight.powered_up = False

        flight.draw()
        left_button.draw()
        right_button.draw()

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

# --- Main Menu ---
def main_menu():
    start_button = Button(200, 300, 200, 60, "Start Game", BLUE, GREEN)
    quit_button = Button(200, 400, 200, 60, "Quit", RED, ORANGE)
    title_font = pygame.font.Font(None, 60)
    running = True

    while running:
        screen.fill((10, 10, 20))
        title_text = title_font.render("✈️ Real Flight Shooter ✈️", True, YELLOW)
        screen.blit(title_text, (70, 150))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if start_button.is_clicked(event):
                main_game()
            if quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

        start_button.draw()
        quit_button.draw()

        pygame.display.flip()
        clock.tick(60)

# --- Run the Game ---
main_menu()
