import pygame
import random

pygame.init()


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

        self.target_ratio: int | float = 10/100

        self.white_ratio: int = 0
        self.map: list[list[int]] = [[0] * (self.width // 10) for i in range(self.height // 10)]

        self.ticks: int = ticks

    def update_ant(self, x: int, y: int, direction: int, grid: list[list], white_ratio: int, target_ratio: int | float) -> tuple[int, int, int, int]:
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
            if pygame.time.get_ticks() - self.ticks > 10000:
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
                self.ant_x, self.ant_y, self.ant_direction, self.grid, self.white_ratio, self.target_ratio
            )

            for y in range(self.height // 10):
                for x in range(self.width // 10):
                    if self.grid[y][x] == self.black:
                        self.map[y][x] = 0
                    else:
                        self.map[y][x] = 1

            pygame.display.flip()

    pygame.quit()
