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

    def updateEnemies(self, enemy: Enemy.BaseEnemy, cameraX: int, cameraY: int):
        x, y = enemy.getCoordinates()
        self._screen.blit(enemy.getImage(), (x - cameraX, y - cameraY))

    def updateProjectiles(self, projectile: projectileNpet.FireProjectile, cameraX: int, cameraY: int):
        x, y = projectile.getCoordinates()
        self._screen.blit(projectile.getImage(), (x - cameraX, y - cameraY))

    def updatePets(self, pet: projectileNpet.BabyGhost, cameraX: int, cameraY: int):
        x, y = pet.getCoordinates()
        self._screen.blit(pet.getImage(), (x - cameraX, y - cameraY))

    def drawUI(self, coinsLabel, killsLabel):
        self._player.getHealthBar().draw(self._screen, self._player.getHP())
        self._player.getStaminaBar().draw(self._screen, self._player.getSTAMINA())
        coinsLabel.draw_coins(self._screen, self._player.getCoins())
        killsLabel.drawKills(self._screen, self._player.getKills())

    def updateView(self, player: player.Player, enemies: list[Enemy.BaseEnemy],
                   projectiles: list[projectileNpet.FireProjectile], pet: list[projectileNpet.BabyGhost]):
        self._player = player
        self._enemies = enemies
        self._projectiles = projectiles
        self._pet = pet


class ButtonsViewer:
    @staticmethod
    def drawButtons(screen, button, text, text_rect):
        pygame.draw.rect(screen, "White", button)
        screen.blit(text, text_rect)
        pygame.display.update()


class LabelViewer:
    @staticmethod
    def drawLabels(screen, text, text_rect):
        screen.blit(text, text_rect)
