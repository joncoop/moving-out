# Imports
import pygame
import xbox360_controller

from entities import *
from overlays import *
from settings import *


# Initialize game engine
pygame.init()


# The main game class
class Game:
    # Scenes
    START = 0
    PLAYING = 1
    WIN = 2
    LOSE = 3

    def __init__(self):
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.running = True
        self.new_game()

        self.p1_controller = xbox360_controller.Controller()

        self.title_screen = TitleScreen(self)
        self.win_screen = WinScreen(self)
        self.lose_screen = LoseScreen(self)
        self.hud = HUD(self)
        
    def new_game(self):
        self.players = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.goal = pygame.sprite.GroupSingle()

        self.p1 = Player(self, [700, 525, 50, 50], RED)
        self.players.add(self.p1)

        wall1 = Obstacle(self, [100, 200, 400, 25], WHITE)
        wall2 = Obstacle(self, [100, 225, 25, 275], WHITE)
        wall3 = Obstacle(self, [475, 225, 25, 275], WHITE)
        wall4 = Obstacle(self, [100, 500, 100, 25], WHITE)
        wall5 = Obstacle(self, [400, 500, 100, 25], WHITE)
        tree = Obstacle(self, [400, 50, 50, 50], GREEN)
        self.obstacles.add(wall1, wall2, wall3, wall4, wall5, tree)

        self.truck = Goal(self, [600, 250, 150, 200], GRAY)
        self.goal.add(self.truck)

        i1 = Item(self, [400, 300, 25, 25], YELLOW)
        i2 = Item(self, [100, 50, 25, 25], YELLOW)
        i3 = Item(self, [200, 400, 25, 25], YELLOW)
        self.items.add(i1, i2, i3)

        self.current_scene = Game.START
        self.time_remaining = 30 * FPS

    def start(self):
        self.current_scene = Game.PLAYING

    def win(self):
        self.current_scene = Game.WIN

    def lose(self):
        self.current_scene = Game.LOSE

    def all_items_in_goal(self):
        for item in self.items:
            if item.vx != 0 or item.vy != 0:
                return False
            
        items_in_goal = pygame.sprite.spritecollide(self.truck, self.items, False)
        held_items = self.p1.my_item

        return held_items is None and len(items_in_goal) == len(self.items)

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                if self.current_scene == Game.START:
                    if event.button == xbox360_controller.START:
                        self.start()
                elif self.current_scene == Game.PLAYING:
                    if event.button == xbox360_controller.A:
                        if self.p1.my_item == None:
                            self.p1.pick_up()
                        else:
                            self.p1.drop()
                elif self.current_scene in [Game.WIN, Game.LOSE]:
                    if event.button == xbox360_controller.START:
                        self.new_game()

        left_x, left_y = self.p1_controller.get_left_stick()
        self.p1.go(left_x, left_y)

    def update(self):
        if self.current_scene == Game.PLAYING:
            self.players.update()
            self.items.update()
            
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
        self.hud.draw(self.screen)

        if self.current_scene == Game.START:
            self.title_screen.draw(self.screen)
        elif self.current_scene == Game.WIN:
            self.win_screen.draw(self.screen)
        elif self.current_scene == Game.LOSE:
            self.lose_screen.draw(self.screen)
    
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
