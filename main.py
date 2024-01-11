import sys
import pygame
from pygame import Surface, sprite
from pygame.locals import *

pygame.init()

fps = 60
clock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
MOVE_SPEED = 10
WIDTH = 22
HEIGHT = 32
COLOR = "#888888"
right = False
lvl_image = pygame.image.load("fon_level.png")
player_image = pygame.image.load("creature.png")
level = [
    "                                                                                                                        ",
    "                                                                                                                        ",
    "                                                                                                                        ",
    "                                                                                                                        ",
    "                                                       --------                       ----------                        ",
    "                   ------                                                                            --------           ",
    "    ------                          --------                         ---------                                          ",
    "------------------------------------------------------------------------------------------------------------------------"]


def terminate():
    pygame.quit()
    sys.exit()


# заставка
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 250 and event.pos[0] <= 400 and event.pos[1] >= 250 and event.pos[1] <= 300:
                    return
        pygame.display.flip()
        clock.tick(fps)
def do_fon(screen):
    width, height = 1000, 400
    new_screen = pygame.display.set_mode((width, height))
    screen = new_screen
    screen.fill((102, 201, 218))
    x = y = 0  # координаты
    up = False
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                # создаем блок, заливаем его цветом и рисеум его
                pf = Surface((50, 50))
                pf.fill(Color((173, 100, 82)))
                screen.blit(pf, (x, y))
            x += 50  # блоки платформы ставятся на ширине блоков
        y += 50  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

def draw_level(screen):
    posx = 90
    posy = 280
    right = False
      # изменить цвет
    do_fon(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    right = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    right = False
        if right:
            posx += MOVE_SPEED
            do_fon(screen)
        screen.blit(player_image, (posx, posy))
        pygame.display.flip()
        clock.tick(fps)


# меню с выбором уровня
def draw_menu(screen):
    while True:
        screen.blit(lvl_image, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 47 and event.pos[0] <= 134 and event.pos[1] >= 155 and event.pos[1] <= 240:
                    draw_level(screen)

        # Update.

        # Draw.
        pygame.display.flip()
        clock.tick(fps)


draw_screensaver(screen)
draw_menu(screen)
# основной цикл всей игры
while True:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

    # Update.

    # Draw.
    pygame.display.flip()
    clock.tick(fps)

    # Update.

    # Draw.
    pygame.display.flip()
    clock.tick(fps)
