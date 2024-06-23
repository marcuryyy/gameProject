import copy

import pygame
import random


class Queue:
    def __init__(self, lst: list):
        self._queue = lst
        self._length = len(self._queue)

    def enqueue(self, elem: any):
        self._queue.append(copy.deepcopy(elem))
        self._length += 1

    def dequeue(self) -> any:
        if self.size() > 0:
            dequeue_elem = self._queue[0]
            self._queue = self._queue[1:]
            self._length -= 1
            return dequeue_elem

    def size(self) -> int:
        return self._length


class BaseTile:
    def __init__(self, image_path: str):
        self._image: pygame.Surface = pygame.image.load(image_path)
        self._width: int = self._image.get_width()
        self._height: int = self._image.get_height()
        self._hitbox: pygame.Rect = self._image.get_rect()

    def draw(self, screen, x: int, y: int, camera_x: int, camera_y: int):
        self._hitbox.topleft = (x * self._width, y * self._height)
        screen.blit(self._image, (x * self._width - camera_x, y * self._height - camera_y))

    def getWidth(self) -> int:
        return self._width

    def getHeight(self) -> int:
        return self._height

    def getHitbox(self) -> pygame.Rect:
        return self._hitbox


class GrassTile(BaseTile):
    def __init__(self):
        super().__init__("background/GrassTile.jpg")


class WaterTile(BaseTile):
    def __init__(self):
        super().__init__("background/Water.png")


class RocksTile(BaseTile):
    def __init__(self):
        super().__init__("background/RockTile.jpg")


class MagmaTile(BaseTile):
    def __init__(self):
        super().__init__("background/MagmaTile.jpg")

class Settings:
    def __init__(self):
        self.width, self.height = 200, 200
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.clock = pygame.time.Clock()


class generateMap(Settings):
    def __init__(self, ticks: int | float):
        super().__init__()
        self.grid: list[list] = [[self.black for _ in range(self.width // 10)] for _ in range(self.height // 10)]
        self.ant_x: int = self.width // 20
        self.ant_y: int = self.height // 20
        self.ant_direction: int = 0

        self.target_ratio: int | float = 95 / 100

        self.white_ratio: int = 0
        self.map: list[list[int]] = [[0] * (self.width // 10) for i in range(self.height // 10)]
        self._tile_map: list[list[BaseTile | None]] = [[None] * (self.width // 10) for i in range(self.height // 10)]

        self.ticks: int = ticks
        self.save_ticks: int = ticks

        self._queue = Queue([])

    def update_ant(self, x: int, y: int, direction: int, grid: list[list], white_ratio: int,
                   target_ratio: int | float) -> tuple[int, int, int, int]:
        if grid[y][x] == self.black:
            direction = (direction + 1) % 4
            grid[y][x] = self.white
            white_ratio += 1
        else:
            direction = (direction - 1) % 4
            grid[y][x] = self.black
            white_ratio -= 1

        if direction == 0 and y > 0:
            y -= 1
        elif direction == 1 and x < 19:
            x += 1
        elif direction == 2 and y < 19:
            y += 1
        elif direction == 3 and x > 0:
            x -= 1

        if white_ratio / (self.width // 10 * self.height // 10) > target_ratio:
            if random.random() < 0.8:
                direction = (direction - 1) % 4
        else:
            if random.random() < 0.8:
                direction = (direction + 1) % 4

        return x, y, direction, white_ratio

    def runGenerate(self):
        running = True
        while running:
            if pygame.time.get_ticks() - self.ticks > 5000:
                rows = len(self.map)
                cols = len(self.map[0])
                final_map = [[2 for _ in range(cols + 2)] for _ in range(rows + 2)]
                tile_map = [[WaterTile() for _ in range(cols + 2)] for _ in range(rows + 2)]
                for y in range(self.height // 10):
                    for x in range(self.width // 10):
                        if self.grid[y][x] == self.black:
                            self._tile_map[y][x] = GrassTile()
                        else:
                            self._tile_map[y][x] = RocksTile()
                for i in range(rows):
                    for j in range(cols):
                        final_map[i + 1][j + 1] = self.map[i][j]
                        tile_map[i + 1][j + 1] = self._tile_map[i][j]
                return final_map, tile_map
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.ant_x, self.ant_y, self.ant_direction, self.white_ratio = self.update_ant(
                self.ant_x, self.ant_y, self.ant_direction, self.grid, self.white_ratio, self.target_ratio)

            for y in range(self.height // 10):
                for x in range(self.width // 10):
                    if self.grid[y][x] == self.black:
                        self.map[y][x] = 0
                    else:
                        self.map[y][x] = 1

            if pygame.time.get_ticks() - self.save_ticks > 500:
                self.save_ticks = pygame.time.get_ticks()
                self._queue.enqueue(self.map)

    def getQueue(self):
        return self._queue
