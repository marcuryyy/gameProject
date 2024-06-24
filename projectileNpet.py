import math
import os

import pygame

import Enemy


class FireProjectile:
    def __init__(self, x: int, y: int, target: Enemy.BaseEnemy, ticks: int, cameraX: int, cameraY: int):
        self.image: pygame.Surface = pygame.image.load("projectiles/fire.png")
        self._rect: pygame.Rect = self.image.get_rect()
        self._rect.x, self._rect.y = x, y
        self._cameraX, self._cameraY = cameraX, cameraY
        self._pos: list[int, int] = [x, y]
        self.speed: int = 1
        self._cooldown: int = 1000
        self._timeAlive: int = 5000
        self._spawnTicks: int = ticks
        self._damage: int | float = 10
        self.target: Enemy.BaseEnemy = target
        self.target_x: int = target.getCoordinates()[0]
        self.target_y: int = target.getCoordinates()[1]
        self.dir_x: int = self.target.getHitbox().centerx - x
        self.dir_y: int = self.target.getHitbox().centery - y
        self.dir_x: float = self.dir_x / math.hypot(self.dir_x, self.dir_y)
        self.dir_y: float = self.dir_y / math.hypot(self.dir_x, self.dir_y)
        self._damageTimes: int = 1
        self._damageTimesCounter: int = 0

    def update(self):
        self._pos[0] += self.dir_x * self.speed
        self._pos[1] += self.dir_y * self.speed
        self._rect = self.image.get_rect(center=self._pos)

    def get_cd(self) -> int:
        return self._cooldown

    def getTicks(self) -> int:
        return self._spawnTicks

    def setTicks(self, newTicks: int):
        self._spawnTicks = newTicks

    def getHitbox(self) -> pygame.Rect:
        return self._rect

    def getDamage(self) -> int:
        return self._damage

    def increaseDamageCounter(self):
        self._damageTimesCounter += 1

    def getDamageCounter(self) -> tuple[int, int]:
        return self._damageTimes, self._damageTimesCounter

    def destroyOnTime(self, currentTicks: int) -> bool | None:
        if currentTicks - self._spawnTicks > self._timeAlive:
            return True

    def getCoordinates(self) -> tuple[int, int]:
        return self._rect.x, self._rect.y

    def getImage(self) -> pygame.Surface:
        return self.image


class BabyGhost:
    def __init__(self, screen: pygame.Surface, x: int, y: int):
        self._screen: pygame.Surface = screen
        self._runFramesRight: list[str] = os.listdir("pets/babyGhost/rightRun")
        self._runFrameRight: int = 0
        self._runFramesLeft: list[str] = os.listdir("pets/babyGhost/leftRun")
        self._runFrameLeft: int = 0
        self.image: pygame.Surface = pygame.image.load("pets/babyGhost/rightRun/run1.png")
        self._hitbox: pygame.Rect = self.image.get_rect()
        self._offset: int = 50
        self._hitbox.x, self._hitbox.y = x - self._offset, y - self._offset * 1.5
        self._focusEnemy: Enemy.BaseEnemy | None = None
        self._isAttacking: bool = False
        self._attackRadius: int = 250
        self._speed: int = 2
        self._damage: int = 5

    def followPlayer(self, x: int, y: int, cameraX: int, cameraY: int, enemies: list[Enemy.BaseEnemy]):
        if not self._isAttacking:
            self._hitbox.x, self._hitbox.y = x - self._offset, y - self._offset * 1.5
            self._screen.blit(self.image, (self._hitbox.x - cameraX, self._hitbox.y - cameraY))
            self.findClosestEnemy(enemies)
        else:
            self.attackEnemy(cameraX, cameraY)

    def attackEnemy(self, cameraX: int, cameraY: int):
        enemy_x, enemy_y = self._focusEnemy.getHitbox().topleft
        dx, dy = enemy_x - self._hitbox.x, enemy_y - self._hitbox.y
        vector_length = math.hypot(dx, dy)
        dx, dy = dx / vector_length, dy / vector_length
        self._hitbox.x += dx * self._speed
        self._hitbox.y += dy * self._speed
        self.processAnimation(enemy_x)
        if self._focusEnemy.getHP() < 1:
            self._isAttacking = False
            self._focusEnemy = None

    def findClosestEnemy(self, enemies: list[Enemy.BaseEnemy]):
        for enemy in enemies:
            enemy_x, enemy_y = enemy.getHitbox().topleft
            distance = ((enemy_x - self._hitbox.x) ** 2 + (enemy_y - self._hitbox.y) ** 2) ** 0.5
            if distance <= self._attackRadius:
                self._focusEnemy = enemy
                self._isAttacking = True

    def processAnimation(self, enemy_x: int | float):
        if enemy_x > self._hitbox.x:
            self._runFrameRight += 0.05
            if self._runFrameRight >= len(self._runFramesRight):
                self._runFrameRight = 0
            self.image = pygame.image.load(f"pets/babyGhost/rightRun/{self._runFramesRight[int(self._runFrameRight)]}")
        if enemy_x <= self._hitbox.x:
            self._runFrameLeft += 0.05
            if self._runFrameLeft >= len(self._runFramesLeft):
                self._runFrameLeft = 0
            self.image = pygame.image.load(f"pets/babyGhost/leftRun/{self._runFramesLeft[int(self._runFrameLeft)]}")

    def getHitbox(self) -> pygame.Rect:
        return self._hitbox

    def getDamage(self) -> int:
        return self._damage

    def getCoordinates(self) -> tuple[int, int]:
        return self._hitbox.x, self._hitbox.y

    def getImage(self) -> pygame.Surface:
        return self.image