from abc import ABC, abstractmethod
import pygame

pygame.init()
class BaseWeapon(ABC):
    @abstractmethod
    def deal_damage(self, *args):
        pass

    @abstractmethod
    def draw(self, *args):
        pass

    @abstractmethod
    def setCoordinates(self, *args):
        pass
class Stick(BaseWeapon):
    def __init__(self):
        self._image: pygame.Surface | pygame.SurfaceType = pygame.image.load("Weapons/Stick.png")
        self._hitbox: pygame.Rect = self._image.get_rect()
        self._damage: int | float = 5

    def deal_damage(self, enemies: list):
        for enemy in enemies:
            if self._hitbox.colliderect(enemy.getHitbox()):
                enemy.getDamage(self._damage)

    def draw(self, screen: pygame.Surface | pygame.SurfaceType, x: int | float, y: int | float, cameraX: int,
             cameraY: int, state: bool):
        self.setCoordinates(x, y)
        if state:
            screen.blit(self._image, (x - cameraX, y - cameraY))

    def setCoordinates(self, x: int | float, y: int | float):
        self._hitbox.topleft = (x, y)


