import pygame
import Weapon
import gameMap
from abc import ABC, abstractmethod

pygame.init()


class Player:
    def __init__(self, screen):
        self._screen = screen
        self.player_image = pygame.image.load("knight.png")
        self._hitbox = self.player_image.get_rect()
        self._x, self._y = self._hitbox.centerx + 1000, self._hitbox.centery + 1000
        self._speed = None
        self._isAttacking = False
        self._isDashing = False
        self._hp = 500
        self._stamina = 100
        self._heatlhbar = HealthBar(5, 5, 200, 30, self._hp)
        self._staminabar = StaminaBar(5, 50, 200, 30, self._stamina)
        self._current_weapon = Weapon.Stick()
        self._dashLength = 100

    def update(self, cameraX, cameraY):
        self._screen.blit(self.player_image, (self._x - cameraX, self._y - cameraY))
        self._hitbox.topleft = (self._x - cameraX, self._y - cameraY)
        if self._stamina < 100:
            self._stamina += 0.1
            self._isDashing = False
        # pygame.draw.rect(self._screen, "red", self._hitbox)

    def handle_keys(self, game_map: gameMap.GameMapCreator):
        keys = pygame.key.get_pressed()
        (pygame.mouse.get_pressed())
        if keys[pygame.K_LSHIFT]:
            self._isDashing = True
        if game_map.getMap()[int(self._y // game_map.getTileSize()[1])][int(self._x // game_map.getTileSize()[0])] == 1:
            self._speed = 4
        else:
            self._speed = 2
        if (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and (keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            self._speed = self._speed / (2 ** 0.5)
        if keys[pygame.K_LEFT]:
            if self._x - game_map.getTileSize()[0] > 10:
                self._x -= self._speed
            if self._isDashing:
                if self._stamina >= 100:
                    self._stamina = 0
                    self._x -= self._speed * self._dashLength
        elif keys[pygame.K_RIGHT]:
            if abs(self._x - (game_map.getTileSize()[0] * (game_map.getTileAmount()[0] - 1))) > 15:
                self._x += self._speed
            if self._isDashing:
                if self._stamina >= 100:
                    self._stamina = 0
                    self._x += self._speed * self._dashLength
        if keys[pygame.K_UP]:
            if self._y - game_map.getTileSize()[1] > 20:
                self._y -= self._speed
            if self._isDashing:
                if self._stamina >= 100:
                    self._stamina = 0
                    self._y -= self._speed * self._dashLength
        elif keys[pygame.K_DOWN]:
            if (game_map.getTileSize()[1] * (game_map.getTileAmount()[1] - 1)) - self._y > 1:
                self._y += self._speed
            if self._isDashing:
                if self._stamina == 100:
                    self._stamina = 0
                    self._y += self._speed * self._dashLength
        self._hitbox.topleft = (self._x, self._y)

    def getCoordinates(self):
        return self._x, self._y

    def getHitbox(self):
        return self._hitbox

    def getHP(self):
        return self._hp

    def getDamage(self, amount):
        self._hp -= amount

    def getHealthBar(self):
        return self._heatlhbar

    def getWeapon(self):
        return self._current_weapon

    def getAttackState(self):
        return self._isAttacking

    def getStaminaBar(self):
        return self._staminabar

    def getSTAMINA(self):
        return self._stamina

    def getDashState(self):
        return self._isDashing

    def addHealth(self, newHealth: int):
        if self._hp + newHealth <= 500:
            self._hp += newHealth
        else:
            self._hp = 500


class Bar(ABC):
    @abstractmethod
    def draw(self, *args):
        pass


class HealthBar(Bar):
    def __init__(self, x, y, width, height, max_hp):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._max_hp = max_hp

    def draw(self, screen, player_hp):
        ratio = player_hp / self._max_hp
        pygame.draw.rect(screen, "red", (self._x, self._y, self._width, self._height))
        pygame.draw.rect(screen, "green", (self._x, self._y, self._width * ratio, self._height))


class StaminaBar(Bar):
    def __init__(self, x, y, width, height, max_stamina):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._max_stamina = max_stamina

    def draw(self, screen, player_stamina):
        ratio = player_stamina / self._max_stamina
        pygame.draw.rect(screen, "red", (self._x, self._y, self._width, self._height))
        pygame.draw.rect(screen, "yellow", (self._x, self._y, self._width * ratio, self._height))
