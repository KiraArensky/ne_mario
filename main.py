from os import system

system("pip install -r requirements.txt")

import pygame
from pygame import *
import os
import sys
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


meow_on = []
person_main = None

# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"

ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

pygame.font.init()

font = pygame.font.SysFont('arial', 40)

objects = []


class Tile(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/data/blocks/platform.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Tile_win(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/data/blocks/win.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        objects.append(self)

    def process(self, screen):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


class Monster_wraith(sprite.Sprite):
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp):
        sprite.Sprite.__init__(self)
        self.frames = []
        self.frames2 = []
        self.sheet = image.load("%s/data/Wraith.png" % ICON_DIR)
        self.sheet2 = image.load("%s/data/Wraith_right.png" % ICON_DIR)
        self.columns = 4
        self.rows = 5
        self.cut_sheet(self.sheet, self.columns, self.rows)
        self.cut_sheet2(self.sheet2, self.columns, self.rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.startX = x  # начальные координаты
        self.startY = y
        self.maxLengthLeft = maxLengthLeft  # максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthUp = maxLengthUp  # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = left  # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = up  # скорость движения по вертикали, 0 - не двигается
        self.leftt = True

    def cut_sheet(self, sheet, columns, rows):
        self.rect = Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def cut_sheet2(self, sheet, columns, rows):
        self.rect = Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames2.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, platforms):  # по принципу героя

        if self.leftt:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        else:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames2)
            self.image = self.frames2[self.cur_frame]

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel = -self.xvel  # если прошли максимальное растояние, то идеи в обратную сторону
            if self.leftt:
                self.leftt = False
            else:
                self.leftt = True
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.yvel = -self.yvel  # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль
            if self.leftt:
                self.leftt = False
            else:
                self.leftt = True

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:  # если с чем-то или кем-то столкнулись
                self.xvel = - self.xvel  # то поворачиваем в обратную сторону
                self.yvel = - self.yvel


class Monster_slime(sprite.Sprite):
    def __init__(self, x, y, left, up):
        sprite.Sprite.__init__(self)
        self.frames = []
        self.frames2 = []
        self.sheet = image.load("%s/data/Slime_right.png" % ICON_DIR)
        self.sheet2 = image.load("%s/data/Slime_left.png" % ICON_DIR)
        self.columns = 4
        self.rows = 1
        self.cut_sheet(self.sheet, self.columns, self.rows)
        self.cut_sheet2(self.sheet2, self.columns, self.rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.startX = x  # начальные координаты
        self.startY = y
        self.xvel = left  # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = up  # скорость движения по вертикали, 0 - не двигается
        self.leftt = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def cut_sheet2(self, sheet, columns, rows):
        self.rect = Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames2.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, platforms):  # по принципу героя
        if self.leftt:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames2)
            self.image = self.frames2[self.cur_frame]
        else:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        self.rect.x += self.xvel

        self.collide(platforms)

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:
                # если с чем-то или кем-то столкнулись
                self.xvel = - self.xvel  # то поворачиваем в обратную сторону
                if self.leftt:
                    self.leftt = False
                else:
                    self.leftt = True


class Meow(sprite.Sprite):
    def __init__(self, x, y, screen, clock, FPS):
        sprite.Sprite.__init__(self)
        self.screen = screen
        self.clock = clock
        self.FPS = FPS
        self.fast = 150  # скорость перемещения. 0 - стоять на месте
        self.image = Surface((10, 10))
        self.image.fill(Color("black"))
        self.frames = []
        self.frames2 = []
        self.frames3 = []
        self.sheet = image.load("%s/data/meow/meow_sheet_stay.png" % ICON_DIR)
        self.sheet2 = image.load("%s/data/meow/meow_sheet_left.png" % ICON_DIR)
        self.sheet3 = image.load("%s/data/meow/meow_sheet_right.png" % ICON_DIR)
        self.rows = 1
        self.columns = 8
        self.cut_sheet(self.sheet, self.columns, self.rows)
        self.cut_sheet2(self.sheet2, self.columns, self.rows)
        self.cut_sheet3(self.sheet3, self.columns, self.rows)
        self.cur_frame = 0
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def cut_sheet2(self, sheet, columns, rows):
        self.rect = Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames2.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def cut_sheet3(self, sheet, columns, rows):
        self.rect = Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames3.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, hero, screen, clock, left, right, up, platforms):
        global meow_on, person_main
        if 11 in meow_on:
            if person_main == "momoka":
                self.rect.x = hero.rect.x - 64
                self.rect.y = hero.rect.y - 16
            if person_main == "kokoma":
                self.rect.x = hero.rect.x - 64
                self.rect.y = hero.rect.y
            if up:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]

            if left:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames2)
                self.image = self.frames2[self.cur_frame]

            if right:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames3)
                self.image = self.frames3[self.cur_frame]

            if not (left or right):  # стоим, когда нет указаний идти
                if not up:
                    self.cur_frame = 0
                    self.image = self.frames[self.cur_frame]
        else:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]


