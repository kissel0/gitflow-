import sys
import pygame
from pygame import Surface, sprite
from pygame.locals import *
import pyganim

pygame.init()

fps = 60
clock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
blocks = pygame.sprite.Group()
right = False
lvl_image = pygame.image.load("fon_level.png")
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR = "#888888"
JUMP_POWER = 10
GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз
ANIMATION_DELAY = 0.1
ANIMATION_RIGHT = [('mario/r1.png'),
                   ('mario/r2.png'),
                   ('mario/r3.png'),
                   ('mario/r4.png'),
                   ('mario/r5.png')]
ANIMATION_LEFT = [('mario/l1.png'),
                  ('mario/l2.png'),
                  ('mario/l3.png'),
                  ('mario/l4.png'),
                  ('mario/l5.png')]

monsters = pygame.sprite.Group()


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным
        #        Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        #        Анимация движения влево
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        self.boltAnimStay = pyganim.PygAnimation([('mario/0.png', 0.1)])
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим

        self.boltAnimJumpLeft = pyganim.PygAnimation([('mario/jl.png', 0.1)])
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation([('mario/jr.png', 0.1)])
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation([('mario/j.png', 0.1)])
        self.boltAnimJump.play()

    def update(self, left, right, up, platforms):

        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
            self.image.fill(Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))

        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.image.fill(Color(COLOR))
            if up:  # для прыжка влево есть отдельная анимация
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n
            self.image.fill(Color(COLOR))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False;  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = pygame.image.load('platform.png')
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY


class Cactus(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.y = y
        self.x = x
        self.image = pygame.image.load('cactus_bricks.png')
        self.image = pygame.transform.scale(self.image, (50, 50))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY


def die(self):
    pygame.time.wait(500)
    draw_menu(screen)


ANIMATION_MONSTERHORYSONTAL = [('monsters/fire1.png'),
                               ('monsters/fire2.png')]


class Fire(sprite.Sprite):
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp):
        sprite.Sprite.__init__(self)
        self.image = Surface((32, 32))
        self.image.fill(Color("#2110FF"))
        self.rect = Rect(x, y, 32, 32)
        self.image.set_colorkey(Color("#2110FF"))
        self.startX = x  # начальные координаты
        self.startY = y
        self.maxLengthLeft = maxLengthLeft  # максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthUp = maxLengthUp  # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = left  # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = up  # скорость движения по вертикали, 0 - не двигается
        boltAnim = []
        for anim in ANIMATION_MONSTERHORYSONTAL:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self, platforms):  # по принципу героя

        self.image.fill(Color("#2110FF"))
        self.boltAnim.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel = -self.xvel  # если прошли максимальное растояние, то идеи в обратную сторону
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.yvel = -self.yvel  # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:  # если с чем-то или кем-то столкнулись
                self.xvel = - self.xvel  # то поворачиваем в обратную сторону
                self.yvel = - self.yvel


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + 800 / 2, -t + 400 / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - 800), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - 400), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


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


def main(screen):
    new_screen = pygame.display.set_mode((800, 250))
    pygame.init()  # Инициация PyGame, обязательная строчка
    pygame.display.set_caption("Super Mario Boy")  # Пишем в шапку
    bg = Surface((800, 250))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(176, 224, 230))  # Заливаем поверхность сплошным цветом
    hero = Player(55, 55)  # создаем героя по (x,y) координатам
    left = right = False  # по умолчанию - стоим
    up = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться

    entities.add(hero)

    level = [
        "                                                                                                                        ",
        "                                                                                                                        ",
        "                                                                                                                        ",
        "                                                                                                                        ",
        "                     /                                 --------                       ----------       /                ",
        "                   ------                                                                            --------           ",
        "    ------ *                        --------                        *---------                                          ",
        "------------------------------------------------------------------------------------------------------------------------"]

    timer = pygame.time.Clock()
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == '*':
                ct = Cactus(x, y)
                entities.add(ct)
                platforms.append(ct)
            if col == '/':
                mn = Fire(x, y, 2, 3, 150, 15)
                entities.add(mn)
                platforms.append(mn)
                monsters.add(mn)
                monsters.update(platforms)
            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while 1:  # Основной цикл программы
        timer.tick(60)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                pygame.quit()
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
        new_screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.update(left, right, up, platforms)  # передвижение
        # entities.draw(screen) # отображение
        for e in entities:
            new_screen.blit(e.image, camera.apply(e))

        pygame.display.update()  # обновление и вывод всех изменений на экран


# меню с выбором уровня
def draw_menu(screen):
    while True:
        screen.blit(lvl_image, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 47 and event.pos[0] <= 134 and event.pos[1] >= 155 and event.pos[1] <= 240:
                    main(screen)

        # Update.

        # Draw.
        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    draw_screensaver(screen)
    draw_menu(screen)
