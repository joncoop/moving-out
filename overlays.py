import pygame
import math

from settings import *

pygame.init()

# Fonts
FONT_SM = pygame.font.Font('assets/fonts/Splatch.ttf', 20)
FONT_MD = pygame.font.Font('assets/fonts/Splatch.ttf', 48)
FONT_LG = pygame.font.Font('assets/fonts/Splatch.ttf', 64)

class TitleScreen:

    def __init__(self, game):
        self.game = game
        self.reset()

    def reset(self):
        self.truck_x, self.truck_y = 250, 260
        self.truck_speed = 0
        self.time_elapsed = 0

    def update(self):
        self.time_elapsed += 1

        if self.time_elapsed == 90:
            self.game.truck_sound.play()

        if self.time_elapsed > 180:
            self.truck_speed += 0.5
            self.truck_speed = min(self.truck_speed, 15)
            self.truck_x += self.truck_speed

    def draw(self, surface):
        surface.fill(SKY_BLUE)
        surface.blit(self.game.sky_img, [0, -100])
        pygame.draw.rect(surface, DARK_GRAY, [0, 560, 960, 80])
        surface.blit(self.game.van_img, [self.truck_x, self.truck_y])

        text = FONT_LG.render(TITLE, True, RED)
        rect = text.get_rect()
        rect.midtop = WIDTH // 2, 130
        surface.blit(text, rect)

        if self.truck_x > WIDTH:
            alpha = min(self.truck_x - WIDTH, 255)
            sub_text = FONT_SM.render("Press START.", True, DARK_GRAY)
            sub_text.set_alpha(alpha)
            rect = sub_text.get_rect()
            rect.midtop = WIDTH // 2, 280
            surface.blit(sub_text, rect)


class WinScreen:

    def __init__(self, game):
        self.game = game

    def update(self):
        pass

    def draw(self, surface):
        text = FONT_MD.render("You win!", True, BLUE)
        rect = text.get_rect()
        rect.midbottom = WIDTH // 2, HEIGHT // 2 - 8
        surface.blit(text, rect)

        sub_text = FONT_SM.render("Press START.", True, BLUE)
        rect = sub_text.get_rect()
        rect.midtop = WIDTH // 2, HEIGHT // 2 + 8
        surface.blit(sub_text, rect)


class LoseScreen:

    def __init__(self, game):
        self.game = game

    def update(self):
        pass

    def draw(self, surface):
        text = FONT_MD.render("Time's up.", True, BLUE)
        rect = text.get_rect()
        rect.midbottom = WIDTH // 2, HEIGHT // 2 - 8
        surface.blit(text, rect)

        sub_text = FONT_SM.render("Press START.", True, BLUE)
        rect = sub_text.get_rect()
        rect.midtop = WIDTH // 2, HEIGHT // 2 + 8
        surface.blit(sub_text, rect)


class HUD:

    def __init__(self, game):
        self.game = game

    def update(self):
        pass

    def draw(self, surface):
        minutes = (math.ceil(self.game.time_remaining / FPS)) // 60
        seconds = (math.ceil(self.game.time_remaining / FPS)) % 60

        if minutes == 0 and seconds <= 10:
            time_color = RED
        else:
            time_color = BLACK

        text = FONT_SM.render(f"{minutes}:{seconds:02d}", True, time_color)
        rect = text.get_rect()
        rect.topleft = 16, 16
        surface.blit(text, rect)


class Grid:

    def __init__(self, game):
        self.game = game

        self.size = 32

    def draw(self, surface):
        for x in range(self.size, WIDTH, self.size):
            pygame.draw.line(surface, BLACK, [x, 0], [x, HEIGHT])
            
        for y in range(self.size, HEIGHT, self.size):
            pygame.draw.line(surface, BLACK, [0, y], [WIDTH, y])