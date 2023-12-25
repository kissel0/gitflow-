import sys
import pygame_gui
import pygame
from pygame.locals import *

pygame.init()

fps = 60
clock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))


def terminate():
    pygame.quit()
    sys.exit()


def draw_screensaver(screen):
    screen.fill((194, 237, 206))  # изменить цвет
    font = pygame.font.Font(None, 50)
    font2 = pygame.font.Font(None, 35)

    text = font.render("Hello. These are Dino-Cats", True, (0, 0, 0))  # изменить цвет надписи и её саму
    text2 = font2.render("Start Game", True, (0, 0, 0))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2 - 50
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (150, 200, 170), ((250, 250), (150, 50)), 0)
    screen.blit(text, (text_x, text_y))
    screen.blit(text2, (260, 260))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 250 and event.pos[0] <= 400 and event.pos[1] >= 250 and event.pos[1] <= 300:
                    return
        pygame.display.flip()
        clock.tick(fps)


draw_screensaver(screen)

# Game loop.
while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

    # Update.

    # Draw.
    pygame.display.flip()
    clock.tick(fps)