class Player(sprite.Sprite):
    def __init__(self, x, y, screen, clock, FPS):
        global person_main
        sprite.Sprite.__init__(self)
        self.screen = screen
        self.clock = clock
        self.FPS = FPS
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.frames = []
        self.frames2 = []
        self.frames3 = []
        if person_main == "kokoma":
            self.sheet = image.load("%s/data/kokoma/kokoma_sheet_stay.png" % ICON_DIR)
            self.sheet2 = image.load("%s/data/kokoma/kokoma_sheet_left.png" % ICON_DIR)
            self.sheet3 = image.load("%s/data/kokoma/kokoma_sheet_right.png" % ICON_DIR)
            self.columns2 = 8
            self.rows = 1
            self.move_speed = 4
            self.jump_power = 10
        elif person_main == "momoka":
            self.sheet = image.load("%s/data/momoka/momoka_sheet_stay.png" % ICON_DIR)
            self.sheet2 = image.load("%s/data/momoka/momoka_sheet_left.png" % ICON_DIR)
            self.sheet3 = image.load("%s/data/momoka/momoka_sheet_right.png" % ICON_DIR)
            self.columns2 = 4
            self.rows = 1
            self.move_speed = 8
            self.jump_power = 7
        self.columns = 1
        self.cut_sheet(self.sheet, self.columns, self.rows)
        self.cut_sheet2(self.sheet2, self.columns2, self.rows)
        self.cut_sheet3(self.sheet3, self.columns2, self.rows)
        self.cur_frame = 0
        self.rect = self.rect.move(x, y)

    def die(self):
        global meow_on
        meow_on.clear()
        time.wait(900)
        die_screen(self.screen, self.clock, self.FPS)
        main(screen_flag=False)

    def win(self):
        time.wait(900)
        win_screen(self.screen, self.clock, self.FPS)
        main(screen_flag=False)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def cut_sheet2(self, sheet, columns, rows):
        self.rect = Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames2.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def cut_sheet3(self, sheet, columns, rows):
        self.rect = Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames3.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, screen, clock, FPS, left, right, up, platforms):
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -self.jump_power
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

        if left:
            self.xvel = -self.move_speed  # Лево = x- n
            self.cur_frame = (self.cur_frame + 1) % len(self.frames2)
            self.image = self.frames2[self.cur_frame]

        if right:
            self.xvel = self.move_speed  # Право = x + n
            self.cur_frame = (self.cur_frame + 1) % len(self.frames3)
            self.image = self.frames3[self.cur_frame]

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.cur_frame = 0
                self.image = self.frames[self.cur_frame]

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, screen, clock, FPS, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, screen, clock, FPS, platforms)

    def collide(self, xvel, yvel, screen, clock, FPS, platforms):
        global meow_on
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
                if isinstance(p, Monster_wraith):  # если пересакаемый блок- blocks.BlockDie или Monster
                    self.die()  # умираем
                if isinstance(p, Monster_slime):  # если пересакаемый блок- blocks.BlockDie или Monster
                    self.die()  # умираем
                if isinstance(p, Meow):
                    meow_on.append(11)
                if isinstance(p, Tile_win):
                    if 11 in meow_on:
                        meow_on.clear()
                        self.win()

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
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def terminate():
    pygame.quit()
    sys.exit()


def start_main():
    main(screen_flag=False)


def momoka_choise():
    global person_main
    person_main = "momoka"
    start_main()


def kokoma_choise():
    global person_main
    person_main = "kokoma"
    start_main()


