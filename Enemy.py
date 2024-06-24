from abc import ABC, abstractmethod
import pygame
import random
import drops
import player
import math
import os
import pseudoRandomFunc

pygame.init()


class BaseEnemy(ABC):

    @abstractmethod
    def create(self, *args):
        pass

    @abstractmethod
    def updateCoordinates(self, *args):
        pass

    @abstractmethod
    def getDrawState(self) -> bool:
        pass

    @abstractmethod
    def setDrawState(self, *args):
        pass

    @abstractmethod
    def Damage(self, amount: int | float):
        pass

    @abstractmethod
    def getDamage(self) -> int:
        pass

    @abstractmethod
    def getHitbox(self) -> pygame.Rect:
        pass

    @abstractmethod
    def getHP(self) -> int:
        pass

    @abstractmethod
    def getCoordinates(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def dropGoods(self, *args):
        pass

    @abstractmethod
    def getImage(self) -> pygame.Surface:
        pass


class GhostEnemy(BaseEnemy):
    def __init__(self, screen: pygame.Surface):
        self._screen: pygame.Surface = screen
        self._runFramesRight: list[str] = os.listdir("Enemies/Ghost/GhostAnimations/rightRun")
        self._runFrameRight: int = 0
        self._runFramesLeft: list[str] = os.listdir("Enemies/Ghost/GhostAnimations/leftRun")
        self._runFrameLeft: int = 0
        self.enemy_image: pygame.Surface = pygame.image.load("Enemies/Ghost/GhostAnimations/leftRun/run1.png")
        self._hitbox: pygame.Rect = pygame.Rect((0, 0), (80, 110))
        self._x, self._y = 0, 0
        self.speed: int | float = 2
        self._health: int = 15
        self._isDrawn: bool = False
        self._damage: int = 1

    def create(self, playerX: int | float, playerY: int | float, cameraX: int | float, cameraY: int | float,
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
        self._hitbox.topleft = (self._x, self._y)

    def updateCoordinates(self, player: player.Player, x: int | float, y: int | float, cameraX: int, cameraY: int):
        if not self._hitbox.colliderect(player.getHitbox()):
            dx, dy = x - self._x, y - self._y
            vector_length = math.hypot(dx, dy)
            dx, dy = dx / vector_length, dy / vector_length
            self._x += dx * self.speed
            self._y += dy * self.speed
        if x > self._x:
            self._runFrameRight += 0.05
            if self._runFrameRight >= 12:
                self._runFrameRight = 0
            self.enemy_image = pygame.image.load(f"Enemies/Ghost/GhostAnimations/rightRun/{self._runFramesRight[int(self._runFrameRight)]}").convert_alpha()
        if x <= self._x:
            self._runFrameLeft += 0.05
            if self._runFrameLeft >= 12:
                self._runFrameLeft = 0
            self.enemy_image = pygame.image.load(f"Enemies/Ghost/GhostAnimations/leftRun/{self._runFramesRight[int(self._runFrameRight)]}").convert_alpha()
        self._hitbox.topleft = (self._x + 50, self._y)

    def getDrawState(self) -> bool:
        return self._isDrawn

    def setDrawState(self):
        self._isDrawn = True

    def Damage(self, amount: int | float):
        self.enemy_image = pygame.image.load("Enemies/Ghost/GhostAnimations/leftRun/run1.png")
        self._health -= amount

    def getDamage(self):
        return self._damage

    def getHitbox(self) -> pygame.Rect:
        return self._hitbox

    def getHP(self) -> int:
        return self._health

    def getCoordinates(self) -> tuple[int, int]:
        return self._x, self._y

    def dropGoods(self, screen: pygame.Surface, x: int, y: int, petAmount: dict[str, int]) -> drops:
        goods = None
        chances: tuple = pseudoRandom.getChances()
        if random.choice(chances[0]) == 1:
            goods = drops.HealthRegeneration(screen, x, y)
            pseudoRandom.countChances("boost", True)
        elif random.choice(chances[1]) and petAmount["GhostPet"] < 1:
            goods = drops.GhostPet(screen, x, y)
            pseudoRandom.countChances("pet", True)
        else:
            pseudoRandom.countChances("None", False)
        return goods

    def getImage(self) -> pygame.Surface:
        return self.enemy_image


class ZombieEnemy(BaseEnemy):
    def __init__(self, screen: pygame.Surface):
        self._screen: pygame.Surface = screen
        self._runFramesRight: list[str] = os.listdir("Enemies/Zombie/ZombieAnimations/rightRun")
        self._runFrameRight: int = 0
        self._runFramesLeft: list[str] = os.listdir("Enemies/Zombie/ZombieAnimations/leftRun")
        self._runFrameLeft: int = 0
        self.enemy_image: pygame.Surface = pygame.image.load("Enemies/Zombie/ZombieAnimations/leftRun/run1.png")
        self._hitbox: pygame.Rect = pygame.Rect((30, 0), (70, 80))
        self._x, self._y = 0, 0
        self.speed: int | float = 1
        self._health: int = 30
        self._isDrawn: bool = False
        self._damage: int | float = 3.5

    def create(self, playerX: int | float, playerY: int | float, cameraX: int | float, cameraY: int | float,
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
        self._hitbox.topleft = (self._x, self._y)

    def updateCoordinates(self, player: player.Player, x: int | float, y: int | float, cameraX: int, cameraY: int):
        if not self._hitbox.colliderect(player.getHitbox()):
            dx, dy = x - self._x, y - self._y
            vector_length = math.hypot(dx, dy)
            dx, dy = dx / vector_length, dy / vector_length
            self._x += dx * self.speed
            self._y += dy * self.speed
        if x > self._x:
            self._runFrameRight += 0.05
            if self._runFrameRight >= 8:
                self._runFrameRight = 0
            self.enemy_image = pygame.image.load(f"Enemies/Zombie/ZombieAnimations/rightRun/{self._runFramesRight[int(self._runFrameRight)]}").convert_alpha()
        if x <= self._x:
            self._runFrameLeft += 0.05
            if self._runFrameLeft >= 8:
                self._runFrameLeft = 0
            self.enemy_image = pygame.image.load(f"Enemies/Zombie/ZombieAnimations/leftRun/{self._runFramesLeft[int(self._runFrameLeft)]}").convert_alpha()
        self._hitbox.topleft = (self._x + 30, self._y + 30)

    def getDrawState(self) -> bool:
        return self._isDrawn

    def setDrawState(self):
        self._isDrawn = True

    def Damage(self, amount: int | float):
        self.enemy_image = self.enemy_image = pygame.image.load("Enemies/Zombie/ZombieAnimations/leftRun/run1.png")
        self._health -= amount

    def getDamage(self):
        return self._damage

    def getHitbox(self) -> pygame.Rect:
        return self._hitbox

    def getHP(self) -> int:
        return self._health

    def getCoordinates(self) -> tuple[int, int]:
        return self._x, self._y

    def dropGoods(self, screen: pygame.Surface, x: int, y: int, petAmount: dict[str, int]) -> drops:
        goods = None
        if random.randint(1, 2) == 2:
            goods = drops.HealthRegeneration(screen, x, y)
        return goods

    def getImage(self) -> pygame.Surface:
        return self.enemy_image


pseudoRandom = pseudoRandomFunc.pseudoRandom()
