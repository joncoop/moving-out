import pygame
import random

from settings import *

class Entity(pygame.sprite.Sprite):

    def __init__(self, game, xywh, color):
        super().__init__()

        self.game = game

        x, y, w, h = xywh
        self.image = pygame.Surface([w, h])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y


class Player(Entity):

    def __init__(self, game, xywh, color, image=None):
        super().__init__(game, xywh, color)

        # Override entity constructor until all objects are PNGs
        if image is not None:
            self.image = image
            self.rect = image.get_rect()
            self.rect.topleft = xywh[2:]

        self.vx = 0
        self.vy = 0
        self.speed = 5

        self.my_item = None
    
    def go(self, x, y):
        self.vx = self.speed * x
        self.vy = self.speed * y

    def stop_y(self):
        self.vy = 0

    def move_x(self):            
        self.rect.x += self.vx

    def move_y(self):
        self.rect.y += self.vy

    def pick_up(self):
        if self.my_item != None:
            return
        
        touched_items = pygame.sprite.spritecollide(self, self.game.items, False)

        if touched_items:
            self.my_item = random.choice(touched_items)

    def drop(self):
        self.my_item.vx = 1.25 * self.vx
        self.my_item.vy = 1.25 * self.vy
    
        self.my_item = None

    def check_walls_x(self):
        hit_walls = pygame.sprite.spritecollide(self, self.game.obstacles, False)

        for wall in hit_walls:
            if self.vx > 0:
                self.rect.right = wall.rect.left
            elif self.vx < 0:
                self.rect.left = wall.rect.right

    def check_walls_y(self):
        hit_walls = pygame.sprite.spritecollide(self, self.game.obstacles, False)

        for wall in hit_walls:
            if self.vy > 0:
                self.rect.bottom = wall.rect.top
            elif self.vy < 0:
                self.rect.top = wall.rect.bottom

    def check_boundaries(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def carry_item(self):
        if self.my_item is None:
            return
        
        self.my_item.rect.center = self.rect.center 

    def update(self):
        # Do not change order of movement/collision section
        self.move_x()
        self.check_walls_x()
        self.move_y()
        self.check_walls_y()
        self.check_boundaries()
        
        # Other tasks
        self.carry_item()


class Obstacle(Entity):

    def __init__(self, game, xywh, color):
        super().__init__(game, xywh, color)


class Item(Entity):

    def __init__(self, game, xywh, color, image=None):
        super().__init__(game, xywh, color)

        # Override entity constructor until all objects are PNGs
        if image is not None:
            self.image = image
            self.rect = image.get_rect()
            self.rect.topleft = xywh[2:]

        self.vx = 0
        self.vy = 0

    def move_x(self):            
        self.rect.x += self.vx
        
        if self.vx < 0:
            self.vx += 0.1
        elif self.vx > 0:
            self.vx -= 0.1

        if -0.1 < self.vx < 0.1:
            self.vx = 0 

    def move_y(self):
        self.rect.y += self.vy

        if self.vy < 0:
            self.vy += 0.1
        elif self.vy > 0:
            self.vy -= 0.1

        if -0.1 < self.vy < 0.1:
            self.vy = 0 

    def check_walls_x(self):
        hit_walls = pygame.sprite.spritecollide(self, self.game.obstacles, False)

        for wall in hit_walls:
            if self.vx > 0:
                self.rect.right = wall.rect.left
            elif self.vx < 0:
                self.rect.left = wall.rect.right

    def check_walls_y(self):
        hit_walls = pygame.sprite.spritecollide(self, self.game.obstacles, False)

        for wall in hit_walls:
            if self.vy > 0:
                self.rect.bottom = wall.rect.top
            elif self.vy < 0:
                self.rect.top = wall.rect.bottom

    def check_boundaries(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def update(self):
        # Do not change order of movement/collision section
        self.move_x()
        self.check_walls_x()
        self.move_y()
        self.check_walls_y()
        self.check_boundaries()


class Goal(Entity):

    def __init__(self, game, xywh, color):
        super().__init__(game, xywh, color)

        self.game = game

        x, y, w, h = xywh
        self.image = pygame.Surface([w, h])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
