import pygame
import math

from settings import *

pygame.init()

# Fonts
FONT_SM = pygame.font.Font('assets/fonts/Splatch.ttf', 24)
FONT_MD = pygame.font.Font('assets/fonts/Splatch.ttf', 48)
FONT_LG = pygame.font.Font('assets/fonts/Splatch.ttf', 64)

class TitleScreen:

    def __init__(self, game):
        self.game = game

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(RED)

        text = FONT_LG.render(TITLE, True, WHITE)
        rect = text.get_rect()
        rect.midbottom = WIDTH // 2, HEIGHT // 2 - 8
        surface.blit(text, rect)

        sub_text = FONT_SM.render("Press START.", True, WHITE)
        rect = sub_text.get_rect()
        rect.midtop = WIDTH // 2, HEIGHT // 2 + 8
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
            time_color == RED
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