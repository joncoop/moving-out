# Imports
import pygame
import entities
import math
import xbox360_controller

# Initialize game engine
pygame.init()

# Settings
WIDTH = 800
HEIGHT = 600
TITLE = "Moving Out"
FPS = 60

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


class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.running = True
        self.new_game()

        self.p1_controller = xbox360_controller.Controller()

    def new_game(self):
        self.players = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.goal = pygame.sprite.GroupSingle()

        self.p1 = entities.Player([700, 525, 50, 50], RED)
        self.players.add(self.p1)

        wall1 = entities.Obstacle([100, 200, 400, 25], WHITE)
        wall2 = entities.Obstacle([100, 225, 25, 275], WHITE)
        wall3 = entities.Obstacle([475, 225, 25, 275], WHITE)
        wall4 = entities.Obstacle([100, 500, 100, 25], WHITE)
        wall5 = entities.Obstacle([400, 500, 100, 25], WHITE)
        tree = entities.Obstacle([400, 50, 50, 50], GREEN)
        self.obstacles.add(wall1, wall2, wall3, wall4, wall5, tree)

        self.g = entities.Goal([600, 250, 150, 200], GRAY)
        self.goal.add(self.g)

        i1 = entities.Item([400, 300, 25, 25], YELLOW)
        i2 = entities.Item([100, 50, 25, 25], YELLOW)
        i3 = entities.Item([200, 400, 25, 25], YELLOW)
        self.items.add(i1, i2, i3)

        self.current_scene = START
        self.time_remaining = 30 * FPS

    def start(self):
        global current_scene
        self.current_scene = PLAYING

    def win(self):
        global current_scene
        self.current_scene = WIN

    def lose(self):
        global current_scene
        self.current_scene = LOSE

    def show_start_screen(self):
        text = FONT_LG.render(TITLE, True, BLUE)
        rect = text.get_rect()
        rect.center = WIDTH // 2, HEIGHT // 2
        self.screen.blit(text, rect)

    def show_win_screen(self):
        text = FONT_MD.render("You win!", True, BLUE)
        rect = text.get_rect()
        rect.center = WIDTH // 2, HEIGHT // 2
        self.screen.blit(text, rect)

    def show_lose_screen(self):
        text = FONT_MD.render("Time's up.", True, BLUE)
        rect = text.get_rect()
        rect.center = WIDTH // 2, HEIGHT // 2
        self.screen.blit(text, rect)

    def show_stats(self):
        min = (math.ceil(self.time_remaining / FPS)) // 60
        sec = (math.ceil(self.time_remaining / FPS)) % 60

        text = FONT_SM.render(f"{min}:{sec:02d}", True, BLUE)
        rect = text.get_rect()
        rect.topleft = 16, 16
        self.screen.blit(text, rect)

    def all_items_in_goal(self):
        for item in self.items:
            if item.vx != 0 or item.vy != 0:
                return False
            
        items_in_goal = pygame.sprite.spritecollide(self.g, self.items, False)
        held_items = self.p1.my_item

        return held_items is None and len(items_in_goal) == len(self.items)

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.current_scene == START:
                    if event.key == pygame.K_SPACE:
                        self.start()
                elif self.current_scene == PLAYING:
                    if event.key == pygame.K_SPACE:
                        if self.p1.my_item == None:
                            self.p1.pick_up(self.items)
                        else:
                            self.p1.drop()
                elif self.current_scene in [WIN, LOSE]:
                    if event.key == pygame.K_r:
                        self.new_game()

            elif event.type == pygame.JOYBUTTONDOWN:
                if self.current_scene == START:
                    if event.button == xbox360_controller.START:
                        self.start()
                elif self.current_scene == PLAYING:
                    if event.button == xbox360_controller.A:
                        if self.p1.my_item == None:
                            self.p1.pick_up(self.items)
                        else:
                            self.p1.drop()
                elif self.current_scene in [WIN, LOSE]:
                    if event.button == xbox360_controller.START:
                        self.new_game()

        # keyboard controls
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            self.p1.go_left()
        elif pressed[pygame.K_RIGHT]:
             self.p1.go_right()
        else:
             self.p1.stop_x()
            
        if pressed[pygame.K_UP]:
             self.p1.go_up()
        elif pressed[pygame.K_DOWN]:
             self.p1.go_down()
        else:
             self.p1.stop_y()

        # game controller
        left_x, left_y = self.p1_controller.get_left_stick()
        self.p1.go(left_x, left_y)

    def update(self):
        if self.current_scene == PLAYING:
            self.players.update(WIDTH, HEIGHT, self.obstacles, self.items)
            self.items.update(WIDTH, HEIGHT, self.obstacles)
            
            if self.all_items_in_goal():
                self.win()
            elif self.time_remaining == 0:
                self.lose()
            else:
                self.time_remaining -= 1

    def render(self):
        self.screen.fill(BLACK)
        self.obstacles.draw(self.screen)
        self.goal.draw(self.screen)
        self.players.draw(self.screen)
        self.items.draw(self.screen)
        self.show_stats()

        if self.current_scene == START:
            self.show_start_screen()
        elif self.current_scene == WIN:
            self.show_win_screen()
        elif self.current_scene == LOSE:
            self.show_lose_screen()
    
    def run(self):
        while self.running:
            self.process_input()
            self.update()
            self.render()

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()


# Let's do this!
if __name__ == '__main__':
    g = Game()
    g.run()
