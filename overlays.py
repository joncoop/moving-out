import pygame
import math

from settings import *

pygame.init()

# Fonts
FONT_SM = pygame.font.Font(None, 48)
FONT_MD = pygame.font.Font(None, 64)
FONT_LG = pygame.font.Font(None, 96)

class TitleScreen:

    def __init__(self, game):
        self.game = game

    def update(self):
        pass

    def draw(self, surface):
        text = FONT_LG.render(TITLE, True, BLUE)
        rect = text.get_rect()
        rect.center = WIDTH // 2, HEIGHT // 2
        surface.blit(text, rect)


class WinScreen:

    def __init__(self, game):
        self.game = game

    def update(self):
        pass

    def draw(self, surface):
        text = FONT_LG.render("You win!", True, BLUE)
        rect = text.get_rect()
        rect.center = WIDTH // 2, HEIGHT // 2
        surface.blit(text, rect)


class LoseScreen:

    def __init__(self, game):
        self.game = game

    def update(self):
        pass

    def draw(self, surface):
        text = FONT_LG.render("Time's up.", True, BLUE)
        rect = text.get_rect()
        rect.center = WIDTH // 2, HEIGHT // 2
        surface.blit(text, rect)


class HUD:

    def __init__(self, game):
        self.game = game

    def update(self):
        pass

    def draw(self, surface):
        minutes = (math.ceil(self.game.time_remaining / FPS)) // 60
        seconds = (math.ceil(self.game.time_remaining / FPS)) % 60

        text = FONT_SM.render(f"{minutes}:{seconds:02d}", True, BLUE)
        rect = text.get_rect()
        rect.topleft = 16, 16
        surface.blit(text, rect)