def die_screen(screen, clock, FPS):
    intro_text = ["О нет, ты умер(", "кликни чтобы", "начать заново"]
    fon = pygame.transform.scale(load_image('die.png'), (WIN_WIDTH, WIN_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font("data/font/Fixedsys.ttf", 55)
    text_coord = 160
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 180
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def win_screen(screen, clock, FPS):
    intro_text = ["УРА, ПОБЕДА"]
    fon = pygame.transform.scale(load_image('win.jpg'), (WIN_WIDTH, WIN_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def start_screen(screen, clock, FPS):
    with open('data/txt/rules.txt', 'r', encoding="utf8") as f:
        intro_text = f.readlines()
    f.close()
    fon = pygame.transform.scale(load_image('fon.png'), (WIN_WIDTH, WIN_HEIGHT))
    img = load_image("kokoma/icon.png")
    img1 = load_image("momoka/icon.png")
    screen.blit(fon, (0, 0))
    font = pygame.font.Font("data/font/Fixedsys.ttf", 20)
    font1 = pygame.font.Font("data/font/MotelKingMedium.ttf", 50)
    text_coord = 170
    string_rendered1 = font1.render("NE MARIO", 1, pygame.Color('white'))
    intro_rect1 = string_rendered1.get_rect()
    intro_rect1.top = 40
    intro_rect1.x = 230
    screen.blit(string_rendered1, intro_rect1)
    pygame.draw.rect(screen, "black", (30, 170, 270, 440))
    for line in intro_text:
        string_rendered = font.render(line[:-1], 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 40
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    screen.blit(img, (400, 350))
    screen.blit(img1, (600, 350))
    pygame.display.flip()
    Button(600, 540, 150, 55, 'Momoka', momoka_choise)
    Button(400, 540, 150, 55, 'Kokoma', kokoma_choise, True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        for objt in objects:
            objt.process(screen)
        pygame.display.flip()
        clock.tick(FPS)


def main(screen_flag=True):
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    programIcon = pygame.image.load("data\momoka\momoka_love.png")
    pygame.display.set_icon(programIcon)
    pygame.display.set_caption("ne mario")  # Пишем в шапку
    fon = load_image(f'bg/{random.choice(os.listdir("data/bg"))}')
    FPS = 30
    clock = pygame.time.Clock()
    # будем использовать как фон
    monsters = pygame.sprite.Group()  # Все передвигающиеся объекты
    entities = pygame.sprite.Group()  # Все объекты

    if screen_flag:
        start_screen(screen, clock, FPS)

    left = right = False  # по умолчанию - стоим
    up = False

    platforms = []  # то, во что мы будем врезаться или опираться

    with open(f'data/map/{random.choice(os.listdir("data/map"))}', 'r') as f:
        level = f.readlines()

    f.close()

    clock = pygame.time.Clock()
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Tile(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "@":
                pf = Tile_win(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == ".":
                mn = Monster_wraith(x, y, 2, 3, 150, 15)
                entities.add(mn)
                platforms.append(mn)
                monsters.add(mn)
            if col == ",":
                mn1 = Monster_slime(300, 576, 2, 3)
                entities.add(mn1)
                platforms.append(mn1)
                monsters.add(mn1)
            if col == "+":
                meow = Meow(x, y, screen, clock, FPS)
                entities.add(meow)
                platforms.append(meow)
            if col == "=":
                hero = Player(x, y, screen, clock, FPS)  # создаем героя по (x,y) координатам
                entities.add(hero)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0][:-1]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level[:-1]) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while 1:  # Основной цикл программы
        clock.tick(FPS)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                terminate()
            if e.type == KEYDOWN and (e.key == K_w or e.key == K_UP):
                up = True
            if e.type == KEYDOWN and (e.key == K_a or e.key == K_LEFT):
                left = True
            if e.type == KEYDOWN and (e.key == K_d or e.key == K_RIGHT):
                right = True
            if e.type == KEYUP and (e.key == K_w or e.key == K_UP):
                up = False
            if e.type == KEYUP and (e.key == K_d or e.key == K_RIGHT):
                right = False
            if e.type == KEYUP and (e.key == K_a or e.key == K_LEFT):
                left = False

        screen.blit(fon, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.update(screen, clock, FPS, left, right, up, platforms)  # передвижение
        meow.update(hero, screen, clock, left, right, up, platforms)
        monsters.update(platforms)  # передвигаем всех монстров
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()  # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()
