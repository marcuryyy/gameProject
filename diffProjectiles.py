import pygame
import math
import copy
import Enemy


class FireProjectile:
    def __init__(self, x, y, target: Enemy.BaseEnemy, ticks, cameraX, cameraY):
        self.image = pygame.Surface((10, 10))
        self.image.fill("yellow")
        self._rect = self.image.get_rect()
        self._rect.x, self._rect.y = x, y
        self._cameraX, self._cameraY = cameraX, cameraY
        self._pos = [x, y]
        self.speed = 1
        self._cooldown = 1000
        self._timeAlive = 5000
        self._spawnTicks = ticks
        self._damage = 5
        self.target = target
        self.target_x = target.getCoordinates()[0]
        self.target_y = target.getCoordinates()[1]
        self.dir_x = self.target.getHitbox().centerx - x
        self.dir_y = self.target.getHitbox().centery - y
        self.dir_x = self.dir_x/math.hypot(self.dir_x, self.dir_y)
        self.dir_y = self.dir_y/math.hypot(self.dir_x, self.dir_y)
        self._angle = math.degrees(math.atan2(-self.dir_y, self.dir_x))
        self._damageTimes = 1
        self._damageTimesCounter = 0

    def update(self, screen, cameraX, cameraY):
        self._pos[0] += self.dir_x * self.speed
        self._pos[1] += self.dir_y * self.speed
        self._rect = self.image.get_rect(center=self._pos)
        screen.blit(self.image, (self._rect.x - cameraX, self._rect.y - cameraY))



    def get_cd(self):
        return self._cooldown

    def getTicks(self):
        return self._spawnTicks

    def setTicks(self, newTicks):
        self._spawnTicks = newTicks

    def killOnCollision(self, enemies: list):
        for enemy in enemies:
            temp_rect = copy.deepcopy(self._rect)
            if temp_rect.colliderect(enemy.getHitbox()) and self._damageTimesCounter < self._damageTimes:
                self.target.getDamage(self._damage)
                self._damageTimesCounter += 1
                return True

    def destroy(self, currentTicks):
        if currentTicks - self._spawnTicks > self._timeAlive:
            return True


class BabyGhost:
    def __init__(self, screen, x, y):
        self._screen = screen
        self.image = pygame.image.load("pets/babyghost.png")
        self._hitbox = self.image.get_rect()
        self._offset = 50
        self._hitbox.x, self._hitbox.y = x - self._offset, y - self._offset * 1.5
        self._focusEnemy: Enemy.BaseEnemy | None = None
        self._isAttacking = False
        self._attackRadius = 250
        self._speed = 2

    def followPlayer(self, x, y, cameraX, cameraY, enemies):
        if not self._isAttacking:
            self._hitbox.x, self._hitbox.y = x - self._offset, y - self._offset * 1.5
            self._screen.blit(self.image, (self._hitbox.x - cameraX, self._hitbox.y - cameraY))
            for enemy in enemies:
                enemy_x, enemy_y = enemy.getHitbox().topleft
                distance = ((enemy_x - self._hitbox.x)**2 + (enemy_y - self._hitbox.y)**2)**0.5
                if distance <= self._attackRadius:
                    self._focusEnemy = enemy
                    self._isAttacking = True
        else:
            self.attackEnemy(cameraX, cameraY)

    def attackEnemy(self, cameraX, cameraY):
        if not self._hitbox.colliderect(self._focusEnemy.getHitbox()):
            enemy_x, enemy_y = self._focusEnemy.getHitbox().topleft
            dx, dy = enemy_x - self._hitbox.x, enemy_y - self._hitbox.y
            vector_length = math.hypot(dx, dy)
            dx, dy = dx / vector_length, dy / vector_length
            self._hitbox.x += dx * self._speed
            self._hitbox.y += dy * self._speed
        else:
            self._focusEnemy.getDamage(1)
        self._screen.blit(self.image, (self._hitbox.x - cameraX, self._hitbox.y - cameraY))
        if self._focusEnemy.getHP() < 1:
            self._isAttacking = False
            self._focusEnemy = None



