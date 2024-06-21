import copy

import pygame
import random


class Queue:
    def __init__(self, lst):
        self._queue = lst
        self._length = len(self._queue)

    def enqueue(self, elem):
        self._queue.append(copy.deepcopy(elem))
        self._length += 1

    def dequeue(self):
        if self.size() > 0:
            dequeue_elem = self._queue[0]
            self._queue = self._queue[1:]
            self._length -= 1
            return dequeue_elem

    def size(self) -> int:
        return self._length


class GameMapCreator:
    def __init__(self):
        self._antLangton = generateMap(pygame.time.get_ticks())
        self._map = self._antLangton.runGenerate()
        self._water: pygame.Surface = pygame.image.load("background/Water.png")
        self._swamp: pygame.Surface = pygame.image.load("background/swamp.png")
        self._grass: list[pygame.Surface] = [pygame.image.load("background/Grass1.png"),
                                             pygame.image.load("background/Grass2.png"),
                                             pygame.image.load("background/Grass3.png")]
        self._grassWidth, self._grassHeight = self._grass[0].get_width(), self._grass[0].get_height()
        self._waterWidth, self._waterHeight = self._water.get_width(), self._water.get_height()
        self._swampWidth, self._swampHeight = self._swamp.get_width(), self._swamp.get_height()
        self._grass_tiles: list[pygame.Surface] = [random.choice(self._grass) for _ in
                                                   range(len(self._map) * len(self._map[0]))]
        self._tile_width, self._tile_height = self._swampWidth, self._swampHeight
        self._tile_amount_x, self._tile_amount_y = len(self._map[0]), len(self._map)

    def fillMap(self, screen: pygame.Surface, cameraX: int, cameraY: int):
        grass_tile_index: int = 0
        for y, line in enumerate(self._map):
            for x, tile in enumerate(line):
                if tile == 2:
                    screen.blit(self._water, (x * self._waterWidth - cameraX, y * self._waterHeight - cameraY))
                elif tile == 1:
                    screen.blit(self._swamp, (x * self._swampWidth - cameraX, y * self._swampHeight - cameraY))
                elif tile == 0:
                    screen.blit(self._grass_tiles[grass_tile_index],
                                (x * self._grassWidth - cameraX, y * self._grassHeight - cameraY))
                    grass_tile_index += 1

    def getMap(self) -> list[list[int]]:
        return self._map

    def getTileSize(self) -> tuple[int, int]:
        return self._tile_width, self._tile_height

    def getTileAmount(self) -> tuple[int, int]:
        return self._tile_amount_x, self._tile_amount_y

    def getMapQueue(self):
        return self._antLangton.getQueue()


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
            if pygame.time.get_ticks() - self.ticks > 1000:
                rows = len(self.map)
                cols = len(self.map[0])
                final_map = [[2 for _ in range(cols + 2)] for _ in range(rows + 2)]
                for i in range(rows):
                    for j in range(cols):
                        final_map[i + 1][j + 1] = self.map[i][j]
                return final_map
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
