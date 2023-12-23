import sys

import pygame
from pygame.locals import *

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))


def draw_screensaver(screen):
    screen.fill((194, 237, 206))  # изменить цвет
    font = pygame.font.Font(None, 50)
    text = font.render("Hello. These are Dino-Cats", True, (0, 0, 0))  # изменить цвет надписи и её саму
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))


# Game loop.
while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update.

    # Draw.
    draw_screensaver(screen)

    pygame.display.flip()
    fpsClock.tick(fps)
