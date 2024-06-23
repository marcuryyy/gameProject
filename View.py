import pygame

import Enemy
import gameMap
import player
import projectileNpet


class GameSceneView:
    def __init__(self):
        self._antLangton = gameMap.generateMap(pygame.time.get_ticks())
        self._map, self._tile_map = self._antLangton.runGenerate()
        self._grass = gameMap.GrassTile()
        self._water = gameMap.WaterTile()
        self._rocks = gameMap.RocksTile()

        self._tile_width, self._tile_height = self._rocks.getWidth(), self._rocks.getHeight()
        self._tile_amount_x, self._tile_amount_y = len(self._map[0]), len(self._map)

    def fillMap(self, screen: pygame.Surface, cameraX: int, cameraY: int):
        for y, line in enumerate(self._tile_map):
            for x, tile in enumerate(line):
                tile.draw(screen, x, y, cameraX, cameraY)

    def getMap(self) -> (list[list[int]], list[list[gameMap.BaseTile]]):
        return self._map, self._tile_map

    def getTileSize(self) -> tuple[int, int]:
        return self._tile_width, self._tile_height

    def getTileAmount(self) -> tuple[int, int]:
        return self._tile_amount_x, self._tile_amount_y

    def getMapQueue(self):
        return self._antLangton.getQueue()


class EntityView:
    def __init__(self, screen: pygame.Surface, player: player.Player, enemies: list[Enemy.BaseEnemy],
                 projectiles: list[projectileNpet.FireProjectile], pet: list[projectileNpet.BabyGhost]):
        self._player = player
        self._enemies = enemies
        self._projectiles = projectiles
        self._pet = pet
        self._screen = screen

    def updatePlayer(self, cameraX: int, cameraY: int):
        self._player.updateAnimation()
        offset_x: int = self._player.getHitbox().centerx - self._player.getPlayerImage().get_width() // 2
        offset_y: int = self._player.getHitbox().centery - self._player.getPlayerImage().get_height() // 2
        self._screen.blit(self._player.getPlayerImage(), (offset_x - cameraX, offset_y - cameraY))

    def updateEnemies(self):
        pass

    def updateView(self, player: player.Player, enemies: list[Enemy.BaseEnemy],
                   projectiles: list[projectileNpet.FireProjectile], pet: list[projectileNpet.BabyGhost]):
        self._player = player
        self._enemies = enemies
        self._projectiles = projectiles
        self._pet = pet
