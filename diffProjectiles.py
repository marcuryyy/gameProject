import pygame
import math
import copy
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
        self._damage: int | float = 5
        self.target: Enemy.BaseEnemy = target
        self.target_x: int = target.getCoordinates()[0]
        self.target_y: int = target.getCoordinates()[1]
        self.dir_x: int = self.target.getHitbox().centerx - x
        self.dir_y: int = self.target.getHitbox().centery - y
        self.dir_x: float = self.dir_x / math.hypot(self.dir_x, self.dir_y)
        self.dir_y: float = self.dir_y / math.hypot(self.dir_x, self.dir_y)
        self._damageTimes: int = 1
        self._damageTimesCounter: int = 0

    def update(self, screen: pygame.Surface, cameraX: int, cameraY: int):
        self._pos[0] += self.dir_x * self.speed
        self._pos[1] += self.dir_y * self.speed
        self._rect = self.image.get_rect(center=self._pos)
        screen.blit(self.image, (self._rect.x - cameraX, self._rect.y - cameraY))

    def get_cd(self) -> int:
        return self._cooldown

    def getTicks(self) -> int:
        return self._spawnTicks

    def setTicks(self, newTicks: int):
        self._spawnTicks = newTicks

    def killOnCollision(self, enemies: list[Enemy.BaseEnemy]):
        for enemy in enemies:
            temp_rect = copy.deepcopy(self._rect)
            if temp_rect.colliderect(enemy.getHitbox()) and self._damageTimesCounter < self._damageTimes:
                self.target.Damage(self._damage)
                self._damageTimesCounter += 1
                return True

    def destroy(self, currentTicks: int) -> bool | None:
        if currentTicks - self._spawnTicks > self._timeAlive:
            return True


class BabyGhost:
    def __init__(self, screen: pygame.Surface, x: int, y: int):
        self._screen: pygame.Surface = screen
        self._runFramesRight: list[str] = ["pets/babyGhost/rightRun/run1.png",
                                           "pets/babyGhost/rightRun/run2.png",
                                           "pets/babyGhost/rightRun/run3.png",
                                           "pets/babyGhost/rightRun/run4.png",
                                           "pets/babyGhost/rightRun/run5.png",
                                           "pets/babyGhost/rightRun/run6.png",
                                           "pets/babyGhost/rightRun/run7.png",
                                           "pets/babyGhost/rightRun/run8.png",
                                           "pets/babyGhost/rightRun/run9.png",
                                           "pets/babyGhost/rightRun/run10.png",
                                           "pets/babyGhost/rightRun/run11.png",
                                           "pets/babyGhost/rightRun/run12.png",
                                           ]
        self._runFrameRight: int = 0
        self._runFramesLeft: list[str] = ["pets/babyGhost/leftRun/run1.png",
                                          "pets/babyGhost/leftRun/run2.png",
                                          "pets/babyGhost/leftRun/run3.png",
                                          "pets/babyGhost/leftRun/run4.png",
                                          "pets/babyGhost/leftRun/run5.png",
                                          "pets/babyGhost/leftRun/run6.png",
                                          "pets/babyGhost/leftRun/run7.png",
                                          "pets/babyGhost/leftRun/run8.png",
                                          "pets/babyGhost/leftRun/run9.png",
                                          "pets/babyGhost/leftRun/run10.png",
                                          "pets/babyGhost/leftRun/run11.png",
                                          "pets/babyGhost/leftRun/run12.png",
                                          ]
        self._runFrameLeft: int = 0
        self.image: pygame.Surface = pygame.image.load(self._runFramesRight[0])
        self._hitbox: pygame.Rect = self.image.get_rect()
        self._offset: int = 50
        self._hitbox.x, self._hitbox.y = x - self._offset, y - self._offset * 1.5
        self._focusEnemy: Enemy.BaseEnemy | None = None
        self._isAttacking: bool = False
        self._attackRadius: int = 250
        self._speed: int = 2

    def followPlayer(self, x: int, y: int, cameraX: int, cameraY: int, enemies: list[Enemy.BaseEnemy]):
        if not self._isAttacking:
            self._hitbox.x, self._hitbox.y = x - self._offset, y - self._offset * 1.5
            self._screen.blit(self.image, (self._hitbox.x - cameraX, self._hitbox.y - cameraY))
            for enemy in enemies:
                enemy_x, enemy_y = enemy.getHitbox().topleft
                distance = ((enemy_x - self._hitbox.x) ** 2 + (enemy_y - self._hitbox.y) ** 2) ** 0.5
                if distance <= self._attackRadius:
                    self._focusEnemy = enemy
                    self._isAttacking = True
        else:
            self.attackEnemy(cameraX, cameraY)

    def attackEnemy(self, cameraX: int, cameraY: int):
        if not self._hitbox.colliderect(self._focusEnemy.getHitbox()):
            enemy_x, enemy_y = self._focusEnemy.getHitbox().topleft
            dx, dy = enemy_x - self._hitbox.x, enemy_y - self._hitbox.y
            vector_length = math.hypot(dx, dy)
            dx, dy = dx / vector_length, dy / vector_length
            if enemy_x > self._hitbox.x:
                self._runFrameRight += 0.05
                if self._runFrameRight >= 12:
                    self._runFrameRight = 0
                self.image = pygame.image.load(self._runFramesRight[int(self._runFrameRight)])
            if enemy_x <= self._hitbox.x:
                self._runFrameLeft += 0.05
                if self._runFrameLeft >= 12:
                    self._runFrameLeft = 0
                self.image = pygame.image.load(self._runFramesLeft[int(self._runFrameLeft)])
            self._hitbox.x += dx * self._speed
            self._hitbox.y += dy * self._speed
        else:
            self._focusEnemy.getDamage(1)
        self._screen.blit(self.image, (self._hitbox.x - cameraX, self._hitbox.y - cameraY))
        if self._focusEnemy.getHP() < 1:
            self._isAttacking = False
            self._focusEnemy = None
