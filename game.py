# Imports
import pygame
import entities
import math

# Screen settings
WIDTH = 800
HEIGHT = 600
TITLE = "Moving Out"
FPS = 60

# Initialize game engine
pygame.init()

# Make the screen
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
FONT_SM = pygame.font.Font(None, 48)
FONT_MD = pygame.font.Font(None, 64)
FONT_LG = pygame.font.Font(None, 96)

# Scenes
START = 0
PLAYING = 1
WIN = 2
LOSE = 3

# Helper functions
def new_game():
    global p1, g, players, items, obstacles, goal, current_scene, time_remaining

    players = pygame.sprite.Group()
    items = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    goal = pygame.sprite.GroupSingle()

    # Make game objects
    p1 = entities.Player([700, 525, 50, 50], RED)
    players.add(p1)

    wall1 = entities.Obstacle([100, 200, 400, 25], WHITE)
    wall2 = entities.Obstacle([100, 225, 25, 275], WHITE)
    wall3 = entities.Obstacle([475, 225, 25, 275], WHITE)
    wall4 = entities.Obstacle([100, 500, 100, 25], WHITE)
    wall5 = entities.Obstacle([400, 500, 100, 25], WHITE)
    tree = entities.Obstacle([400, 50, 50, 50], GREEN)
    obstacles.add(wall1, wall2, wall3, wall4, wall5, tree)

    g = entities.Goal([600, 250, 150, 200], GRAY)
    goal.add(g)

    i1 = entities.Item([400, 300, 25, 25], YELLOW)
    i2 = entities.Item([100, 50, 25, 25], YELLOW)
    i3 = entities.Item([200, 400, 25, 25], YELLOW)
    items.add(i1, i2, i3)

    current_scene = START
    time_remaining = 30 * FPS

def start():
    global current_scene
    current_scene = PLAYING

def win():
    global current_scene
    current_scene = WIN

def lose():
    global current_scene
    current_scene = LOSE

def show_start_screen():
    text = FONT_LG.render(TITLE, True, BLUE)
    rect = text.get_rect()
    rect.center = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)

def show_win_screen():
    text = FONT_MD.render("You win!", True, BLUE)
    rect = text.get_rect()
    rect.center = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)

def show_lose_screen():
    text = FONT_MD.render("Time's up.", True, BLUE)
    rect = text.get_rect()
    rect.center = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)

def show_stats():
    min = (math.ceil(time_remaining / FPS)) // 60
    sec = (math.ceil(time_remaining / FPS)) % 60

    text = FONT_SM.render(f"{min}:{sec:02d}", True, BLUE)
    rect = text.get_rect()
    rect.topleft = 16, 16
    screen.blit(text, rect)

def all_items_in_goal():
    for item in items:
        if item.vx != 0 or item.vy != 0:
            return False
        
    items_in_goal = pygame.sprite.spritecollide(g, items, False)
    held_items = p1.my_item

    return held_items is None and len(items_in_goal) == len(items)


# Let's do this!
new_game()

# Game loop
running = True

while running:
    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if current_scene == START:
                if event.key == pygame.K_SPACE:
                    start()
            elif current_scene == PLAYING:
                if event.key == pygame.K_SPACE:
                    if p1.my_item == None:
                        p1.pick_up(items)
                    else:
                        p1.drop()
            elif current_scene in [WIN, LOSE]:
                if event.key == pygame.K_r:
                    new_game()

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_LEFT]:
        p1.go_left()
    elif pressed[pygame.K_RIGHT]:
        p1.go_right()
    else:
        p1.stop_x()
        
    if pressed[pygame.K_UP]:
        p1.go_up()
    elif pressed[pygame.K_DOWN]:
        p1.go_down()
    else:
        p1.stop_y()


    # Logic
    if current_scene == PLAYING:
        players.update(WIDTH, HEIGHT, obstacles, items)
        items.update(WIDTH, HEIGHT, obstacles)
        
        if all_items_in_goal():
            win()
        elif time_remaining == 0:
            lose()
        else:
            time_remaining -= 1



    # Drawing
    screen.fill(BLACK)
    obstacles.draw(screen)
    goal.draw(screen)
    players.draw(screen)
    items.draw(screen)
    show_stats()

    if current_scene == START:
        show_start_screen()
    elif current_scene == WIN:
        show_win_screen()
    elif current_scene == LOSE:
        show_lose_screen()

    # Update screen
    pygame.display.update()
    clock.tick(FPS)


# Close window and quit
pygame.quit()
