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
        
        self.p1_controller = xbox360_controller.Controller()

        self.title_screen = TitleScreen(self)
        self.win_screen = WinScreen(self)
        self.lose_screen = LoseScreen(self)
        self.hud = HUD(self)

        self.grid = Grid(self)
        self.grid_on = False

        self.load_assets()
        self.new_game()

    def load_assets(self):
        self.van_img = pygame.image.load('assets/images/truck_with_boxes.png').convert_alpha()
        self.sky_img = pygame.image.load('assets/images/backgrounds/sky1.png').convert_alpha()
        self.truck_sound = pygame.mixer.Sound('assets/sounds/start_and_drive_away.ogg')

        self.man_img = pygame.image.load('assets/images/characters/man_blue.png').convert_alpha()

        self.large_box_img = pygame.image.load('assets/images/furniture/box_large.png').convert_alpha()
        self.small_box_img = pygame.image.load('assets/images/furniture/box_small.png').convert_alpha()
        self.chair_img = pygame.image.load('assets/images/furniture/chair_blue.png').convert_alpha()

        self.tree_img = pygame.image.load('assets/images/tiles/tree.png').convert_alpha()
        self.bush_img = pygame.image.load('assets/images/tiles/bush.png').convert_alpha()

        self.beep_sound = pygame.mixer.Sound('assets/sounds/beep.ogg')

    def new_game(self):
        self.players = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.goal = pygame.sprite.GroupSingle()

        self.p1 = Player(self, [704, 512, 48, 48], BLUE, self.man_img)
        self.players.add(self.p1)

        wall1 = Obstacle(self, [96, 224, 512, 32], WHITE)
        wall2 = Obstacle(self, [96, 256, 32, 256], WHITE)
        wall3 = Obstacle(self, [576, 256, 32, 256], WHITE)
        wall4 = Obstacle(self, [96, 512, 192, 32], WHITE)
        wall5 = Obstacle(self, [416, 512, 192, 32], WHITE)

        tree1 = Obstacle(self, [640, 64, 96, 96], DARK_GREEN, self.tree_img)
        bush1 = Obstacle(self, [256, 128, 96, 96], DARK_GREEN, self.bush_img)
        bush2 = Obstacle(self, [832, 512, 96, 96], DARK_GREEN, self.bush_img)

        self.obstacles.add(wall1, wall2, wall3, wall4, wall5)
        self.obstacles.add(tree1, bush1, bush2)

        self.truck = Goal(self, [672, 288, 128, 192], RED)
        self.goal.add(self.truck)

        i1 = Item(self, [400, 300, 48, 48], BROWN, self.large_box_img)
        i2 = Item(self, [100, 50, 48, 48], BROWN, self.small_box_img)
        i3 = Item(self, [200, 400, 48, 48], BROWN, self.chair_img)
        self.items.add(i1, i2, i3)

        self.current_scene = Game.START
        self.time_remaining = 30 * FPS

        self.title_screen.reset()

    def start(self):
        self.current_scene = Game.PLAYING
        pygame.mixer.stop()

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

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    self.grid_on = not self.grid_on

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

                ten_seconds_remain = self.time_remaining <= 10 * FPS
                even_second = self.time_remaining % FPS == 0

                if ten_seconds_remain and even_second:
                    self.beep_sound.play()
        
        if self.current_scene == Game.START:
            self.title_screen.update()

    def render(self):
        self.screen.fill(GREEN)
        pygame.draw.rect(self.screen, GRAY, [640, 256, 192, 352])
        pygame.draw.rect(self.screen, GRAY, [0, 608, 960, 32])
        pygame.draw.rect(self.screen, DARK_BROWN, [96, 224, 512, 320])

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

        if self.grid_on:
            self.grid.draw(self.screen)
    
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
