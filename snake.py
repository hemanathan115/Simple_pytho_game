import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
gray = (200, 200, 200)
dark_gray = (120, 120, 120)
light_green = (144, 238, 144)

# Screen setup
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('🐍 Snake Game - Manual Button Control')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 12

font_style = pygame.font.SysFont("bahnschrift", 25)
title_font = pygame.font.SysFont("comicsansms", 45)
score_font = pygame.font.SysFont("comicsansms", 30)

# Draw gradient background
def draw_background():
    for y in range(dis_height):
        color = (50, 100 + y // 10, 150 + y // 15)
        pygame.draw.line(dis, color, (0, y), (dis_width, y))

# Display score
def Your_score(score):
    pygame.draw.rect(dis, black, [5, 5, 140, 40], border_radius=8)
    value = score_font.render("Score: " + str(score), True, yellow)
    dis.blit(value, [10, 10])

# Draw snake
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, light_green, [x[0], x[1], snake_block, snake_block])
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block], 1)

# Message display
def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 2 + y_offset])

# Draw a rounded button
def draw_button(x, y, w, h, text, color, hover=False):
    pygame.draw.rect(dis, dark_gray if hover else color, [x, y, w, h], border_radius=10)
    text_surf = font_style.render(text, True, black)
    dis.blit(text_surf, (x + w/3, y + h/4))
    return pygame.Rect(x, y, w, h)

# ---------- START SCREEN ----------
def start_screen():
    while True:
        draw_background()
        title = title_font.render("🐍 Snake Game", True, yellow)
        dis.blit(title, [dis_width / 3, dis_height / 4])

        mouse_pos = pygame.mouse.get_pos()

        play_btn = draw_button(320, 300, 150, 60, "PLAY", gray, 320 <= mouse_pos[0] <= 470 and 300 <= mouse_pos[1] <= 360)
        quit_btn = draw_button(320, 400, 150, 60, "QUIT", gray, 320 <= mouse_pos[0] <= 470 and 400 <= mouse_pos[1] <= 460)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):
                    return  # start the game
                elif quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# ---------- MAIN GAME FUNCTION ----------
def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block - 100) / 10.0) * 10.0

    # Button setup
    btn_size = 60
    btn_y = dis_height - 80
    direction = 'STOP'

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost! Press C to Play Again or Q to Quit", red, -20)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if left_btn.collidepoint(mouse_pos):
                    direction = 'LEFT'
                elif right_btn.collidepoint(mouse_pos):
                    direction = 'RIGHT'
                elif up_btn.collidepoint(mouse_pos):
                    direction = 'UP'
                elif down_btn.collidepoint(mouse_pos):
                    direction = 'DOWN'

        # Direction control
        if direction == 'LEFT':
            x1_change = -snake_block
            y1_change = 0
        elif direction == 'RIGHT':
            x1_change = snake_block
            y1_change = 0
        elif direction == 'UP':
            y1_change = -snake_block
            x1_change = 0
        elif direction == 'DOWN':
            y1_change = snake_block
            x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height - 100 or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        draw_background()

        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        # Draw buttons (manual control)
        mouse_pos = pygame.mouse.get_pos()
        left_btn = draw_button(300, btn_y, btn_size, btn_size, "←", gray, 300 <= mouse_pos[0] <= 360 and btn_y <= mouse_pos[1] <= btn_y+btn_size)
        right_btn = draw_button(420, btn_y, btn_size, btn_size, "→", gray, 420 <= mouse_pos[0] <= 480 and btn_y <= mouse_pos[1] <= btn_y+btn_size)
        up_btn = draw_button(360, btn_y - 70, btn_size, btn_size, "↑", gray, 360 <= mouse_pos[0] <= 420 and btn_y-70 <= mouse_pos[1] <= btn_y-10)
        down_btn = draw_button(360, btn_y + 70, btn_size, btn_size, "↓", gray, 360 <= mouse_pos[0] <= 420 and btn_y+70 <= mouse_pos[1] <= btn_y+130)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block - 100) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# ---------- MAIN CALL ----------
start_screen()
gameLoop()
