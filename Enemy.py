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


class GhostEnemy(BaseEnemy):
    def __init__(self, screen):
        self._screen = screen
        self._runFramesRight = ["Enemies/Ghost/GhostAnimations/rightRun/run1.png",
                          "Enemies/Ghost/GhostAnimations/rightRun/run2.png",
                          "Enemies/Ghost/GhostAnimations/rightRun/run3.png",
                          "Enemies/Ghost/GhostAnimations/rightRun/run4.png",
                          "Enemies/Ghost/GhostAnimations/rightRun/run5.png",
                          "Enemies/Ghost/GhostAnimations/rightRun/run6.png",
                          "Enemies/Ghost/GhostAnimations/rightRun/run7.png",
                          "Enemies/Ghost/GhostAnimations/rightRun/run8.png",
                          "Enemies/Ghost/GhostAnimations/rightRun/run9.png",
                          "Enemies/Ghost/GhostAnimations/rightRun/run10.png",
                          "Enemies/Ghost/GhostAnimations/rightRun/run11.png",
                                "Enemies/Ghost/GhostAnimations/rightRun/run12.png",
                                ]
        self._runFrameRight = 0
        self._runFramesLeft = ["Enemies/Ghost/GhostAnimations/leftRun/run1.png",
                                "Enemies/Ghost/GhostAnimations/leftRun/run2.png",
                                "Enemies/Ghost/GhostAnimations/leftRun/run3.png",
                                "Enemies/Ghost/GhostAnimations/leftRun/run4.png",
                                "Enemies/Ghost/GhostAnimations/leftRun/run5.png",
                                "Enemies/Ghost/GhostAnimations/leftRun/run6.png",
                                "Enemies/Ghost/GhostAnimations/leftRun/run7.png",
                                "Enemies/Ghost/GhostAnimations/leftRun/run8.png",
                                "Enemies/Ghost/GhostAnimations/leftRun/run9.png",
                                "Enemies/Ghost/GhostAnimations/leftRun/run10.png",
                                "Enemies/Ghost/GhostAnimations/leftRun/run11.png",
                                "Enemies/Ghost/GhostAnimations/leftRun/run12.png",
                                ]
        self._runFrameLeft = 0
        self.enemy_image = pygame.image.load(self._runFramesRight[0])
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
        if x > self._x:
            self._runFrameRight += 0.05
            if self._runFrameRight >= 12:
                self._runFrameRight = 0
            self.enemy_image = pygame.image.load(self._runFramesRight[int(self._runFrameRight)])
        if x <= self._x:
            self._runFrameLeft += 0.05
            if self._runFrameLeft >= 12:
                self._runFrameLeft = 0
            self.enemy_image = pygame.image.load(self._runFramesLeft[int(self._runFrameLeft)])
        self._screen.blit(self.enemy_image, (self._x - cameraX, self._y - cameraY))
        self._hitbox.topleft = (self._x, self._y)

    def getDrawState(self):
        return self._isDrawn

    def setDrawState(self):
        self._isDrawn = True

    def checkCollisions(self, player: player.Player, player_hitbox: pygame.Rect):
        if self._hitbox.colliderect(player_hitbox):
            player.getDamage(self._damage)

    def getDamage(self, amount: int | float):
        self.enemy_image = pygame.image.load(self._runFramesRight[0])
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


class ZombieEnemy(BaseEnemy):
    def __init__(self, screen):
        self._screen = screen
        self._runFramesRight = ["Enemies/Zombie/ZombieAnimations/rightRun/run1.png",
                               "Enemies/Zombie/ZombieAnimations/rightRun/run2.png",
                               "Enemies/Zombie/ZombieAnimations/rightRun/run3.png",
                               "Enemies/Zombie/ZombieAnimations/rightRun/run4.png",
                               "Enemies/Zombie/ZombieAnimations/rightRun/run5.png",
                               "Enemies/Zombie/ZombieAnimations/rightRun/run6.png",
                               "Enemies/Zombie/ZombieAnimations/rightRun/run7.png",
                               "Enemies/Zombie/ZombieAnimations/rightRun/run8.png"
                               ]
        self._runFrameRight = 0
        self._runFramesLeft = ["Enemies/Zombie/ZombieAnimations/leftRun/run1.png",
                               "Enemies/Zombie/ZombieAnimations/leftRun/run2.png",
                               "Enemies/Zombie/ZombieAnimations/leftRun/run3.png",
                               "Enemies/Zombie/ZombieAnimations/leftRun/run4.png",
                               "Enemies/Zombie/ZombieAnimations/leftRun/run5.png",
                               "Enemies/Zombie/ZombieAnimations/leftRun/run6.png",
                               "Enemies/Zombie/ZombieAnimations/leftRun/run7.png",
                               "Enemies/Zombie/ZombieAnimations/leftRun/run8.png"
                               ]
        self._runFrameLeft = 0
        self.enemy_image = pygame.image.load(self._runFramesLeft[0])
        self._hitbox = pygame.Rect((0, 0), (80, 130))
        self._x, self._y = 0, 0
        self.speed = 1.5
        self._health = 10
        self._isDrawn = False
        self._damage = 3.5

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
        if x > self._x:
            self._runFrameRight += 0.05
            if self._runFrameRight >= 8:
                self._runFrameRight = 0
            self.enemy_image = pygame.image.load(self._runFramesRight[int(self._runFrameRight)]).convert_alpha()
        if x <= self._x:
            self._runFrameLeft += 0.05
            if self._runFrameLeft >= 8:
                self._runFrameLeft = 0
            self.enemy_image = pygame.image.load(self._runFramesLeft[int(self._runFrameLeft)]).convert_alpha()
        self._screen.blit(self.enemy_image, (self._x - cameraX, self._y - cameraY))
        self._hitbox.topleft = (self._x, self._y)
        self.enemy_image = self.enemy_image = pygame.image.load(self._runFramesLeft[0])

    def getDrawState(self):
        return self._isDrawn

    def setDrawState(self):
        self._isDrawn = True

    def checkCollisions(self, player: player.Player, player_hitbox: pygame.Rect):
        if self._hitbox.colliderect(player_hitbox):
            player.getDamage(self._damage)

    def getDamage(self, amount: int | float):
        self.enemy_image = self.enemy_image = pygame.image.load(self._runFramesLeft[0])
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
        return goods