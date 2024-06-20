import pygame
from abc import ABC, abstractmethod
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
        self._red_rect: pygame.Surface = pygame.Surface((32, 32))
        self._red_rect.fill("red")
        self._image: pygame.Surface = pygame.image.load("dropsSprites/healthRegeneration.png")
        self._hitbox: pygame.Rect = self._image.get_rect()
        self._x, self._y = x, y
        self._screen: pygame.Surface = screen
        self._healthBoost: int = 50

    def update(self, cameraX: int, cameraY: int):
        self._screen.blit(self._red_rect, (self._x - cameraX, self._y - cameraY))
        self._screen.blit(self._image, (self._x - cameraX, self._y - cameraY))
        self._hitbox.topleft = (self._x, self._y)

    def onPickUp(self, player: player.Player) -> bool:
        if self._hitbox.colliderect(player.getHitbox()):
            player.addHealth(self._healthBoost)
            return True
        return False


class GhostPet(DropBase):
    def __init__(self, screen: pygame.Surface, x: int, y: int):
        self._gray_rect: pygame.Surface = pygame.Surface((32, 32))
        self._gray_rect.fill("gray")
        self._image: pygame.Surface = pygame.image.load("dropsSprites/ghostSprite.png")
        self._hitbox: pygame.Rect = self._image.get_rect()
        self._x, self._y = x, y
        self._screen: pygame.Surface = screen
        self._healthBoost: int = 50

    def update(self, cameraX: int, cameraY: int):
        self._screen.blit(self._gray_rect, (self._x - cameraX, self._y - cameraY))
        self._screen.blit(self._image, (self._x - cameraX, self._y - cameraY))
        self._hitbox.topleft = (self._x, self._y)

    def onPickUp(self, player: player.Player) -> str:
        if self._hitbox.colliderect(player.getHitbox()):
            return "GhostPet"







