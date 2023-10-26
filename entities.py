import pygame
import random


class Player(pygame.sprite.Sprite):

    def __init__(self, xywh, color):
        super().__init__()

        x, y, w, h = xywh

        self.image = pygame.Surface([w, h])
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

        self.vx = 0
        self.vy = 0
        self.speed = 5

        self.my_item = None
    
    def go_left(self):
        self.vx = -1 * self.speed
    
    def go_right(self):
        self.vx = self.speed

    def stop_x(self):
        self.vx = 0

    def go_up(self):
        self.vy = -1 * self.speed
    
    def go_down(self):
        self.vy = self.speed

    def stop_y(self):
        self.vy = 0

    def move_x(self):            
        self.rect.x += self.vx

    def move_y(self):
        self.rect.y += self.vy

    def pick_up(self, items):
        if self.my_item != None:
            return
        
        touched_items = pygame.sprite.spritecollide(self, items, False)

        if touched_items:
            self.my_item = random.choice(touched_items)

    def drop(self):
        self.my_item.vx = 1.25 * self.vx
        self.my_item.vy = 1.25 * self.vy
    
        self.my_item = None

    def check_walls_x(self, walls):
        hit_walls = pygame.sprite.spritecollide(self, walls, False)

        for wall in hit_walls:
            if self.vx > 0:
                self.rect.right = wall.rect.left
            elif self.vx < 0:
                self.rect.left = wall.rect.right

    def check_walls_y(self, walls):
        hit_walls = pygame.sprite.spritecollide(self, walls, False)

        for wall in hit_walls:
            if self.vy > 0:
                self.rect.bottom = wall.rect.top
            elif self.vy < 0:
                self.rect.top = wall.rect.bottom

    def check_boundaries(self, width, height):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > width:
            self.rect.right = width

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > height:
            self.rect.bottom = height

    def carry_item(self):
        if self.my_item is None:
            return
        
        self.my_item.rect.center = self.rect.center 

    def update(self, width, height, walls, items):
        # Do not change order of movement/collision section
        self.move_x()
        self.check_walls_x(walls)
        self.move_y()
        self.check_walls_y(walls)
        self.check_boundaries(width, height)
        
        # Other tasks
        self.carry_item()


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, xywh, color):
        super().__init__()
    
        x, y, w, h = xywh
    
        self.image = pygame.Surface([w, h])
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y


class Item(pygame.sprite.Sprite):

    def __init__(self, xywh, color):
        super().__init__()
    
        x, y, w, h = xywh
    
        self.image = pygame.Surface([w, h])
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

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

    def check_walls_x(self, walls):
        hit_walls = pygame.sprite.spritecollide(self, walls, False)

        for wall in hit_walls:
            if self.vx > 0:
                self.rect.right = wall.rect.left
            elif self.vx < 0:
                self.rect.left = wall.rect.right

    def check_walls_y(self, walls):
        hit_walls = pygame.sprite.spritecollide(self, walls, False)

        for wall in hit_walls:
            if self.vy > 0:
                self.rect.bottom = wall.rect.top
            elif self.vy < 0:
                self.rect.top = wall.rect.bottom

    def check_boundaries(self, width, height):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > width:
            self.rect.right = width

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > height:
            self.rect.bottom = height

    def update(self, width, height, walls):
        # Do not change order of movement/collision section
        self.move_x()
        self.check_walls_x(walls)
        self.move_y()
        self.check_walls_y(walls)
        self.check_boundaries(width, height)


class Goal(pygame.sprite.Sprite):

    def __init__(self, xywh, color):
        super().__init__()
    
        x, y, w, h = xywh
    
        self.image = pygame.Surface([w, h])
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
