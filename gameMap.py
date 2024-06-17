import pygame
import random
import antLangton


class GameMapCreator:
    def __init__(self):
        self._antLangton = antLangton.generateMap(pygame.time.get_ticks())
        self._map = self._antLangton.runGenerate()
        self._water = pygame.image.load("background/Water.png")
        self._road = pygame.image.load("background/swamp.png")
        self._grass = [pygame.image.load("background/Grass1.png"), pygame.image.load("background/Grass2.png"),
                       pygame.image.load("background/Grass3.png")]
        self._grassWidth, self._grassHeight = self._grass[0].get_width(), self._grass[0].get_height()
        self._waterWidth, self._waterHeight = self._water.get_width(), self._water.get_height()
        self._roadWidth, self._roadHeight = self._road.get_width(), self._road.get_height()
        self._grass_tiles = [random.choice(self._grass) for _ in range(len(self._map) * len(self._map[0]))]
        self._tile_width, self._tile_height = 400, 400
        self._tile_amount_x, self._tile_amount_y = len(self._map[0]), len(self._map)

    def fillMap(self, screen, cameraX, cameraY):
        grass_tile_index: int = 0
        for y, line in enumerate(self._map):
            for x, tile in enumerate(line):
                if tile == 2:
                    screen.blit(self._water, (x * self._waterWidth - cameraX, y * self._waterHeight - cameraY))
                elif tile == 1:
                    screen.blit(self._road, (x * self._roadWidth - cameraX, y * self._roadHeight - cameraY))
                elif tile == 0:
                    screen.blit(self._grass_tiles[grass_tile_index],
                                (x * self._grassWidth - cameraX, y * self._grassHeight - cameraY))
                    grass_tile_index += 1

    def getMap(self):
        return self._map

    def getTileSize(self):
        return self._tile_width, self._tile_height

    def getTileAmount(self):
        return self._tile_amount_x, self._tile_amount_y
