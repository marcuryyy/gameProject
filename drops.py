from typing import Tuple

import numpy as np
import pygame
import numpy
from abc import ABC, abstractmethod

from numpy import ndarray

import player


class DropBase(ABC):
    @abstractmethod
    def update(self, cameraX, cameraY):
        pass

    @abstractmethod
    def onPickUp(self, *args):
        pass


class HealthRegeneration(DropBase):
    def __init__(self, screen: pygame.Surface, x: int, y: int):
        self._image: pygame.Surface = pygame.Surface((25, 25))
        self._image.fill("red")
        self._hitbox: pygame.Rect = self._image.get_rect()
        self._x, self._y = x, y
        self._screen: pygame.Surface = screen
        self._healthBoost: int = 50

    def update(self, cameraX: int, cameraY: int):
        self._screen.blit(self._image, (self._x - cameraX, self._y - cameraY))
        self._hitbox.topleft = (self._x, self._y)

    def onPickUp(self, player: player.Player) -> bool:
        if self._hitbox.colliderect(player.getHitbox()):
            player.addHealth(self._healthBoost)
            return True
        return False


class GhostPet(DropBase):
    def __init__(self, screen: pygame.Surface, x: int, y: int):
        self._image: pygame.Surface = pygame.Surface((25, 25))
        self._image.fill("gray")
        self._hitbox: pygame.Rect = self._image.get_rect()
        self._x, self._y = x, y
        self._screen: pygame.Surface = screen
        self._healthBoost: int = 50

    def update(self, cameraX: int, cameraY: int):
        self._screen.blit(self._image, (self._x - cameraX, self._y - cameraY))
        self._hitbox.topleft = (self._x, self._y)

    def onPickUp(self, player: player.Player) -> str:
        if self._hitbox.colliderect(player.getHitbox()):
            return "GhostPet"


class pseudoRandom:
    def __init__(self):
        self._boostChances: ndarray = np.array([0] * 100)
        self._petChances: ndarray = np.array([0] * 100)
        self._countBoostOnes: int = 1
        self._countPetOnes: int = 1
        self._boostChances[0], self._petChances[0] = 1, 1

    def countChances(self, dropType: str, result: bool):
        if result:
            if dropType.lower() == "boost":
                self._boostChances = np.array([0] * 100)
                self._boostChances[0] = 1
                self._countBoostOnes: int = 1
            elif dropType.lower() == "pet":
                self._petChances = np.array([0] * 100)
                self._petChances[0] = 1
                self._countPetOnes: int = 1
        else:
            if self._countBoostOnes < 20:
                lastBoostIdx: int = np.where(self._boostChances == 1)[0][-1]
                self._boostChances[lastBoostIdx + 1] = 1
            if self._countPetOnes < 10:
                lastPetIdx: int = np.where(self._petChances == 1)[0][-1]
                self._petChances[lastPetIdx + 1] = 1

    def getChances(self) -> tuple[ndarray, ndarray]:
        return self._boostChances, self._petChances





