import pygame
import gameMap
from abc import ABC, abstractmethod

from EC.Component import components

pygame.init()


class Player:
    def __init__(self, screen: pygame.Surface, health: components.Health,
                 stamina: components.Stamina, speed: components.Speed):
        self._screen = screen
        self.player_image: pygame.Surface = pygame.image.load("playerAnimations/idle/idle1.png")
        self._idleFrames: list[str] = ["playerAnimations/idle/idle1.png", "playerAnimations/idle/idle2.png",
                                       "playerAnimations/idle/idle3.png", "playerAnimations/idle/idle4.png",
                                       "playerAnimations/idle/idle5.png", "playerAnimations/idle/idle6.png",
                                       "playerAnimations/idle/idle7.png",
                                       "playerAnimations/idle/idle8.png",
                                       "playerAnimations/idle/idle9.png", "playerAnimations/idle/idle10.png"
                                       ]
        self._idleFrame: int = 0
        self._runFramesRight: list[str] = ["playerAnimations/rightRun/run1.png", "playerAnimations/rightRun/run2.png",
                                           "playerAnimations/rightRun/run3.png", "playerAnimations/rightRun/run4.png",
                                           "playerAnimations/rightRun/run5.png", "playerAnimations/rightRun/run6.png",
                                           "playerAnimations/rightRun/run7.png", "playerAnimations/rightRun/run8.png",
                                           "playerAnimations/rightRun/run9.png", "playerAnimations/rightRun/run10.png"
                                           ]
        self._runFrameRight: int = 0
        self._runFramesLeft: list[str] = ["playerAnimations/leftRun/run1.png", "playerAnimations/leftRun/run2.png",
                                          "playerAnimations/leftRun/run3.png", "playerAnimations/leftRun/run4.png",
                                          "playerAnimations/leftRun/run5.png", "playerAnimations/leftRun/run6.png",
                                          "playerAnimations/leftRun/run7.png", "playerAnimations/leftRun/run8.png",
                                          "playerAnimations/leftRun/run9.png", "playerAnimations/leftRun/run10.png",
                                          ]
        self._runFrameLeft: int = 0
        self._hitbox: pygame.Rect = pygame.Rect((0, 0), (90, 90))
        self._x: int = self._hitbox.topleft[0] + 1000
        self._y: int = self._hitbox.topleft[1] + 1000
        self._speed: components.Speed = speed
        self._hp: components.Health = health
        self._stamina: components.Stamina = stamina
        self._heatlhbar: HealthBar = HealthBar(5, 5, 200, 30, self._hp.getMAXHP())
        self._staminabar: StaminaBar = StaminaBar(5, 50, 200, 30, self._stamina.getStamina())
        self._dashLength: int = 100
        self._isAttacking: bool = False
        self._isDashing: bool = False
        self._isRunningRight: bool = False
        self._isRunningLeft: bool = False

    def update(self, cameraX: int, cameraY: int):
        if not (self._isRunningLeft or self._isRunningRight):
            self._idleFrame += 0.05
            if self._idleFrame >= len(self._idleFrames) - 1:
                self._idleFrame = 0
            self.player_image = pygame.image.load(self._idleFrames[int(self._idleFrame)]).convert_alpha()
        else:
            if self._isRunningRight:
                self._runFrameRight += 0.05
                if self._runFrameRight >= len(self._runFramesRight) - 1:
                    self._runFrameRight = 0
                self.player_image = pygame.image.load(self._runFramesRight[int(self._runFrameRight)]).convert_alpha()
            else:
                self._runFrameLeft += 0.05
                if self._runFrameLeft >= len(self._runFramesLeft) - 1:
                    self._runFrameLeft = 0
                self.player_image = pygame.image.load(self._runFramesLeft[int(self._runFrameLeft)]).convert_alpha()
        offset_x: int = self._hitbox.centerx - self.player_image.get_width() // 2
        offset_y: int = self._hitbox.centery - self.player_image.get_height() // 2
        self._screen.blit(self.player_image, (offset_x - cameraX, offset_y - cameraY))
        if self._stamina.getStamina() < 100:
            self._stamina.increaseStamina(0.1)
            self._isDashing = False

    def handle_keys(self, game_map: gameMap.GameMapCreator):
        self._isRunningRight = self._isRunningLeft = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            self._isDashing = True
        if game_map.getMap()[int(self._y // game_map.getTileSize()[1])][int(self._x // game_map.getTileSize()[0])] == 1:
            self._speed.setSpeed(2)
        else:
            self._speed.setSpeed(4)
        if (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and (keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            self._speed.setSpeed(self._speed.getSpeed() / (2 ** 0.5))
        if keys[pygame.K_LEFT]:
            if self._x - game_map.getTileSize()[0] > 10:
                self._x -= self._speed.getSpeed()
            if self._isDashing:
                if self._stamina.getStamina() >= 100:
                    self._stamina.setStamina(0)
                    self._x -= self._speed.getSpeed() * self._dashLength
            self.setRunningStateLeft(True)
        elif keys[pygame.K_RIGHT]:
            if abs(self._x - (game_map.getTileSize()[0] * (game_map.getTileAmount()[0] - 1))) > 15:
                self._x += self._speed.getSpeed()
            if self._isDashing:
                if self._stamina.getStamina() >= 100:
                    self._stamina.setStamina(0)
                    self._x += self._speed.getSpeed() * self._dashLength
            self.setRunningStateRight(True)
        if keys[pygame.K_UP]:
            if self._y - game_map.getTileSize()[1] > 20:
                self._y -= self._speed.getSpeed()
            if self._isDashing:
                if self._stamina.getStamina() >= 100:
                    self._stamina.setStamina(0)
                    self._y -= self._speed.getSpeed() * self._dashLength
            self.setRunningStateLeft(True)
        elif keys[pygame.K_DOWN]:
            if (game_map.getTileSize()[1] * (game_map.getTileAmount()[1] - 1)) - self._y > 1:
                self._y += self._speed.getSpeed()
            if self._isDashing:
                if self._stamina.getStamina() == 100:
                    self._stamina.setStamina(0)
                    self._y += self._speed.getSpeed() * self._dashLength
            self.setRunningStateRight(True)
        self._hitbox.topleft = (self._x, self._y)

    def getCoordinates(self) -> tuple[int, int]:
        return self._x, self._y

    def getHitbox(self) -> pygame.Rect:
        return self._hitbox

    def getHP(self) -> int:
        return self._hp.getHP()

    def getMaxHP(self) -> int:
        return self._hp.getMAXHP()

    def getDamage(self, amount: int):
        self._hp.decreaseHP(amount)

    def getHealthBar(self):
        return self._heatlhbar

    def getAttackState(self) -> bool:
        return self._isAttacking

    def getStaminaBar(self):
        return self._staminabar

    def getSTAMINA(self) -> int:
        return self._stamina.getStamina()

    def getDashState(self) -> bool:
        return self._isDashing

    def addHealth(self, newHealth: int):
        if self._hp.getHP() + newHealth <= 500:
            self._hp.increaseHP(newHealth)
        else:
            self._hp.setHP(self._hp.getMAXHP())

    def setRunningStateRight(self, state: bool):
        self._isRunningRight = state

    def setRunningStateLeft(self, state: bool):
        self._isRunningLeft = state


class Bar(ABC):
    @abstractmethod
    def draw(self, *args):
        pass


class HealthBar(Bar):
    def __init__(self, x: int, y: int, width: int, height: int, max_hp: int):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._max_hp = max_hp

    def draw(self, screen: pygame.Surface, player_hp: int):
        ratio: float = player_hp / self._max_hp
        pygame.draw.rect(screen, "red", (self._x, self._y, self._width, self._height))
        pygame.draw.rect(screen, "green", (self._x, self._y, self._width * ratio, self._height))


class StaminaBar(Bar):
    def __init__(self, x: int, y: int, width: int, height: int, max_stamina: int):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._max_stamina = max_stamina

    def draw(self, screen: pygame.Surface, player_stamina: int):
        ratio = player_stamina / self._max_stamina
        pygame.draw.rect(screen, "red", (self._x, self._y, self._width, self._height))
        pygame.draw.rect(screen, "yellow", (self._x, self._y, self._width * ratio, self._height))
