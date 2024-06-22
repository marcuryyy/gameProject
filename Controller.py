import pygame

import Enemy
import gameMap
import player


class Controller:
    def __init__(self, playerEntity, enemies, gameMap, tile_map):
        self._player: player.Player = playerEntity
        self._enemies: list[Enemy.BaseEnemy] = enemies
        self._game_map: list[list[int]] = gameMap
        self._tile_map: list[list[gameMap.BaseTile]] = tile_map

    def handle_collisions(self):
        for enemy in self._enemies:
            if self._player.getHitbox().colliderect(enemy.getHitbox()):
                self._player.getDamage(enemy.getDamage())

        player_rect = self._player.getHitbox()
        for y, line in enumerate(self._game_map):
            for x, tile in enumerate(line):
                if tile == 0 and player_rect.colliderect(self._tile_map[y][x].getHitbox()):
                    self._player.setSpeed(4)
                    self._player.setAllStates(True)
                if tile == 1 and player_rect.colliderect(self._tile_map[y][x].getHitbox()):
                    self._player.setSpeed(2)
                    self._player.setAllStates(True)
                if self._tile_map[y][x].__class__.__name__ == "WaterTile" and player_rect.colliderect(self._tile_map[y][x].getHitbox()):
                    if self._player.getFacing().lower() == "left":
                        self._player.setWalkLeftState(False)
                    if self._player.getFacing().lower() == "right":
                        self._player.setWalkRightState(False)
                    if self._player.getFacing().lower() == "up":
                        self._player.setWalkUpState(False)
                    if self._player.getFacing().lower() == "down":
                        self._player.setWalkDownState(False)

    def update(self, playerEntity, enemies):
        self._player = playerEntity
        self._enemies = enemies
        self.handle_collisions()
