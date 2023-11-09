import pygame
import random
import math

from settings import *


class Entity(pygame.sprite.Sprite):

    def __init__(self, game, xywh, color, image):
        super().__init__()

        self.game = game

        x, y, w, h = xywh

        if image is not None:
            self.image = image
        else:
            # delete this secion once all entites are images
            self.image = pygame.Surface([w, h])
            self.image.fill(color)

        self.original_image = self.image
        self.angle = 0

        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

    def move_x(self):            
        self.rect.x += self.vx

    def move_y(self):
        self.rect.y += self.vy

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

    def apply_friction(self):
        if self.vx < 0:
            self.vx += 0.2
        elif self.vx > 0:
            self.vx -= 0.2
        else:
            self.vx = 0

        if self.vy < 0:
            self.vy += 0.2
        elif self.vy > 0:
            self.vy -= 0.2
        else:
            self.vy = 0

    def set_image(self):
        center = self.rect.center
        angle_degrees = math.degrees(self.angle)
        self.image = pygame.transform.rotate(self.original_image, -angle_degrees)
        self.rect.center = center


class Player(Entity):

    def __init__(self, game, xywh, color, image=None):
        super().__init__(game, xywh, color, image)

        self.vx = 0
        self.vy = 0
        self.speed = 5

        self.my_item = None
    
    def go(self, x, y):
        if self.my_item is None:
            slow_down_multiplier = 1.0
        else:
            slow_down_multiplier = 0.6 # eventually should account for item weight

        self.vx = slow_down_multiplier * self.speed * x
        self.vy = slow_down_multiplier * self.speed * y

    def pick_up(self):
        if self.my_item is not None:
            return
        
        touched_items = pygame.sprite.spritecollide(self, self.game.items, False)

        if touched_items:
            self.my_item = random.choice(touched_items)

    def drop(self):
        if self.my_item is not None:
            self.my_item.vx = self.vx
            self.my_item.vy = self.vy

            self.my_item = None

    def throw(self):
        if self.my_item is not None:
            throw_speed = 8 # should factor in weight

            self.my_item.vx = math.sin(-1 * self.angle + math.pi /2) * throw_speed
            self.my_item.vy = math.cos(-1 * self.angle + math.pi /2) * throw_speed

            self.my_item = None

    def rotate(self):
        # stay facing same direction if not moving
        if self.vx == 0 and self.vy == 0:
            return
        
        self.angle = math.atan2(self.vy, self.vx)

    def set_carry_loc(self):
        if self.my_item is not None:
            self.my_item.angle = self.angle

            # -1 and math.pi /2 are for getting item in correct quadrant, 35 is pixel offset from center
            x = self.rect.centerx + math.sin(-1 * self.angle + math.pi /2) * 35
            y = self.rect.centery + math.cos(-1 * self.angle + math.pi /2) * 35

            self.my_item.rect.center = x, y

    def update(self):
        # Do not change order of movement/collision section
        self.move_x()
        self.check_walls_x()
        self.move_y()
        self.check_walls_y()
        self.check_boundaries()
        
        # Other tasks
        self.rotate()
        self.set_image()
        self.set_carry_loc()


class Obstacle(Entity):

    def __init__(self, game, xywh, color, image=None):
        super().__init__(game, xywh, color, image)


class Item(Entity):

    def __init__(self, game, xywh, color, image=None):
        super().__init__(game, xywh, color, image)

        self.vx = 0
        self.vy = 0

    def update(self):
        self.move_x()
        self.check_walls_x()
        self.move_y()
        self.check_walls_y()
        self.check_boundaries()
        self.set_image()
        self.apply_friction()


class Goal(Entity):

    def __init__(self, game, xywh, color, image=None):
        super().__init__(game, xywh, color, image)
