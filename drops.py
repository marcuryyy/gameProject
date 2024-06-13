import pygame
from abc import ABC, abstractmethod

class DropBase(ABC):
    @abstractmethod
    def update(self, cameraX, cameraY):
        pass

    @abstractmethod
    def onPickUp(self, *args):
        pass


class HealthRegeneration(DropBase):
    def __init__(self, screen, x, y):
        self._image = pygame.Surface((25, 25))
        self._image.fill("red")
        self._hitbox = self._image.get_rect()
        self._x, self._y = x, y
        self._screen = screen
        self._healthBoost = 50

    def update(self, cameraX, cameraY):
        self._screen.blit(self._image, (self._x - cameraX, self._y - cameraY))
        self._hitbox.topleft = (self._x, self._y)

    def onPickUp(self, player):
        if self._hitbox.colliderect(player.getHitbox()):
            player.addHealth(self._healthBoost)
            return True


class GhostPet(DropBase):
    def __init__(self, screen, x, y):
        self._image = pygame.Surface((25, 25))
        self._image.fill("gray")
        self._hitbox = self._image.get_rect()
        self._x, self._y = x, y
        self._screen = screen
        self._healthBoost = 50

    def update(self, cameraX, cameraY):
        self._screen.blit(self._image, (self._x - cameraX, self._y - cameraY))
        self._hitbox.topleft = (self._x, self._y)

    def onPickUp(self, player):
        if self._hitbox.colliderect(player.getHitbox()):
            return "GhostPet"
