from abc import ABC, abstractmethod
import pygame
import random
import drops
import player
import math
pygame.init()


class BaseEnemy(ABC):

    @abstractmethod
    def draw(self, *args):
        pass

    @abstractmethod
    def followPlayer(self, *args):
        pass

    @abstractmethod
    def getDrawState(self):
        pass

    @abstractmethod
    def setDrawState(self, *args):
        pass

    @abstractmethod
    def checkCollisions(self, *args):
        pass

    @abstractmethod
    def getDamage(self, amount: int | float):
        pass

    @abstractmethod
    def getHitbox(self):
        pass

    @abstractmethod
    def getHP(self):
        pass

    @abstractmethod
    def getCoordinates(self):
        pass

    @abstractmethod
    def dropGoods(self, *args):
        pass


class EasyEnemy(BaseEnemy):
    def __init__(self, screen):
        self._screen = screen
        self._images = [pygame.image.load("Enemies/Ghost.png"), pygame.image.load("Enemies/damagedGhost.png")]
        self.enemy_image = self._images[0]
        self._hitbox = pygame.Rect((0, 0), (80, 130))
        self._x, self._y = 0, 0
        self.speed = 2.5
        self._health = 10
        self._isDrawn = False
        self._damage = 1

    def draw(self, playerX: int | float, playerY: int | float, cameraX: int | float, cameraY: int | float,
             tileSize: tuple[int], tileAmount: tuple[int], screenSize: tuple[int]):
        width, height = tileSize[0] * tileAmount[0], tileSize[1] * tileAmount[1]
        side = random.randint(0, 3)
        if side == 0:
            self._x = random.randint(0, width - self._hitbox.width)
            self._y = screenSize[1] // 2 + playerY
        elif side == 1:
            self._x = screenSize[0] // 2 + playerX
            self._y = random.randint(0, height - self._hitbox.height)
        elif side == 2:
            self._x = random.randint(0, width - self._hitbox.width)
            self._y = screenSize[1] // 2 - playerY
        else:
            self._x = screenSize[0] // 2 - playerX
            self._y = random.randint(0, height - self._hitbox.height)
        self._screen.blit(self.enemy_image, (self._x - cameraX, self._y - cameraY))
        self._hitbox.topleft = (self._x, self._y)

    def followPlayer(self, player, x, y, cameraX, cameraY):
        if not self._hitbox.colliderect(player.getHitbox()):
            dx, dy = x - self._x, y - self._y
            vector_length = math.hypot(dx, dy)
            dx, dy = dx / vector_length, dy / vector_length
            self._x += dx * self.speed
            self._y += dy * self.speed
        self._screen.blit(self.enemy_image, (self._x - cameraX, self._y - cameraY))
        self._hitbox.topleft = (self._x, self._y)
        self.enemy_image = self._images[0]

    def getDrawState(self):
        return self._isDrawn

    def setDrawState(self):
        self._isDrawn = True

    def checkCollisions(self, player: player.Player, player_hitbox: pygame.Rect):
        if self._hitbox.colliderect(player_hitbox):
            player.getDamage(self._damage)

    def getDamage(self, amount: int | float):
        self.enemy_image = self._images[1]
        self._health -= amount

    def getHitbox(self):
        return self._hitbox

    def getHP(self):
        return self._health

    def getCoordinates(self):
        return self._x, self._y

    def dropGoods(self, screen, x, y, petAmount: dict[str, int]):
        goods = None
        if random.randint(1, 2) == 2:
            goods = drops.HealthRegeneration(screen, x, y)
        elif random.randint(1, 2) == 2 and petAmount["GhostPet"] < 1:
            goods = drops.GhostPet(screen, x, y)
        return goods
