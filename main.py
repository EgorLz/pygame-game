import pygame
import os
import sys

pygame.init()
size = widht, height = 600, 600
screen = pygame.display.set_mode(size)

def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (widht, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = os.path.join("data", filename)

    if not os.path.isfile(filename):
        print(f"Файл с изображением '{filename}' не найден")
        sys.exit()

    with open(filename, "r") as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, "."), level_map))


def generate_level(level):
    global player
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == ".":
                Tile('empty', x, y)
            elif level[y][x] == "#":
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                Player(x, y)
                player = Player(x, y)
    return player, x, y


tile_images = {
    'empty': load_image('grass.png'),
    'wall': load_image('box.png')
}

player_image = load_image('mar.png')

tile_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

player, level_x, level_y = None, None, None
tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tile_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            pos_x * tile_width, pos_y * tile_height
        )


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            pos_x * tile_width + 13, pos_y * tile_height + 5
        )

    def update(self, event):
        if event[pygame.K_DOWN]:
            player.rect.y += 50
        if event[pygame.K_LEFT]:
            player.rect.x -= 50
        if event[pygame.K_UP]:
            player.rect.y -= 50
        if event[pygame.K_RIGHT]:
            player.rect.x += 50


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - widht // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


player, level_x, level_y = generate_level(load_level("lvl.txt"))

camera = Camera()


class Board:
    def __init__(self, wight, height, cell_size=10, left=10, top=10):
        self.wight = wight
        self.height = height
        self.cell_size = cell_size
        self.left = left
        self.top = top
        self.board = [[0] * wight for _ in range(height)]

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, surface):
        x, y = self.left, self.top
        for i in range(self.height):
            for j in range(self.wight):
                le = (j * self.cell_size + x, i * self.cell_size + y)
                n = (self.cell_size, self.cell_size)
                pygame.draw.rect(surface, 'white', (le, n), 1)
        pass

    def get_cell(self, mouse_pos):
        pass

    def on_click(self, cell_coords):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

start_screen()
running = True

while running:
    screen.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        player.update(pygame.key.get_pressed())

    tile_group.draw(screen)
    player_group.draw(screen)

    camera.update(player);
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)

    pygame.display.flip()

pygame.quit()
